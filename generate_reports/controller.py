from fastapi import APIRouter
from fastapi import HTTPException, Depends, Response
from generate_reports import utils, schema
from user import utils as user_utils
from config import security
from sqlalchemy.orm import Session
from config.database import SessionLocal
import json
from datetime import datetime

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
    try:
        user = user_utils.get_user(db=db, user_id=current_user_id.id)

        if (user.role.name == 'hr') or (user.role.name == 'admin'):
            staff = user_utils.get_user_by_email(db=db, email=report_request.user_email)
            staff_messages = staff.sent_messages

            if report_request.date_range:
                start_date = datetime.strptime(report_request.date_range.split(':')[0], '%Y-%m-%d')
                end_date = datetime.strptime(report_request.date_range.split(':')[1]+' 23:59:59', '%Y-%m-%d %H:%M:%S')
                
                staff_messages = [message for message in staff_messages 
                                  if message.created_at >= start_date and 
                                  message.created_at <= end_date]

            message_groupings = dict()
            for message in staff_messages:
                message_groupings.setdefault(message.label, []).append(schema.ReturnReport.to_dict(message=message).model_dump())

            return Response(status_code=200, content=json.dumps(message_groupings))
        else:
            raise HTTPException(status_code=401, detail=json.dumps({'message':'Unauthorized to view report. Must be hr or admin'}))

    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))