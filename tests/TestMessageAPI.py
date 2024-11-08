import unittest
from app import create_app, db
import time
import os

class TestMessageAPI(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     cls.app = create_app()
    #     cls.app.config['TESTING'] = True
    #     cls.client = cls.app.test_client()

    @classmethod
    def setUpClass(cls):
        """Setup test app"""
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        cls.client = cls.app.test_client()
        
        # Ensure database is ready
        cls.wait_for_db()
        
        # Create tables
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def wait_for_db(cls):
        """Wait for database to be ready"""
        max_retries = 30
        retry_interval = 1
        
        with cls.app.app_context():
            for i in range(max_retries):
                try:
                    db.engine.connect()
                    return
                except Exception as e:
                    if i == max_retries - 1:
                        raise
                    time.sleep(retry_interval)

    def setUp(self):
        with self.app.app_context():
            db.session.begin_nested()

    def tearDown(self):
        with self.app.app_context():
            db.session.rollback()
            db.session.remove()

    @classmethod
    def tearDownClass(cls):
        """Cleanup after all tests"""
        with cls.app.app_context():
            db.drop_all()

    def test_send_valid_email_message(self):
        """Test sending valid email message"""
        payload = {
            "channel_type": "email",
            "recipient": "test@example.com",
            "content": "Test email"
        }
        response = self.client.post('/api/sendMessage', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_send_valid_sms_message(self):
        """Test sending valid SMS message"""
        payload = {
            "channel_type": "sms",
            "recipient": "+1234567890",
            "content": "Test SMS"
        }
        response = self.client.post('/api/sendMessage', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_send_invalid_channel_type(self):
        """Test sending message with invalid channel type"""
        payload = {
            "channel_type": "invalid",
            "recipient": "test@example.com",
            "content": "Test"
        }
        response = self.client.post('/api/sendMessage', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_send_invalid_email(self):
        """Test sending message with invalid email"""
        payload = {
            "channel_type": "email",
            "recipient": "invalid-email",
            "content": "Test"
        }
        response = self.client.post('/api/sendMessage', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()
