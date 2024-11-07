from abc import ABC, abstractmethod
from typing import Dict, Any

class MessageService(ABC):
    """Abstract base class for message services"""
    
    @abstractmethod
    def send_message(self, recipient: str, content: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def validate_recipient(self, recipient: str) -> bool:
        pass
