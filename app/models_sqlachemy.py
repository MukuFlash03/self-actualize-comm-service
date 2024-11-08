from datetime import datetime
import uuid
from sqlalchemy import Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app import db

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_type = db.Column(Enum('email', 'sms', name='channel_type'), nullable=False)
    recipient = db.Column(db.String(255), nullable=False)
    content = db.Column(Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    
    logs = relationship("MessageLog", back_populates="message")

    def __repr__(self) -> str:
        return (
            '<Message (id={0}, '
            'channel_type={1}, '
            'recipient={2}, '
            'content={3}, '
            'created_at={4}>'
            .format(
                self.id,
                self.channel_type,
                self.recipient,
                self.content,
                self.created_at
            )
        )

class MessageLog(db.Model):
    __tablename__ = 'message_logs'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = db.Column(UUID(as_uuid=True), db.ForeignKey('messages.id'), nullable=False)
    delivery_status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    logged_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    error_message = db.Column(Text)
    provider_response = db.Column(Text) 

    message = relationship("Message", back_populates="logs")
    
    def __repr__(self) -> str:
        return (
            '<MessageLog (id={0}, '
            'message_id={1}, '
            'delivery_status={2}, '
            'logged_at={3}, '
            'error_message={4}>'
            'provider_response={5}>'
            .format(
                self.id,
                self.message_id,
                self.delivery_status,
                self.logged_at,
                self.error_message,
                self.provider_response
            )
        )
