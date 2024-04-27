from fastapi import APIRouter
from fastapi import HTTPException, Depends, Response
from user import utils as user_utils
from message import utils, schema, model
from config import security
from sqlalchemy.orm import Session
from config.database import SessionLocal
import json
from helpers.upload_helper import do_upload

from fastapi import Form, UploadFile
from typing import Annotated

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/upload-document/')
async def upload_document(document: UploadFile, 
                          title: Annotated[str, Form()], 
                          label: Annotated[str, Form()],
                          recipient: Annotated[str, Form()],
                          text: Annotated[str, Form()]=None,
                          db: Session = Depends(get_db), 
                          current_user_id = Depends(security.get_current_user)
                          ):
    try:
        user = user_utils.get_user(db=db, user_id=current_user_id.id)
        
        if document is None:
            raise HTTPException(status_code=400, detail=json.dumps({'message':'No document to upload'}))

        #upload document first
        doc_url = do_upload(document, user.email)

        #store details in db
        message_data = {'sender_id':user.id,
                        'recipient_id':user_utils.get_user_by_email(email=recipient, db=db).id,
                        'label':label,
                        'title':title,
                        'document':doc_url,
                        'text':text,
                        'type':'document_upload',
                        'status':'doc_upload'}
        message_schema = schema.CreateMessage(**message_data)
        db_message = utils.create_message(message=message_schema, db=db)

        #TODO: send notification to recipient ...
        return Response(status_code=200, content=json.dumps({'message':'Document sent successfully'}))

    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))

@router.post('/request-leave/')
async def request_leave(title: Annotated[str, Form()], 
                        label: Annotated[str, Form()],
                        recipient: Annotated[str, Form()],
                        text: Annotated[str, Form()]=None, 
                        document: UploadFile = None, 
                        db: Session = Depends(get_db), 
                        current_user_id = Depends(security.get_current_user)):
    try:
        user = user_utils.get_user(db=db, user_id=current_user_id.id)
        
        if text is None:
            raise HTTPException(status_code=400, detail=json.dumps({'message':'No request leave letter'}))

        #upload document first
        if document is not None:
            doc_url = do_upload(document, user.email)
        else:
            doc_url = None

        #store details in db
        message_data = {'sender_id':user.id,
                        'recipient_id':user_utils.get_user_by_email(db=db, email=recipient).id,
                        'label':label,
                        'title':title,
                        'document':doc_url,
                        'text':text,
                        'type':'request_leave',
                        'status':'pending'}

        message_schema = schema.CreateMessage(**message_data)
        db_message = utils.create_message(db=db, message=message_schema)

        #TODO: send notification to recipient ...
        return Response(status_code=200, content=json.dumps({'message':'Document sent successfully'}))

    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))

@router.get('/outbox/')
async def get_messages(db: Session = Depends(get_db), current_user_id = Depends(security.get_current_user)):
    user = user_utils.get_user(db=db, user_id=current_user_id.id)

    messages = user.sent_messages
    return_messsages = [schema.ReturnMessage.to_dict(msg=msg, db=db).model_dump() for msg in messages]

    return Response(status_code=200, content=json.dumps(return_messsages))

@router.get('/inbox/')
async def get_messages(db: Session = Depends(get_db), current_user_id = Depends(security.get_current_user)):
    user = user_utils.get_user(db=db, user_id=current_user_id.id)

    messages = user.received_messages
    return_messsages = [schema.ReturnMessage.to_dict(msg=msg, db=db).model_dump() for msg in messages]

    return Response(status_code=200, content=json.dumps(return_messsages))

#comment on a message

#status update on leave request

#broad cast message

@router.post('/file/')
def files(file: UploadFile):
    res = do_upload(file, 'hr@exec.mail')
    return {'message': res}