import unittest
from app.services.email_service import EmailService
from app.services.sms_service import SMSService

class TestMessageServices(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize services"""
        cls.email_service = EmailService()
        cls.sms_service = SMSService()

    def test_valid_email_addresses(self):
        """Test various valid email formats"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.com",
            "user+label@domain.co.uk",
            "user123@domain.net",
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(
                    self.email_service.validate_recipient(email),
                    f"Should accept valid email: {email}"
                )

    def test_invalid_email_addresses(self):
        """Test various invalid email formats"""
        invalid_emails = [
            "",                     # Empty
            "plainaddress",         # Missing @ and domain
            "@domain.com",          # Missing username
            "user@",                # Missing domain
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(
                    self.email_service.validate_recipient(email),
                    f"Should reject invalid email: {email}"
                )

    def test_valid_phone_numbers(self):
        """Test various valid phone number formats"""
        valid_phones = [
            "+1234567890",
            "1234567890",
            "+442071234567",
        ]
        for phone in valid_phones:
            with self.subTest(phone=phone):
                self.assertTrue(
                    self.sms_service.validate_recipient(phone),
                    f"Should accept valid phone: {phone}"
                )

    def test_invalid_phone_numbers(self):
        """Test various invalid phone number formats"""
        invalid_phones = [
            "",                # Empty
            "123",            # Too short
            "abcdefghij",     # Contains non-digits
        ]
        for phone in invalid_phones:
            with self.subTest(phone=phone):
                self.assertFalse(
                    self.sms_service.validate_recipient(phone),
                    f"Should reject invalid phone: {phone}"
                )

if __name__ == '__main__':
    unittest.main()
