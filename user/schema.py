from typing import Optional
from pydantic import BaseModel
from user.model import User as MUser
from datetime import time

class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    role: str
    resumption_time: Optional[str|time] = None
    closing_time: Optional[str|time] = None

    class Config:
        from_attributes = True

    @classmethod
    def to_dict(cls, db_item: MUser) -> "BaseUser":
        return cls (
            first_name = db_item.first_name,
            last_name = db_item.last_name,
            email = db_item.email,
            phone = db_item.phone,
            role = db_item.role.name,
            resumption_time = db_item.resumption_time.isoformat() if db_item.resumption_time is not None else None,
            closing_time = db_item.closing_time.isoformat() if db_item.closing_time is not None else None
        )

class CreateUser(BaseUser):
    password: str

class User(BaseUser):
    id: int

    @classmethod
    def to_dict(cls, db_item: MUser) -> "User":
        return cls (
            id = db_item.id,
            first_name = db_item.first_name,
            last_name = db_item.last_name,
            email = db_item.email,
            phone = db_item.phone,
            role = db_item.role.name,
            resumption_time = db_item.resumption_time.isoformat() if db_item.resumption_time is not None else None,
            closing_time = db_item.closing_time.isoformat() if db_item.closing_time is not None else None
        )
    
class TokenData(BaseModel):
    id: int

class Login(BaseModel):
    email: str
    password: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

class WorkPeriod(BaseModel):
    user_id: int
    start_time: str
    end_time: str

class GetUsers(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    role: str

    @classmethod
    def to_dict(cls, user):
        return cls(
            user_id = user.id,
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email,
            role = user.role.name
        )
    
class EditUser(BaseModel):
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[int] = None

    class Config:
        orm_mode = True

class EditUserRole(BaseModel):
    user_id: int
    role: str

    class Config:
        orm_mode = True

class DeleteUser(BaseModel):
    user_id: int