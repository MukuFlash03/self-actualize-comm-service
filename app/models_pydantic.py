from pydantic import BaseModel, constr
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID

"""
Models for Pydantic validation

MessageRequest: Request model for sending messages
MessageResponse: Response model for receiving messages response
MessageLogResponse: Response model for receiving message logs response
"""

class MessageRequest(BaseModel):
    channel_type: Literal['email', 'sms']
    recipient: str
    content: str

class MessageResponse(BaseModel):
    id: UUID
    channel_type: Literal['email', 'sms']
    recipient: str
    content: str
    created_at: datetime
    
    # Helps map Pydantic model to SQLAlchemy model
    model_config = {
        'from_attributes': True
    }

class MessageLogResponse(BaseModel):
    id: UUID
    message_id: UUID
    delivery_status: str
    created_at: datetime
    logged_at: datetime
    error_message: Optional[str] = None
    provider_response: Optional[str] = None
    
    # Helps map Pydantic model to SQLAlchemy model
    model_config = {
        'from_attributes': True
    }
