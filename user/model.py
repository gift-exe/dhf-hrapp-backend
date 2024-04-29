from sqlalchemy import String, Column, DateTime, func, BigInteger, Time
from sqlalchemy.orm import relationship
from config.database import Base
from message.model import message_recipients_association

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())
    role = Column(String) #STAFF, HOS, ADMIN, HR
    resumption_time = Column(Time, nullable=True)
    closing_time = Column(Time, nullable=True)
    
    sent_messages = relationship("Message", back_populates="sender", foreign_keys="[Message.sender_id]")
    received_messages = relationship("Message", back_populates="recipients", secondary=message_recipients_association)

    comments = relationship("Comment", back_populates="sender", foreign_keys="[Comment.sender_id]")


