from fastapi import APIRouter
from fastapi import HTTPException, Depends, Response
from user import utils, schema
from config import security
from sqlalchemy.orm import Session
from config.database import SessionLocal
import json

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/signup/')
async def signup(user: schema.CreateUser, db: Session = Depends(get_db)):
    try:
        if utils.get_user_by_email(email=user.email, db=db) is not None:
            raise HTTPException(status_code=400, detail="email already registered")

        db_user = utils.create_user(user=user, db=db)
    
        user_dict = schema.BaseUser.to_dict(db_user).model_dump()
        return Response(status_code=201, content=json.dumps({'message':'user created successfully', 'details':user_dict}))
    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))

@router.post('/login/')
async def login(creds: schema.Login, db: Session = Depends(get_db)):
    #try:
        user = utils.get_user_by_email(email=creds.email, db=db)
        print(f'user: {user}')
        if not user:
            raise HTTPException(status_code=400, detail="User does not exist")
        
        if not security.verify_hash(plain_text=creds.password, hashed_password=user.password):
            raise HTTPException(status_code=400, detail="Invalid Credentials")
        
        token = security.generate_access_token(data={'user_id': user.id})
        
        return {'status': True, 'user_details':schema.User.to_dict(user).model_dump(), 'access_token': token, 'token_type': 'bearer'}
    
    #except Exception as e:
    #    raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))
    
@router.post('/reset-password/')
async def reset_password(password_change: schema.PasswordChange, db: Session = Depends(get_db), current_user_id = Depends(security.get_current_user)):
    user = utils.get_user(db=db, user_id=current_user_id.id)

    #TODO:This
    return {'message': 'will implement later'}
    

    