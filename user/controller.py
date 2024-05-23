from fastapi import APIRouter
from fastapi import HTTPException, Depends, Response
from user import utils, schema, model
from config import security
from sqlalchemy.orm import Session
from config.database import SessionLocal
import json
from datetime import time
from office import utils as office_utils
from sqlalchemy import func

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

@router.get('/get-users')
async def get_users(db: Session = Depends(get_db),
                    current_user_id = Depends(security.get_current_user)):
    try:
        db_users = utils.get_users(db=db, user_id=current_user_id.id)
        users = [schema.User.to_dict(db_item=user).model_dump() for user in db_users]
        
        return Response(status_code=200, content=json.dumps(users))
    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))

@router.patch('/edit-user-role')
async def edit_role(data: schema.EditUserRole,
                    db:Session = Depends(get_db),
                    current_user_id = Depends(security.get_current_user)
):
    try:
        user = utils.get_user(db=db, user_id=current_user_id.id)
        if user.role.name not in ['admin', 'hr']:
            raise HTTPException(status_code=401, detail=json.dumps({'message':'Unauthorized. Must be Hr or Admin'}))

        edit_user = utils.get_user(db=db, user_id=data.user_id)
        edit_user.role = office_utils.get_office_by_name(db=db, name=data.role)
        
        user.updated_at = func.now()
        db.commit()

        # TODO: Notify user or take any other necessary action
        return Response(status_code=200, content=json.dumps({'message':'User Data Updated Successfully'}))

    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occurred', 'error': str(e)}))

@router.patch('/edit-user-details')
async def edit_data(edit_user: schema.EditUser,
                    db:Session = Depends(get_db),
                    current_user_id = Depends(security.get_current_user)):
    try:
        l_user = utils.get_user(db=db, user_id=current_user_id.id)
        if l_user.role.name not in ['admin', 'hr']:
            raise HTTPException(status_code=401, detail=json.dumps({'message':'Unauthorized. Must be Hr or Admin'}))

        user = utils.get_user(db=db, user_id=edit_user.user_id)
        if edit_user.first_name is not None:
            user.first_name = edit_user.first_name
        if edit_user.last_name is not None:
            user.last_name = edit_user.last_name
        if edit_user.email is not None:
            user.email = edit_user.email
        if edit_user.phone is not None:
            user.phone = edit_user.phone
        if edit_user.role is not None:
            user.role_id = office_utils.get_office_by_name(db=db, name=edit_user.role).id
        
        user.updated_at = func.now()

        db.commit()

        # TODO: Notify user or take any other necessary action
        return Response(status_code=200, content=json.dumps({'message':'User Role Updated Successfully'}))

    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occurred', 'error': str(e)}))

@router.delete('/user')
async def delete_user(data: schema.DeleteUser,
                    db:Session = Depends(get_db),
                    current_user_id = Depends(security.get_current_user)):
    try:
        user = utils.get_user(db=db, user_id=current_user_id.id)
        if user.role.name not in ['admin', 'hr']:
            raise HTTPException(status_code=401, detail=json.dumps({'message':'Unauthorized. Must be Hr or Admin'}))

        del_user = db.query(model.User).filter(model.User.id == data.user_id).first()

        db.delete(del_user)
        db.commit()

        # TODO: Notify user or take any other necessary action
        return Response(status_code=200, content=json.dumps({'message':'User Deleted Successfully'}))

    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occurred', 'error': str(e)}))
