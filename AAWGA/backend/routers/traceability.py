# backend/routers/traceability.py

from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

class TraceabilityItem(BaseModel):
    requirement_id: str
    testcase_ids: List[str]

class TraceabilityDefinition(BaseModel):
    traceability_matrix: List[TraceabilityItem]

router = APIRouter()

@router.post(
    "",
    response_model=TraceabilityDefinition,
    summary="요구사항–테스트케이스 추적성 매트릭스 생성"
)
async def make_traceability(
    input_data: TraceabilityDefinition
):
    return input_data
