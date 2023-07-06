from fastapi import FastAPI, APIRouter

from src.auth.router import router as auth_router

app = FastAPI(title="LabTracker",
              description="An application for tracking labs, term papers and essays for students")

app.include_router(auth_router)


@app.get("/")
async def root():
    return {'status': 200, 'message': "Server is OK"}


