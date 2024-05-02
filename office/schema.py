from pydantic import BaseModel
from office.model import Office as MOffice
from office.model import OfficeHead as MOfficeHead
from office import utils
from typing import Optional
from user import utils as user_utils
from sqlalchemy.orm import Session
from datetime import datetime

class Office(BaseModel):
    name: str

class GetOffice(Office):
    id: int
    created_at: datetime
    last_update: datetime

    @classmethod
    def to_dict(cls, db_item: MOffice) -> "Office":
        return cls(
            id = db_item.id,
            name = db_item.name,
            created_at = db_item.created_at,
            last_update = db_item.updated_at
        )

class CreateHofoO(BaseModel):
    office_name: str
    email: str

class GetHofO(BaseModel):
    office_name: str
    head_email: str
    created_at: datetime
    last_update: datetime

    @classmethod
    def to_dict(cls, db_item: MOfficeHead) -> "Office":
        return cls(
            office_name = db_item.office.name,
            head_email = db_item.user.name,
            created_at = db_item.created_at,
            last_update = db_item.updated_at
        )


