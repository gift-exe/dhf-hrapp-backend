from fastapi import FastAPI
from config.database import Base, engine
import user.model
from user.controller import router as user_router
from message.controller import  router as message_router
from office.controller import router as office_router
from generate_reports.controller import router as report_router


app = FastAPI()

app.include_router(user_router, prefix='/user')
app.include_router(message_router, prefix='/messages')
app.include_router(office_router, prefix='/offices')
app.include_router(report_router, prefix='/generate-report')


Base.metadata.create_all(bind=engine)

@app.get('/')
async def home():
    return {'message': 'HR API v0.0.1'}


