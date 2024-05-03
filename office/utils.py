from sqlalchemy.orm import Session
from office import model, schema
from user import utils as user_utils
from config import security

def get_office_by_name(db: Session, name: str):
    try:
        office = db.query(model.Office).filter(model.Office.name == name).first()
        return office
    except Exception as e:
        raise e

def create_office(db: Session, office: schema.Office):
    try:
        result = model.Office(name=office.name)
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        raise e

def assign_hofo(db: Session, assignhofo: schema.CreateHofoO):
    try:
        result = model.OfficeHead(office_id=get_office_by_name(db=db, name=assignhofo.office_name).id,
                                  user_id=user_utils.get_user_by_email(db=db, email=assignhofo.email).id)
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        raise e

