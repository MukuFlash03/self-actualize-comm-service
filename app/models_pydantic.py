from pydantic import BaseModel, constr
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID

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
    
    model_config = {
        'from_attributes': True  # For SQLAlchemy compatibility
    }

class MessageLogResponse(BaseModel):
    id: UUID
    message_id: UUID
    delivery_status: str
    created_at: datetime
    logged_at: datetime
    error_message: Optional[str] = None
    provider_response: Optional[str] = None
    
    model_config = {
        'from_attributes': True  # For SQLAlchemy compatibility
    }
