from fastapi import APIRouter
from fastapi import HTTPException, Depends, Response
from office import utils, schema, model
from user import utils as user_utils
from user import schema as user_schema
from config import security
from sqlalchemy.orm import Session
from config.database import SessionLocal
import json

router = APIRouter()

def get_db():
    db =  SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/register-office/')
async def register_office(
    office: schema.Office,
    db: Session = Depends(get_db), 
    current_user_id = Depends(security.get_current_user)):
    try:
        current_user = user_utils.get_user(db=db, user_id=current_user_id.id)
        
        if (current_user.role.name == 'admin') or (current_user.role.name == 'hr'):
            if utils.get_office_by_name(db=db, name=office.name) is not None:
                raise HTTPException(status_code=400, detail='office already exists')
            
            db_office = utils.create_office(db=db, office=office)
            office_dict = schema.GetOffice.to_dict(db_office).model_dump()
            
            return Response(status_code=201, content=json.dumps({'message':'office created successfully', 'details':office_dict}))
        
        else:
            raise HTTPException(status_code=401, detail="Not authorized to create an office. must be an admin or hr staff")
    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))

@router.post('/assign-hofo/')
async def assign_hofo(
    assign_hofo: schema.CreateHofoO,
    db: Session = Depends(get_db), 
    current_user_id = Depends(security.get_current_user)
    ):
    try:
        current_user = user_utils.get_user(db=db, user_id=current_user_id.id)

        if (current_user.role.name == 'admin') or (current_user.role.name == 'hr'):
            if utils.get_office_by_name(db=db, name=assign_hofo.office_name) is None:
                raise HTTPException(status_code=400, detail='office does not exists')
            
            if user_utils.get_user_by_email(db=db, email=assign_hofo.email) is None:
                raise HTTPException(status_code=400, detail='user does not exists')
            
            db_hofo = utils.assign_hofo(db=db, assignhofo=assign_hofo)

            hofo_dict = schema.GetHofO.to_dict(db_item=db_hofo).model_dump()

            return Response(status_code=201, content=json.dumps({'message':'office head assigned successfully', 'details':hofo_dict}))
        
        else:
            raise HTTPException(status_code=401, detail="Not authorized to assign head of office. must be an admin or hr staff")
    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))