from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

class Testcase(BaseModel):
    id: str
    requirement_id: str
    steps: List[str]
    expected_result: str

class TestcaseDefinition(BaseModel):
    testcases: List[Testcase]

router = APIRouter()

@router.post("", response_model=TestcaseDefinition, summary="테스트케이스 생성")
async def create_testcases(defs: TestcaseDefinition):
    return defs
