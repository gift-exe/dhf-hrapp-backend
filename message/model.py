from sqlalchemy import String, Column, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"))
    label = Column(String, nullable=False)
    title = Column(String, nullable=False)
    text = Column(String, nullable=True)
    document = Column(String, nullable=True)
    type = Column(String)
    status = Column(String, nullable=False, default='pending')
    
    sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    recipient = relationship("User", back_populates="received_messages", foreign_keys=[recipient_id])
    comments = relationship("Comment", back_populates="message", foreign_keys="[Comment.message_id]")

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    message_id = Column(Integer, ForeignKey("messages.id"))

    message = relationship("Message", back_populates="comments", foreign_keys=[message_id])
