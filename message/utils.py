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