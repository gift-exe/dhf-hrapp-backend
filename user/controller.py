from fastapi import APIRouter
from fastapi import HTTPException, Depends, Response
from user import utils, schema
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

@router.post('/signup/')
async def signup(user: schema.CreateUser, db: Session = Depends(get_db), current_user_id = Depends(security.get_current_user)):
    try:
        current_user = utils.get_user(db=db, user_id=current_user_id.id)
        
        if (current_user.role.name == 'admin') or (current_user.role.name == 'hr'):

            if utils.get_user_by_email(email=user.email, db=db) is not None:
                raise HTTPException(status_code=400, detail="email already registered")
            
            if user.resumption_time and user.closing_time:
                user.resumption_time = time(hour=int(user.resumption_time.split(':')[0]), minute=int(user.resumption_time.split(':')[1]))
                user.closing_time = time(hour=int(user.closing_time.split(':')[0]), minute=int(user.closing_time.split(':')[1]))

                print(user.closing_time, type(user.closing_time))

            db_user = utils.create_user(user=user, db=db)
        
            user_dict = schema.BaseUser.to_dict(db_user).model_dump()
            return Response(status_code=201, content=json.dumps({'message':'user created successfully', 'details':user_dict}))
        
        else:
            raise HTTPException(status_code=401, detail="Not authorized to create a user. must be an admin or hr staff")
    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))

@router.post('/login/')
async def login(creds: schema.Login, db: Session = Depends(get_db)):
    try:
        user = utils.get_user_by_email(email=creds.email, db=db)
        
        if not user:
            raise HTTPException(status_code=400, detail="User does not exist")
        
        if not security.verify_hash(plain_text=creds.password, hashed_password=user.password):
            raise HTTPException(status_code=400, detail="Invalid Credentials")
        
        token = security.generate_access_token(data={'user_id': user.id})
        
        return {'status': True, 'user_details':schema.User.to_dict(user).model_dump(), 'access_token': token, 'token_type': 'bearer'}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))
    
@router.post('/reset-password/')
async def reset_password(password_change: schema.PasswordChange, 
                         db: Session = Depends(get_db), 
                         current_user_id = Depends(security.get_current_user)):
    user = utils.get_user(db=db, user_id=current_user_id.id)

    #TODO:This
    return {'message': 'will implement later'}
    

@router.put('/set-working-period')
async def set_working_period(work_period: schema.WorkPeriod, 
                             db: Session = Depends(get_db), 
                             current_user_id = Depends(security.get_current_user)):
    try:
        current_user = utils.get_user(db=db, user_id=current_user_id.id)
        
        if (current_user.role.name == 'admin') or (current_user.role.name == 'hr'):
            user = utils.get_user(db=db, user_id=work_period.user_id)
            start_time = work_period.start_time
            end_time = work_period.end_time

            user.resumption_time = time(hour=int(start_time.split(':')[0]), minute=int(start_time.split(':')[1]))
            user.closing_time = time(hour=int(end_time.split(':')[0]), minute=int(end_time.split(':')[1]))

            db.commit()
            db.refresh(user)

            user_dict = schema.BaseUser.to_dict(user).model_dump()
            return Response(status_code=201, content=json.dumps({'message':'user working period updated successfully', 'details':user_dict}))

        else:
            raise HTTPException(status_code=401, detail="Not authorized to define working hours. must be an admin or hr staff")
    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))