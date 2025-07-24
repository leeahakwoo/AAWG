# backend/app.py

from fastapi import FastAPI
from backend.routers import requirements, testcases, traceability

app = FastAPI(
    title="AAWGA Agent API",
    version="1.0.0",
    description="요구사항·테스트케이스·추적성 Agent API"
)

# 각 라우터 파일에서 FastAPI Router 인스턴스를 `router`로 export했다고 가정합니다.
app.include_router(
    requirements.router,
    prefix="/requirements",
    tags=["requirements"]
)
app.include_router(
    testcases.router,
    prefix="/testcases",
    tags=["testcases"]
)
app.include_router(
    traceability.router,
    prefix="/traceability",
    tags=["traceability"]
)
