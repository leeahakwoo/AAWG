# backend/app.py

from fastapi import FastAPI
from backend.routers import requirements, testcases, traceability

app = FastAPI(
    title="AAWGA Agent API",
    version="1.0.0"
)

app.include_router(requirements.router,    prefix="/requirements", tags=["requirements"])
app.include_router(testcases.router,       prefix="/testcases",   tags=["testcases"])
app.include_router(traceability.router,    prefix="/traceability",tags=["traceability"])
