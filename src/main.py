from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.tracker.router import teachers_router as tracker_teachers_router
from src.tracker.router import subjects_router as tracker_subjects_router
from src.tracker.router import tasks_router as tracker_tasks_router

app = FastAPI(title="LabTracker",
              description="An application for tracking labs, term papers and essays for students")
app.include_router(auth_router)
app.include_router(tracker_teachers_router)
app.include_router(tracker_subjects_router)
app.include_router(tracker_tasks_router)

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://192.168.1.67:5173",
    "http://192.168.1.67"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {'status': status.HTTP_200_OK, 'message': "Server is OK"}
