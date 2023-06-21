from enum import Enum

from fastapi import FastAPI

app = FastAPI(title="LabTracker")


@app.get("/")
async def root():
    return "Hello World"


@app.put()

