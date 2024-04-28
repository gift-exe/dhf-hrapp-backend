from sqlalchemy import String, Column, DateTime, func, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from config.database import Base

message_recipients_association = Table(
    'message_recipients_association',
    Base.metadata,
    Column('message_id', Integer, ForeignKey('messages.id')),
    Column('recipient_id', Integer, ForeignKey('users.id')),
    Column('created_at', DateTime, nullable=False, default=func.now()),
    Column('updated_at', DateTime, nullable=False, default=func.now()),

)
class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    label = Column(String, nullable=False)
    title = Column(String, nullable=False)
    text = Column(String, nullable=True)
    document = Column(String, nullable=True)
    type = Column(String)
    status = Column(String, nullable=False, default='pending')
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())
    
    sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    recipients = relationship("User", back_populates="received_messages", secondary=message_recipients_association)

    comments = relationship("Comment", back_populates="message", foreign_keys="[Comment.message_id]")

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    message_id = Column(Integer, ForeignKey("messages.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    message = relationship("Message", back_populates="comments", foreign_keys=[message_id])
    sender = relationship("User", back_populates="comments", foreign_keys=[sender_id])
