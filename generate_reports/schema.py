from typing import Optional, List
from pydantic import BaseModel
from message.model import Message as MMessage
from message.model import Comment as MComment
from sqlalchemy.orm import Session
from user import utils as user_utils

class RequestReport(BaseModel):
    user_email: str

