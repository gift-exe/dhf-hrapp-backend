from sqlalchemy.orm import Session
from message import model
from message import schema

def create_message(db: Session, message: schema.CreateMessage):
    try:
        result = model.Message(sender_id=message.sender_id, 
                            recipient_id=message.recipient_id, 
                            label=message.label, 
                            title=message.title, 
                            text=message.text, 
                            document=message.document, 
                            type=message.type,
                            status=message.status)
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