from pydantic import BaseModel, constr
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID

# Request Models
class MessageRequest(BaseModel):
    channel_type: Literal['email', 'sms']
    recipient: str
    content: str

class MessageResponse(BaseModel):
    message_id: UUID
    status: str

class MessageLogResponse(BaseModel):
    delivery_status: str
    timestamp: datetime
    error_message: Optional[str] = None
    
    model_config = {
        'from_attributes': True  # For SQLAlchemy compatibility
    }
