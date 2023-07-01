from fastapi import FastAPI
from fastapi_users import fastapi_users, FastAPIUsers
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from config import settings

fastapi_users_lib = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(title="LabTracker")

app.include_router(
    fastapi_users_lib.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users_lib.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/")
async def root():
    return {'status': 200, 'message': "Server is OK", 'settings': settings}


