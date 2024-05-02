
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

class OfficeHead(Base):
    __tablename__ = 'office_heads'

    office_id = Column(BigInteger, ForeignKey('offices.id'), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    office = relationship('Office', backref='head')
    user = relationship('User', backref='department_head')
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())