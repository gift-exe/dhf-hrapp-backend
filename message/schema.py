from typing import Optional, BinaryIO, TextIO
from pydantic import BaseModel
from message.model import Message as MMessage
from message.model import Comment as MComment
from fastapi import UploadFile
from sqlalchemy.orm import Session
from user import utils as user_utils

class RequestMessage(BaseModel):
    title: str
    label: str
    document: Optional[TextIO] = None
    recipient: str
    text: Optional[str] = None

    class Config:
        arbitrary_types_allowed=True

class CreateMessage(BaseModel):
    sender_id: int
    recipient_id: int
    label: str
    title: str
    text: Optional[str] = None
    document: Optional[str] = None
    status: str
    type: str

class ReturnMessage(BaseModel):
    message_id: int
    sender: str
    recipient: str
    label: str
    title: str
    text: Optional[str] = None
    document: Optional[str] = None
    status: str = None

    @classmethod
    def to_dict(cls, msg:MMessage, db:Session) -> "ReturnMessage":
        return cls (
            message_id=msg.id, 
            sender=f"{user_utils.get_user(db=db, user_id=msg.sender_id).first_name} {user_utils.get_user(db=db, user_id=msg.sender_id).last_name}", 
            recipient=f"{user_utils.get_user(db=db, user_id=msg.recipient_id).first_name} {user_utils.get_user(db=db, user_id=msg.recipient_id).last_name}",
            label=msg.label,
            title=msg.title,
            text=msg.text,
            document=msg.document,
            status=msg.status
        )
