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
    text = Column(String, nullable=False)
    document = Column(String, nullable=True)
    
    sender = relationship("User", back_populates="sent_messages")
    recipient = relationship("User", back_populates="received_messages")
    comments = relationship("Comment", back_populates="message")

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    message_id = Column(Integer, ForeignKey("messages.id"))

    message = relationship("Message", back_populates="comments")
