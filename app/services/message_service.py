from abc import ABC, abstractmethod
from typing import Dict, Any

class MessageService(ABC):
    """Abstract base class for message services"""
    
    @abstractmethod
    def send_message(self, recipient: str, content: str) -> Dict[str, Any]:
        """Send a message to the specified recipient"""
        pass
    
    @abstractmethod
    def validate_recipient(self, recipient: str) -> bool:
        """Validate the recipient format"""
        pass
