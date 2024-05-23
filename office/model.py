
from sqlalchemy import String, Column, DateTime, BigInteger, ForeignKey, func
from sqlalchemy.orm import relationship

from config.database import Base

class Office(Base):
    #STAFF, HOS, ADMIN, HR
    __tablename__ = 'offices'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    staff = relationship('User', back_populates='role')
    office_head = relationship('OfficeHead', back_populates='office', cascade="all, delete-orphan")

class OfficeHead(Base):
    __tablename__ = 'office_heads'
    
    id = Column(BigInteger, primary_key=True)

    office_id = Column(BigInteger, ForeignKey('offices.id', ondelete='CASCADE'), unique=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    office = relationship('Office', back_populates='office_head')
    user = relationship('User', back_populates='department_head')
    
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())
