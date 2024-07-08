from fastapi import APIRouter
from fastapi import HTTPException, Depends, Response
from generate_reports import utils, schema
from user import utils as user_utils
from config import security
from sqlalchemy.orm import Session
from config.database import SessionLocal
import json
from datetime import datetime
from message.model import Message, EarlyClosure, StudyLeave, Evaluation
from typing import List

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/messages')
async def generate_report(report_request: schema.RequestReport,
                           db: Session = Depends(get_db), 
                           current_user_id = Depends(security.get_current_user)):
    try:
        user = user_utils.get_user(db=db, user_id=current_user_id.id)

        if (user.role.name == 'hr') or (user.role.name == 'admin'):

            if report_request.date_range:
                start_date = datetime.strptime(report_request.date_range.split(':')[0], '%Y-%m-%d')
                end_date = datetime.strptime(report_request.date_range.split(':')[1]+' 23:59:59', '%Y-%m-%d %H:%M:%S')
            else:
                raise HTTPException(status_code=400, detail=json.dumps({'message':'Date Range is needed'}))

            messages = db.query(Message).filter(Message.created_at >= start_date, Message.created_at <= end_date).all()
            return Response(content=json.dumps([schema.MessageBase.to_dict(message=message).model_dump() for message in messages]))
        else:
            raise HTTPException(status_code=401, detail=json.dumps({'message':'Unauthorized to view report. Must be hr or admin'}))

    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))
    
@router.post('/early-closures')
async def generate_report(report_request: schema.RequestReport,
                           db: Session = Depends(get_db), 
                           current_user_id = Depends(security.get_current_user)):
    try:
        user = user_utils.get_user(db=db, user_id=current_user_id.id)

        if (user.role.name == 'hr') or (user.role.name == 'admin'):

            if report_request.date_range:
                start_date = datetime.strptime(report_request.date_range.split(':')[0], '%Y-%m-%d')
                end_date = datetime.strptime(report_request.date_range.split(':')[1]+' 23:59:59', '%Y-%m-%d %H:%M:%S')
            else:
                raise HTTPException(status_code=400, detail=json.dumps({'message':'Date Range is needed'}))

            messages = db.query(EarlyClosure).filter(EarlyClosure.created_at >= start_date, EarlyClosure.created_at <= end_date).all()
            return Response(content=json.dumps([schema.EarlyClosureBase.to_dict(early_closure=message).model_dump() for message in messages]))
        else:
            raise HTTPException(status_code=401, detail=json.dumps({'message':'Unauthorized to view report. Must be hr or admin'}))

    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))

@router.post('/study-leaves')
async def generate_report(report_request: schema.RequestReport,
                           db: Session = Depends(get_db), 
                           current_user_id = Depends(security.get_current_user)):
    try:
        user = user_utils.get_user(db=db, user_id=current_user_id.id)

        if (user.role.name == 'hr') or (user.role.name == 'admin'):

            if report_request.date_range:
                start_date = datetime.strptime(report_request.date_range.split(':')[0], '%Y-%m-%d')
                end_date = datetime.strptime(report_request.date_range.split(':')[1]+' 23:59:59', '%Y-%m-%d %H:%M:%S')
            else:
                raise HTTPException(status_code=400, detail=json.dumps({'message':'Date Range is needed'}))

            messages = db.query(StudyLeave).filter(StudyLeave.created_at >= start_date, StudyLeave.created_at <= end_date).all()
            return Response(content=json.dumps([schema.StudyLeaveBase.to_dict(study_leave=message).model_dump() for message in messages]))
        else:
            raise HTTPException(status_code=401, detail=json.dumps({'message':'Unauthorized to view report. Must be hr or admin'}))

    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))

@router.post('/evaluations')
async def generate_report(report_request: schema.RequestReport,
                           db: Session = Depends(get_db), 
                           current_user_id = Depends(security.get_current_user)):
    try:
        user = user_utils.get_user(db=db, user_id=current_user_id.id)

        if (user.role.name == 'hr') or (user.role.name == 'admin'):

            if report_request.date_range:
                start_date = datetime.strptime(report_request.date_range.split(':')[0], '%Y-%m-%d')
                end_date = datetime.strptime(report_request.date_range.split(':')[1]+' 23:59:59', '%Y-%m-%d %H:%M:%S')
            else:
                raise HTTPException(status_code=400, detail=json.dumps({'message':'Date Range is needed'}))

            messages = db.query(Evaluation).filter(Evaluation.created_at >= start_date, Evaluation.created_at <= end_date).all()
            return Response(content=json.dumps([schema.EvaluationBase.to_dict(evaluation=message).model_dump() for message in messages]))
        else:
            raise HTTPException(status_code=401, detail=json.dumps({'message':'Unauthorized to view report. Must be hr or admin'}))

    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))