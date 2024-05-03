from typing import Optional, List
from pydantic import BaseModel
from message.model import Message as MMessage
from message.model import Comment as MComment
from sqlalchemy.orm import Session
from user import utils as user_utils

class RequestReport(BaseModel):
    user_email: str
    date_range: Optional[str] = None

class ReturnReport(BaseModel):
    created_at: str
    recipients: List[str]
    document: Optional[str] = None
    status: Optional[str] = None

    @classmethod
    def to_dict(cls, message: MMessage) -> 'RequestReport':
        recipients = [f'{r.first_name} {r.last_name}' for r in message.recipients]
        return cls(
            created_at = message.created_at.isoformat(),
            recipients = recipients,
            document = message.document,
            status = message.status
        )