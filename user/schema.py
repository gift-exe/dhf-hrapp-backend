from typing import Optional
from pydantic import BaseModel
from model import User as MUser

class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: int
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
    
class TokenData(BaseModel):
    id: str

    @classmethod
    def to_dict(cls, db_item: MUser) -> "User":
        base_user_dict = super().to_dict(db_item)
        user_dict = {
            **base_user_dict,
            "id": db_item.id
        }
        return user_dict