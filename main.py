from fastapi import FastAPI, APIRouter

from api.endpoints import user_router

app = FastAPI(title="LabTracker",
              description="An application for tracking labs, term papers and essays for students")

main_router = APIRouter()

main_router.include_router(user_router)
app.include_router(main_router)


@app.get("/")
async def root():
    return {'status': 200, 'message': "Server is OK"}


