# backend/routers/requirements.py

from fastapi import APIRouter, UploadFile, File
from typing import List
from backend.schemas.requirement_agent_output import RequirementDefinitionOutput  # Pydantic 모델로 대체

router = APIRouter()

@router.post(
    "",  # /requirements
    response_model=RequirementDefinitionOutput,
    summary="사업계획서에서 요구사항 추출"
)
async def extract_requirements(
    business_plan: UploadFile = File(...)
):
    # TODO: 실제 PPTX/PDF 파싱 로직을 여기에 넣으세요.
    # 예시 더미 응답:
    return {"requirements": [
        {"id":"REQ-001","title":"유저 로그인","description":"이메일/비번","priority":"High"}
    ]}
