from fastapi import APIRouter
from fastapi import HTTPException, Depends, Response
from user import utils, model, schema
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

@router.get("/users")
async def users():
    return {"message": "Users App"}


@router.post('/signup')
async def signup(user: schema.CreateUser, db: Session = Depends(get_db)):
    try:
        if utils.get_user_by_email(email=user.username, db=db) is not None:
            raise HTTPException(status_code=400, detail="email already registered")

        db_user = utils.create_user(user=user, db=db)
        user_dict = schema.BaseUser.to_dict(db_user).model_dump()
        return Response(status_code=201, content=json.dumps({'message':'user created successfully', 'details':user_dict}))
    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))