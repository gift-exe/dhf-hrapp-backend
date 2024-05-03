from fastapi import APIRouter
from fastapi import HTTPException, Depends, Response
from generate_reports import utils, schema
from user import utils as user_utils
from config import security
from sqlalchemy.orm import Session
from config.database import SessionLocal
import json
from datetime import time

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/')
async def generate_report(report_request: schema.RequestReport,
                           db: Session = Depends(get_db), 
                           current_user_id = Depends(security.get_current_user)):
    #leave of absence
    #informed late arrival
    #early closure
    #movement
    #TODO: Add timeline filter
    try:
        user = user_utils.get_user(db=db, user_id=current_user_id.id)

        if (user.role.name == 'hr') or (user.role.name == 'admin'):
            staff = user_utils.get_user_by_email(db=db, email=report_request.user_email)
            staff_messages = staff.sent_messages

            message_groupings = dict()
            for message in staff_messages:
                message_groupings.setdefault(message.label, []).append(message.created_at.isoformat())

            return Response(status_code=200, content=json.dumps(message_groupings))
        else:
            raise HTTPException(status_code=401, detail=json.dumps({'message':'Unauthorized to view report. Must be hr or admin'}))



    #so the logic is going to be simple. all we would do is 
    #get all the messages with this person_id as the sender id
    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))