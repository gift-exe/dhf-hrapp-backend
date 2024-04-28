from typing import Optional, List
from pydantic import BaseModel
from message.model import Message as MMessage
from message.model import Comment as MComment
from fastapi import UploadFile
from sqlalchemy.orm import Session
from user import utils as user_utils

class CreateComment(BaseModel):
    text: str
    message_id: int


class CreateMessage(BaseModel):
    sender_id: int
    label: str
    title: str
    text: Optional[str] = None
    document: Optional[str] = None
    status: str
    type: str

class ReturnMessage(BaseModel):
    message_id: int
    sender: str
    recipients: List[str]
    label: str
    title: str
    text: Optional[str] = None
    document: Optional[str] = None
    status: str = None
    comments: List[dict] = []

    @classmethod
    def to_dict(cls, msg:MMessage, comments:MComment, db:Session) -> "ReturnMessage":
        recipients = [f'{r.first_name} {r.last_name}' for r in msg.recipients]
        return cls (
            message_id=msg.id, 
            sender=f"{user_utils.get_user(db=db, user_id=msg.sender_id).first_name} {user_utils.get_user(db=db, user_id=msg.sender_id).last_name}", 
            recipients=recipients,
            label=msg.label,
            title=msg.title,
            text=msg.text,
            document=msg.document,
            status=msg.status,
            comments = [{'comments_id':comment.id, 
                         'text':comment.text, 
                         'sender':f'{user_utils.get_user(db=db, user_id=comment.sender_id).first_name} {user_utils.get_user(db=db, user_id=comment.sender_id).last_name}'} 
                        for comment in comments]
        )

class LeaveResponse(BaseModel):
    message_id: int
    status: str
