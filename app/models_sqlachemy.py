from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
	pass

class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_type = Column(Enum('email', 'sms', name='channel_type'), nullable=False)
    recipient = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
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

class MessageLog(Base):
    __tablename__ = 'message_logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey('messages.id'), nullable=False)
    delivery_status = Column(String(20), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    error_message = Column(Text)

    message = relationship("Message", back_populates="logs")
    
    def __repr__(self) -> str:
        return (
			'<MessageLog (id={0}, '
			'message_id={1}, '
			'delivery_status={2}, '
			'timestamp={3}, '
			'error_message={4}>'
			.format(
				self.id,
				self.message_id,
				self.delivery_status,
				self.timestamp,
				self.error_message
			)
		)
