# backend/routers/requirements.py

from fastapi import APIRouter, UploadFile, File
from typing import List
from pydantic import BaseModel

# 1) 스키마 정의 (schemas 폴더에 뺀 후 import 해도 좋습니다)
class Requirement(BaseModel):
    id: str
    title: str
    description: str
    priority: str

class RequirementDefinition(BaseModel):
    requirements: List[Requirement]

# 2) APIRouter 인스턴스를 router 변수로 선언
router = APIRouter()

# 3) 엔드포인트 등록
@router.post(
    "",  # /requirements
    response_model=RequirementDefinition,
    summary="사업계획서에서 요구사항 추출"
)
async def extract_requirements(
    business_plan: UploadFile = File(...)
):
    # TODO: 실제 PPTX/PDF 파싱 로직
    # 테스트를 위해 더미 데이터를 반환
    return RequirementDefinition(requirements=[
        Requirement(
            id="REQ-001",
            title="유저 로그인 기능",
            description="이메일/비밀번호를 통한 로그인 지원",
            priority="High"
        )
    ])
