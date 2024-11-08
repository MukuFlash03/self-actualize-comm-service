import unittest
from app import create_app, db
import time
import os

class TestMessageAPI(unittest.TestCase):
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
                # Create a savepoint that we can rollback to after each test
                db.session.begin_nested()

    def tearDown(self):
        """Clean up after each test by rolling back database changes"""
        with self.app.app_context():
            # Rollback to the savepoint created in setUp
            db.session.rollback()
            # Remove the session to ensure clean state
            db.session.remove()

    @classmethod
    def tearDownClass(cls):
        """Cleanup after all tests"""
        with cls.app.app_context():
            # Drop all tables
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

    def test_successful_email_message(self):
        """Test successful email message submission"""
        payload = {
            "channel_type": "email",
            "recipient": "test@example.com",
            "content": "Test email content"
        }
        
        response = self.client.post('/api/sendMessage', json=payload)
        data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', data)
        self.assertIn('channel_type', data)
        self.assertIn('recipient', data)
        
        # Validating that response data should match the request data
        self.assertEqual(data['channel_type'], 'email')
        self.assertEqual(data['recipient'], 'test@example.com')
        self.assertEqual(data['content'], 'Test email content')

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

    def test_missing_required_fields(self):
      """Test missing required fields"""
      payload = {
          "channel_type": "email",
          "recipient": "test@example.com"
          # missing content field
      }
      
      response = self.client.post('/api/sendMessage', json=payload)
      
      self.assertEqual(response.status_code, 400)
      self.assertIn('error', response.get_json())

if __name__ == '__main__':
    unittest.main()
