from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models.db_models import FeedbackModel
from backend.services.database import db_service
from pydantic import BaseModel

router = APIRouter(prefix="/feedback", tags=["feedback"])

class CreateFeedbackRequest(BaseModel):
    template_id: Optional[str] = None
    instruction: str
    original_content: str
    generated_result: dict
    user_feedback: str
    rating: Optional[int] = None

@router.post("/", response_model=FeedbackModel)
async def create_feedback(request: CreateFeedbackRequest):
    """피드백 생성"""
    try:
        feedback = FeedbackModel(
            template_id=request.template_id,
            instruction=request.instruction,
            original_content=request.original_content,
            generated_result=request.generated_result,
            user_feedback=request.user_feedback,
            rating=request.rating
        )
        return await db_service.create_feedback(feedback)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[FeedbackModel])
async def get_feedback(limit: Optional[int] = 50):
    """피드백 목록 조회"""
    try:
        return await db_service.get_feedback(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 