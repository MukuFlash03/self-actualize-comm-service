import logging
from typing import Dict, Any
import re
from .message_service import MessageService

class EmailService(MessageService):
    def validate_recipient(self, recipient: str) -> bool:
        """Validate email format"""
        logging.info(f"Validating email: {recipient}")
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, recipient))
    
    def send_message(self, recipient: str, content: str) -> Dict[str, Any]:
        """Mock email sending"""
        try:
            # Log the mock email sending
            logging.info(f"[MOCK EMAIL] Sending to: {recipient}, Content: {content}")
            
            # Simulate successful sending
            return {
                "status": "delivered",
                "provider_response": "250 OK: Message accepted for delivery"
            }
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }
