from fastapi import APIRouter, UploadFile, File
from typing import List
from pydantic import BaseModel

class Requirement(BaseModel):
    id: str
    title: str
    description: str
    priority: str

class RequirementDefinition(BaseModel):
    requirements: List[Requirement]

router = APIRouter()

@router.post(
    "",
    response_model=RequirementDefinition,
    summary="사업계획서에서 요구사항 추출"
)
async def extract_requirements(
    business_plan: UploadFile = File(...)
):
    return RequirementDefinition(requirements=[
        Requirement(
            id="REQ-001",
            title="유저 로그인 기능",
            description="이메일/비밀번호를 통한 로그인 지원",
            priority="High"
        )
    ])
