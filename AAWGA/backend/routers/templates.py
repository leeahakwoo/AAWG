from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from models.db_models import TemplateModel
from backend.services.database import db_service
from pydantic import BaseModel

router = APIRouter(prefix="/templates", tags=["templates"])

class CreateTemplateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    content: dict
    is_default: bool = False

class UpdateTemplateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    content: Optional[dict] = None
    is_default: Optional[bool] = None

@router.post("/", response_model=TemplateModel)
async def create_template(request: CreateTemplateRequest):
    """템플릿 생성"""
    try:
        template = TemplateModel(
            name=request.name,
            description=request.description,
            category=request.category,
            content=request.content,
            is_default=request.is_default
        )
        return await db_service.create_template(template)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TemplateModel])
async def get_templates(category: Optional[str] = None):
    """템플릿 목록 조회"""
    try:
        return await db_service.get_templates(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{template_id}", response_model=TemplateModel)
async def get_template(template_id: str):
    """템플릿 조회"""
    try:
        template = await db_service.get_template(template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{template_id}", response_model=TemplateModel)
async def update_template(template_id: str, request: UpdateTemplateRequest):
    """템플릿 수정"""
    try:
        # 기존 템플릿 조회
        existing_template = await db_service.get_template(template_id)
        if not existing_template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # 업데이트할 필드만 수정
        update_data = request.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        updated_template = TemplateModel(
            id=existing_template.id,
            name=update_data.get("name", existing_template.name),
            description=update_data.get("description", existing_template.description),
            category=update_data.get("category", existing_template.category),
            content=update_data.get("content", existing_template.content),
            is_default=update_data.get("is_default", existing_template.is_default),
            created_at=existing_template.created_at
        )
        
        result = await db_service.update_template(template_id, updated_template)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to update template")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{template_id}")
async def delete_template(template_id: str):
    """템플릿 삭제"""
    try:
        success = await db_service.delete_template(template_id)
        if not success:
            raise HTTPException(status_code=404, detail="Template not found")
        return {"message": "Template deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/default/{category}", response_model=TemplateModel)
async def get_default_template(category: str):
    """기본 템플릿 조회"""
    try:
        template = await db_service.get_default_template(category)
        if not template:
            raise HTTPException(status_code=404, detail=f"No default template found for category: {category}")
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 