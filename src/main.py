from fastapi import FastAPI, status

from src.auth.router import router as auth_router

app = FastAPI(title="LabTracker",
              description="An application for tracking labs, term papers and essays for students")
app.include_router(auth_router)


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {'status': status.HTTP_200_OK, 'message': "Server is OK"}


