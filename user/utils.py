from sqlalchemy.orm import Session
from user import model
from user import schema
from config import security
from office import utils as office_utils


def get_user(db: Session, user_id):
    try:
        user = db.query(model.User).filter(model.User.id == user_id).first()
        return user
    except Exception as e:
        raise e

def create_user(db: Session, user: schema.CreateUser):
    try:
        hash_password = security.hash_string(user.password)
        result = model.User(first_name = user.first_name, 
                            last_name = user.last_name, 
                            email = user.email, 
                            password = hash_password, 
                            phone = user.phone, 
                            role_id=office_utils.get_office_by_name(db=db, name=user.role).id,
                            resumption_time=user.resumption_time,
                            closing_time=user.closing_time)
        db.add(result)
        db.commit()
        db.refresh(result)
        
        return result
    except Exception as e:
        raise e

def get_user_by_email(db: Session, email: str):
    try:
        db_user = db.query(model.User).filter(model.User.email == email).first()
        
        return db_user
    except Exception as e:
        raise e

def change_password(db: Session, password: str, id):
    try:
        hash_password = security.hash_string(password)
        result = db.query(model.User).filter(model.User.id == id)
        result.update({'password': hash_password}, synchronize_session = False)
        db.commit()
        result.first()
        return True
    except Exception as e:
        raise e
