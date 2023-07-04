from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from db.dal import UserDAL
from db.models import User
from db.session import get_session
from models.models import CreateUser

app = FastAPI(title="LabTracker",
              description="An application for tracking labs, term papers and essays for students")

main_api_router = APIRouter()

auth_api_router = APIRouter()


@app.get("/")
async def root():
    return {'status': 200, 'message': "Server is OK", 'settings': settings}


@app.post("/reg")
async def registration(user: CreateUser, session: AsyncSession = Depends(get_session)):
    user_dal = UserDAL(session)
    new_user = await user_dal.create_user(
        username=user.username,
        email=user.email,
        password=user.password
    )
    return {'user': new_user}
