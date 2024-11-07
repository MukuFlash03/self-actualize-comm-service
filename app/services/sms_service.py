import logging
from typing import Dict, Any
import re
from .message_service import MessageService

class SMSService(MessageService):
    def validate_recipient(self, recipient: str) -> bool:
        """Validate phone number format (basic example)"""
        logging.info(f"Validating phone number: {recipient}")
        phone_regex = r'^\+?1?\d{9,15}$'
        return bool(re.match(phone_regex, recipient))
    
    def send_message(self, recipient: str, content: str) -> Dict[str, Any]:
        """Mock SMS sending"""
        try:
            # Log the mock SMS sending
            logging.info(f"[MOCK SMS] Sending to: {recipient}, Content: {content}")
            
            # Simulate successful sending
            return {
                "status": "delivered",
                "provider_response": "Message queued for delivery"
            }
        except Exception as e:
            logging.error(f"Failed to send SMS: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }
