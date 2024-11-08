from datetime import datetime
import uuid
from sqlalchemy import Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app import db

"""
SQLAlchemy models for handling messages and message logs.

This module defines two main models:
- Message: Represents a message to be sent via email or SMS
- MessageLog: Tracks the delivery status and related info for each message
"""

class Message(db.Model):
    # SQLAlchemy model for messages table
    __tablename__ = 'messages'

    # Columns for the messages table
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_type = db.Column(Enum('email', 'sms', name='channel_type'), nullable=False)
    recipient = db.Column(db.String(255), nullable=False)
    content = db.Column(Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    
    # Foreign key relationships with MessageLog table
    logs = relationship("MessageLog", back_populates="message")

    """
    Return string representation of Message object.
    Helpful for debugging and logging.
    """
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
    # SQLAlchemy model for message logs table
    __tablename__ = 'message_logs'

    # Columns for the message logs table
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = db.Column(UUID(as_uuid=True), db.ForeignKey('messages.id'), nullable=False)
    delivery_status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    logged_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    error_message = db.Column(Text)
    provider_response = db.Column(Text) 

    # Foreign key relationship with Message table
    message = relationship("Message", back_populates="logs")
    
    """
    Return string representation of MessageLog object.
    Helpful for debugging and logging.
    """
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
