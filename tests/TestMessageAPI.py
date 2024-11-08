import unittest
from app import create_app, db

class TestMessageAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
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
