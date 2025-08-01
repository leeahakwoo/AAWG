import motor.motor_asyncio
from typing import List, Optional
from models.db_models import TemplateModel, FeedbackModel, PyObjectId
from datetime import datetime
import os
import asyncio
from urllib.parse import urlparse, quote_plus, urlunparse

# MongoDB 연결 설정
# 예시: mongodb+srv://cpno13:ｈａｋ１２３１２３@cluster0.jbpyakm.mongodb.net/aawga?retryWrites=true&w=majority
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "aawga")

class DatabaseService:
    def __init__(self):
        self.client = None
        self.db = None
        self.templates = None
        self.feedback = None
        self._connected = False
        self._init_connection()
    
    def _init_connection(self):
        """MongoDB 연결 초기화 (Atlas URI의 비밀번호를 URL‐encode 처리)"""
        try:
            uri = MONGODB_URL
            # Atlas+srv URI 인 경우에만 parsing
            if uri.startswith("mongodb+srv://"):
                parsed = urlparse(uri)
                user = parsed.username or ""
                pwd = parsed.password or ""
                host_and_path = parsed.netloc.split("@")[-1]  # host:port[/db]
                encoded_pwd = quote_plus(pwd)
                # 재조립
                new_netloc = f"{user}:{encoded_pwd}@{host_and_path}"
                uri = urlunparse((
                    parsed.scheme,
                    new_netloc,
                    parsed.path,
                    parsed.params,
                    parsed.query,
                    parsed.fragment
                ))
            # 실제 client 생성
            self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
            self.db = self.client[DATABASE_NAME]
            self.templates = self.db.templates
            self.feedback = self.db.feedback
            self._connected = True
            print("✅ MongoDB 연결 성공:", uri)
        except Exception as e:
            print(f"❌ MongoDB 연결 실패: {e}")
            self._connected = False
    
    async def _ensure_connection(self):
        """연결 상태 확인 및 재연결"""
        if not self._connected:
            self._init_connection()
            if not self._connected:
                return False
        return True

    # 이하 메서드는 기존과 동일...
    async def create_template(self, template: TemplateModel) -> TemplateModel:
        if not await self._ensure_connection():
            template.id = PyObjectId()
            template.created_at = datetime.utcnow()
            template.updated_at = datetime.utcnow()
            return template
        template_dict = template.dict(by_alias=True)
        template_dict["created_at"] = datetime.utcnow()
        template_dict["updated_at"] = datetime.utcnow()
        result = await self.templates.insert_one(template_dict)
        template.id = result.inserted_id
        return template

    async def get_template(self, template_id: str) -> Optional[TemplateModel]:
        if not await self._ensure_connection():
            return None
        template_dict = await self.templates.find_one({"_id": PyObjectId(template_id)})
        return TemplateModel(**template_dict) if template_dict else None

    async def get_templates(self, category: Optional[str] = None) -> List[TemplateModel]:
        if not await self._ensure_connection():
            return []
        filter_query = {}
        if category:
            filter_query["category"] = category
        cursor = self.templates.find(filter_query).sort("created_at", -1)
        return [TemplateModel(**d) async for d in cursor]

    async def update_template(self, template_id: str, template: TemplateModel) -> Optional[TemplateModel]:
        if not await self._ensure_connection():
            return None
        template_dict = template.dict(by_alias=True, exclude={"id"})
        template_dict["updated_at"] = datetime.utcnow()
        result = await self.templates.update_one({"_id": PyObjectId(template_id)}, {"$set": template_dict})
        return await self.get_template(template_id) if result.modified_count else None

    async def delete_template(self, template_id: str) -> bool:
        if not await self._ensure_connection():
            return False
        result = await self.templates.delete_one({"_id": PyObjectId(template_id)})
        return result.deleted_count > 0

    async def get_default_template(self, category: str) -> Optional[TemplateModel]:
        if not await self._ensure_connection():
            return None
        d = await self.templates.find_one({"category": category, "is_default": True})
        return TemplateModel(**d) if d else None

    async def create_feedback(self, feedback: FeedbackModel) -> FeedbackModel:
        if not await self._ensure_connection():
            feedback.id = PyObjectId()
            feedback.created_at = datetime.utcnow()
            return feedback
        feedback_dict = feedback.dict(by_alias=True)
        feedback_dict["created_at"] = datetime.utcnow()
        res = await self.feedback.insert_one(feedback_dict)
        feedback.id = res.inserted_id
        return feedback

    async def get_feedback(self, limit: int = 50) -> List[FeedbackModel]:
        if not await self._ensure_connection():
            return []
        cursor = self.feedback.find().sort("created_at", -1).limit(limit)
        return [FeedbackModel(**d) async for d in cursor]

# 전역 데이터베이스 서비스 인스턴스
db_service = DatabaseService()
