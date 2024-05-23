from sqlalchemy import String, Column, DateTime, func, BigInteger, Time, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from message.model import (message_recipients_association, 
                           evaluation_recipients_association,
                           early_closure_recipients_association,
                           study_leave_recipients_association)

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
    role_id = Column(BigInteger, ForeignKey('offices.id', ondelete='CASCADE'))
    resumption_time = Column(Time, nullable=True)
    closing_time = Column(Time, nullable=True)
    
    sent_messages = relationship("Message", back_populates="sender", foreign_keys="[Message.sender_id]", cascade="all, delete-orphan")
    sent_early_closures = relationship("EarlyClosure", back_populates="sender", foreign_keys="[EarlyClosure.sender_id]", cascade="all, delete-orphan")
    sent_study_leaves = relationship("StudyLeave", back_populates="sender", foreign_keys="[StudyLeave.sender_id]", cascade="all, delete-orphan")
    sent_evaluations = relationship("Evaluation", back_populates="sender", foreign_keys="[Evaluation.sender_id]", cascade="all, delete-orphan")

    received_messages = relationship("Message", back_populates="recipients", secondary=message_recipients_association)
    received_evaluations = relationship("Evaluation", back_populates="recipients", secondary=evaluation_recipients_association)
    received_early_closures = relationship("EarlyClosure", back_populates="recipients", secondary=early_closure_recipients_association)
    received_study_leaves = relationship("StudyLeave", back_populates="recipients", secondary=study_leave_recipients_association)

    role = relationship("Office", back_populates="staff")
    department_head = relationship('OfficeHead', back_populates='user', cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="sender", foreign_keys="[Comment.sender_id]", cascade="all, delete-orphan")
