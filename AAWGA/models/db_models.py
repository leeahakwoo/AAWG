# models/db_models.py

from typing import Any, Optional, Dict
from bson import ObjectId
from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from datetime import datetime


class PyObjectId(ObjectId):
    """
    MongoDB ObjectId를 Pydantic v2 모델에서 안전하게 쓰기 위한 커스텀 타입입니다.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        # 먼저 str용 스키마 받고
        str_schema = handler(str)
        # ObjectId로 변환해주는 검증기
        def validate_pyobjectid(v: Any, info: core_schema.ValidationInfo) -> ObjectId:
            if isinstance(v, ObjectId):
                return v
            return ObjectId(v)

        return core_schema.with_info_plain_validator_function(validate_pyobjectid)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: Any, handler: Any
    ) -> JsonSchemaValue:
        return {
            "type": "string",
            "format": "objectId",
            "description": "MongoDB ObjectId",
        }


class TemplateModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None
    category: str
    content: dict[str, Any]
    is_default: bool = False

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
        "json_encoders": {ObjectId: str},
    }


class FeedbackModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    template_id: Optional[str] = None
    instruction: str
    original_content: str
    generated_result: Dict[str, Any]
    user_feedback: str
    rating: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
        "json_encoders": {ObjectId: str},
    }
