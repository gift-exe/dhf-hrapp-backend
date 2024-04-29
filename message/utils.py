from sqlalchemy.orm import Session
from message import model
from message import schema
from typing import List
from user import utils as user_utils

def create_message(db: Session, recipients:List[str], message: schema.CreateMessage):
    try:
        result = model.Message(sender_id=message.sender_id, 
                            label=message.label, 
                            title=message.title, 
                            text=message.text, 
                            document=message.document, 
                            type=message.type,
                            status=message.status)
        
        for recipient in recipients:
            result.recipients.append(user_utils.get_user_by_email(email=recipient, db=db))
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        raise e
    
def get_message(db: Session, message_id):
    try:
        message = db.query(model.Message).filter(model.Message.id == message_id).first()
        return message
    except Exception as e:
        raise e
def create_comment(db: Session, comment: schema.CreateComment, sender_id):
    
    try:
        result = model.Comment(text=comment.text,
                               message_id=comment.message_id,
                               sender_id=sender_id)
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        raise e
    
def get_leave_requests(db: Session):
    try:
        leave_requests = db.query(model.Message).filter(model.Message.type == 'request_leave')
        return leave_requests
    except Exception as e:
        raise e