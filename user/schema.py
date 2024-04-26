from typing import Optional
from pydantic import BaseModel
from user.model import User as MUser

class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    role: str

    class Config:
        from_attributes = True

    @classmethod
    def to_dict(cls, db_item: MUser) -> "BaseUser":
        return cls (
            first_name = db_item.first_name,
            last_name = db_item.last_name,
            email = db_item.email,
            phone = db_item.phone,
            role = db_item.role
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
            role = db_item.role
        )
    
class TokenData(BaseModel):
    id: int

class Login(BaseModel):
    email: str
    password: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str