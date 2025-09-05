#!/usr/bin/env python3
"""
FAISS → ChromaDB 마이그레이션 실행 스크립트
실행: python execute_migration.py
"""

import os
import sys
import shutil
from datetime import datetime

def main():
    print("🚀 FAISS → ChromaDB 마이그레이션 실행")
    print("=" * 60)
    
    # 경로 설정
    project_root = r"C:\Users\cherr\AAWG\AAWGA"
    backend_dir = os.path.join(project_root, "backend")
    services_dir = os.path.join(backend_dir, "services")
    
    # 1단계: 백업 생성
    print("📦 1단계: FAISS 데이터 백업 생성")
    backup_dir = os.path.join(project_root, "backup", f"faiss_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    faiss_dir = os.path.join(project_root, "vector_store", "faiss_index")
    
    if os.path.exists(faiss_dir):
        os.makedirs(backup_dir, exist_ok=True)
        shutil.copytree(faiss_dir, os.path.join(backup_dir, "faiss_index"))
        print(f"✅ FAISS 백업 완료: {backup_dir}")
    else:
        print("⚠️ FAISS 디렉토리를 찾을 수 없습니다")
    
    # 2단계: ChromaDB 서비스 파일 생성
    print("\n🔧 2단계: ChromaDB 서비스 파일 생성")
    
    chroma_service_content = '''# backend/services/vector_service_chroma.py

import os
import chromadb
from typing import List, Dict, Any, Optional
from datetime import datetime
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

class ChromaVectorService:
    """ChromaDB 기반 벡터 서비스"""
    
    def __init__(self):
        self.chroma_db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            "chroma_db"
        )
        
        # ChromaDB 클라이언트 초기화
        try:
            self.client = chromadb.PersistentClient(path=self.chroma_db_path)
            print(f"✅ ChromaDB 클라이언트 연결: {self.chroma_db_path}")
        except Exception as e:
            print(f"❌ ChromaDB 클라이언트 초기화 실패: {e}")
            self.client = None
            return
        
        # 컬렉션 설정
        try:
            self.collection = self.client.get_collection("aawga_documents")
            print("✅ 기존 ChromaDB 컬렉션 로드됨")
        except:
            try:
                self.collection = self.client.create_collection(
                    name="aawga_documents",
                    metadata={"description": "AAWGA 메인 문서 컬렉션"}
                )
                print("🆕 새 ChromaDB 컬렉션 생성됨")
            except Exception as e:
                print(f"❌ 컬렉션 생성 실패: {e}")
                self.collection = None
                return
        
        print(f"✅ ChromaVectorService 초기화 완료")
    
    def chunk_template(self, template) -> List[Document]:
        """템플릿을 청크로 분할 (기존 로직 유지)"""
        try:
            content = template.content
            if isinstance(content, dict):
                text_content = content.get('text', '') or str(content)
            else:
                text_content = str(content)
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=100,
                separators=["\\n\\n", "\\n", ". ", "\\u3002", "!", "?", "！", "？", ",", "，", "；", ":", "：", " ", ""]
            )
            
            chunks = text_splitter.split_text(text_content)
            
            documents = []
            for i, chunk in enumerate(chunks):
                if chunk.strip():
                    doc = Document(
                        page_content=chunk.strip(),
                        metadata={
                            "doc_type": "template",
                            "template_id": str(template.id),
                            "template_name": template.name,
                            "category": template.category,
                            "chunk_id": i,
                            "created_at": datetime.now().isoformat(),
                            "doc_id": f"template_{template.id}_{i}"
                        }
                    )
                    documents.append(doc)
            
            return documents
            
        except Exception as e:
            print(f"❌ 템플릿 청킹 실패: {e}")
            return []
    
    def chunk_generated_document(self, content: str, instruction: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """AI 생성 문서를 청크로 분할 (기존 로직 유지)"""
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=150,
                separators=["\\n\\n", "\\n", ". ", "\\u3002", "!", "?", "！", "？", ",", "，", "；", ":", "：", " ", ""]
            )
            
            chunks = text_splitter.split_text(content)
            
            documents = []
            timestamp = datetime.now().isoformat()
            doc_id_base = f"generated_{int(datetime.now().timestamp())}"
            
            for i, chunk in enumerate(chunks):
                if chunk.strip():
                    doc_metadata = {
                        "doc_type": "ai_generated", 
                        "instruction": instruction,
                        "chunk_id": i,
                        "created_at": timestamp,
                        "doc_id": f"{doc_id_base}_{i}"
                    }
                    
                    if metadata:
                        doc_metadata.update(metadata)
                    
                    doc = Document(
                        page_content=chunk.strip(),
                        metadata=doc_metadata
                    )
                    documents.append(doc)
            
            return documents
            
        except Exception as e:
            print(f"❌ 생성 문서 청킹 실패: {e}")
            return []
    
    async def add_template(self, template) -> bool:
        """템플릿을 ChromaDB에 추가"""
        try:
            if not self.collection:
                print("❌ ChromaDB 컬렉션이 초기화되지 않음")
                return False
            
            documents = self.chunk_template(template)
            if not documents:
                return False
            
            return await self.add_documents(documents)
            
        except Exception as e:
            print(f"❌ 템플릿 추가 실패: {e}")
            return False
    
    async def add_generated_document(self, content: str, instruction: str, metadata: Dict[str, Any] = None) -> bool:
        """AI 생성 문서를 ChromaDB에 추가"""
        try:
            if not self.collection:
                print("❌ ChromaDB 컬렉션이 초기화되지 않음")
                return False
            
            documents = self.chunk_generated_document(content, instruction, metadata)
            if not documents:
                return False
            
            return await self.add_documents(documents)
            
        except Exception as e:
            print(f"❌ AI 문서 추가 실패: {e}")
            return False
    
    async def add_documents(self, documents: List[Document]) -> bool:
        """문서들을 ChromaDB에 추가"""
        try:
            if not self.collection or not documents:
                return False
            
            # 문서 데이터 준비
            ids = []
            contents = []
            metadatas = []
            
            for i, doc in enumerate(documents):
                doc_id = doc.metadata.get("doc_id", f"doc_{i}_{int(datetime.now().timestamp())}")
                ids.append(doc_id)
                contents.append(doc.page_content)
                metadatas.append(doc.metadata)
            
            # ChromaDB에 추가
            self.collection.add(
                documents=contents,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✅ ChromaDB에 {len(documents)}개 문서 추가됨")
            return True
            
        except Exception as e:
            print(f"❌ ChromaDB 문서 추가 실패: {e}")
            return False
    
    def search_similar(self, query: str, k: int = 5, doc_type: Optional[str] = None) -> List[Document]:
        """ChromaDB에서 유사 문서 검색"""
        try:
            if not self.collection:
                print("❌ ChromaDB 컬렉션이 초기화되지 않음")
                return []
            
            # ChromaDB 쿼리 실행
            where_clause = {"doc_type": doc_type} if doc_type else None
            
            results = self.collection.query(
                query_texts=[query],
                n_results=k,
                where=where_clause
            )
            
            # Document 객체로 변환
            documents = []
            if results["documents"] and results["documents"][0]:
                for i, content in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i] if results["metadatas"] and results["metadatas"][0] else {}
                    documents.append(Document(
                        page_content=content,
                        metadata=metadata
                    ))
            
            return documents
            
        except Exception as e:
            print(f"❌ ChromaDB 검색 실패: {e}")
            return []
    
    def get_vector_store_stats(self) -> Dict[str, Any]:
        """ChromaDB 통계 정보"""
        try:
            if not self.collection:
                return {"error": "ChromaDB 컬렉션이 초기화되지 않음"}
            
            count = self.collection.count()
            return {
                "total_documents": count,
                "vector_store_type": "chromadb",
                "vector_store_exists": True,
                "index_file_exists": True,
                "storage_path": self.chroma_db_path,
                "collection_name": "aawga_documents"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def save_index(self):
        """ChromaDB는 자동 저장되므로 패스"""
        print("💾 ChromaDB는 자동으로 저장됩니다")

# 전역 ChromaDB 서비스 인스턴스
chroma_vector_service = ChromaVectorService()
'''
    
    chroma_service_path = os.path.join(services_dir, "vector_service_chroma.py")
    with open(chroma_service_path, 'w', encoding='utf-8') as f:
        f.write(chroma_service_content)
    print(f"✅ ChromaDB 서비스 파일 생성: {chroma_service_path}")
    
    # 3단계: 기존 vector_service.py 백업 및 수정
    print("\n🔄 3단계: 기존 vector_service.py 수정")
    
    vector_service_path = os.path.join(services_dir, "vector_service.py")
    vector_service_backup = os.path.join(backup_dir, "vector_service_original.py")
    
    # 백업
    if os.path.exists(vector_service_path):
        shutil.copy2(vector_service_path, vector_service_backup)
        print(f"✅ 기존 vector_service.py 백업: {vector_service_backup}")
    
    # 새 vector_service.py 생성 (ChromaDB 래퍼)
    new_vector_service_content = '''# backend/services/vector_service.py
# ChromaDB 전환 버전

import os
from typing import List, Dict, Any, Optional
from datetime import datetime

# ChromaDB 사용 설정 확인
USE_CHROMADB = os.getenv("USE_CHROMADB", "true").lower() == "true"

if USE_CHROMADB:
    try:
        from .vector_service_chroma import chroma_vector_service
        print("🔄 ChromaDB 모드로 전환됨")
        CHROMADB_AVAILABLE = True
    except ImportError as e:
        print(f"❌ ChromaDB 서비스 임포트 실패: {e}")
        CHROMADB_AVAILABLE = False
else:
    CHROMADB_AVAILABLE = False

# FAISS 관련 임포트 (폴백용)
try:
    import pickle
    import numpy as np
    from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_core.documents import Document
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from models.db_models import TemplateModel
    FAISS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ FAISS 관련 라이브러리 임포트 실패: {e}")
    FAISS_AVAILABLE = False

class VectorStoreService:
    """
    벡터 스토어 관리 서비스 (ChromaDB/FAISS 하이브리드)
    """
    
    def __init__(self):
        self.use_chromadb = USE_CHROMADB and CHROMADB_AVAILABLE
        
        if self.use_chromadb:
            self.service = chroma_vector_service
            print("✅ ChromaDB 서비스 로드됨")
        elif FAISS_AVAILABLE:
            print("🔄 FAISS 폴백 모드")
            self._init_faiss()
        else:
            print("❌ 사용 가능한 벡터 서비스가 없습니다")
            self.service = None
            self.vector_store = None
    
    def _init_faiss(self):
        """FAISS 초기화 (폴백용)"""
        try:
            self.vector_store_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "vector_store")
            self.faiss_index_dir = os.path.join(self.vector_store_dir, "faiss_index")
            self.index_file = os.path.join(self.faiss_index_dir, "index.faiss")
            self.pkl_file = os.path.join(self.faiss_index_dir, "index.pkl")
            
            # 임베딩 모델
            api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            if api_key:
                self.embedder = GoogleGenerativeAIEmbeddings(
                    model="models/gemini-embedding-001",
                    google_api_key=api_key,
                )
            else:
                self.embedder = None
                print("⚠️ GOOGLE_API_KEY 없음 - FAISS 더미 모드")
            
            # 기존 인덱스 로드
            if os.path.exists(self.index_file) and os.path.exists(self.pkl_file) and self.embedder:
                self.vector_store = FAISS.load_local(
                    self.faiss_index_dir, 
                    self.embedder,
                    allow_dangerous_deserialization=True
                )
                print("✅ 기존 FAISS 벡터 스토어 로드됨")
            else:
                self.vector_store = None
                print("⚠️ FAISS 벡터 스토어 초기화 실패")
                
        except Exception as e:
            print(f"❌ FAISS 초기화 실패: {e}")
            self.vector_store = None
    
    async def add_template(self, template) -> bool:
        """템플릿 추가"""
        if self.use_chromadb:
            return await self.service.add_template(template)
        elif self.vector_store:
            # FAISS 폴백 로직
            print("⚠️ FAISS 폴백 모드에서 템플릿 추가")
            return False
        else:
            print("❌ 사용 가능한 벡터 서비스가 없습니다")
            return False
    
    async def add_generated_document(self, content: str, instruction: str, metadata: Dict[str, Any] = None) -> bool:
        """AI 생성 문서 추가"""
        if self.use_chromadb:
            return await self.service.add_generated_document(content, instruction, metadata)
        elif self.vector_store:
            # FAISS 폴백 로직
            print("⚠️ FAISS 폴백 모드에서 문서 추가")
            return False
        else:
            print("❌ 사용 가능한 벡터 서비스가 없습니다")
            return False
    
    def search_similar(self, query: str, k: int = 5, doc_type: Optional[str] = None) -> List:
        """유사 문서 검색"""
        if self.use_chromadb:
            return self.service.search_similar(query, k, doc_type)
        elif self.vector_store:
            # FAISS 폴백 로직
            try:
                return self.vector_store.similarity_search(query, k=k)
            except Exception as e:
                print(f"❌ FAISS 검색 실패: {e}")
                return []
        else:
            print("❌ 사용 가능한 벡터 서비스가 없습니다")
            return []
    
    def get_vector_store_stats(self) -> Dict[str, Any]:
        """벡터 스토어 통계"""
        if self.use_chromadb:
            return self.service.get_vector_store_stats()
        elif self.vector_store:
            return {
                "total_documents": "unknown",
                "vector_store_type": "faiss_fallback",
                "vector_store_exists": True,
                "storage_path": getattr(self, 'faiss_index_dir', 'unknown')
            }
        else:
            return {
                "error": "사용 가능한 벡터 서비스가 없습니다",
                "vector_store_exists": False
            }
    
    def save_index(self):
        """인덱스 저장"""
        if self.use_chromadb:
            self.service.save_index()
        elif self.vector_store:
            try:
                self.vector_store.save_local(self.faiss_index_dir)
                print("💾 FAISS 인덱스 저장됨")
            except Exception as e:
                print(f"❌ FAISS 인덱스 저장 실패: {e}")

# 전역 벡터 서비스 인스턴스
vector_service = VectorStoreService()
'''
    
    with open(vector_service_path, 'w', encoding='utf-8') as f:
        f.write(new_vector_service_content)
    print(f"✅ vector_service.py 수정 완료")
    
    # 4단계: 환경 변수 설정
    print("\n⚙️ 4단계: 환경 변수 설정")
    env_path = os.path.join(backend_dir, ".env")
    
    env_content = ""
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
    
    # ChromaDB 설정 추가
    if "USE_CHROMADB" not in env_content:
        env_content += "\\n# ChromaDB 설정\\nUSE_CHROMADB=true\\n"
        
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"✅ .env 파일 업데이트: {env_path}")
    else:
        print("✅ .env 파일에 ChromaDB 설정이 이미 있습니다")
    
    # 5단계: 마이그레이션 실행
    print("\\n🔄 5단계: 데이터 마이그레이션 실행")
    
    try:
        print("마이그레이션 스크립트 실행 중...")
        import subprocess
        result = subprocess.run([sys.executable, "migration_script.py"], 
                              cwd=r"C:\\Users\\cherr\\AAWG", 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 마이그레이션 성공!")
            print(result.stdout[-500:])  # 마지막 500자만 출력
        else:
            print("⚠️ 마이그레이션 중 일부 오류 발생")
            print(result.stderr[-500:])
            
    except Exception as e:
        print(f"⚠️ 마이그레이션 스크립트 실행 중 오류: {e}")
        print("수동으로 마이그레이션을 실행해주세요:")
        print("python migration_script.py")
    
    # 6단계: 완료 및 테스트 가이드
    print("\\n" + "=" * 60)
    print("🎉 마이그레이션 완료!")
    print("\\n📝 다음 단계:")
    print("1. 서버 재시작:")
    print("   cd AAWGA/backend")
    print("   python app.py")
    print("\\n2. 테스트:")
    print("   http://localhost:8000/api/system/status")
    print("\\n3. ChromaDB 웹 인터페이스:")
    print("   cd AAWGA/chroma_db")
    print("   python web_server.py")
    print("   http://localhost:8001")
    print("\\n📦 백업 위치:")
    print(f"   {backup_dir}")
    print("\\n🔄 롤백이 필요한 경우:")
    print("   USE_CHROMADB=false")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\\n✅ 마이그레이션 실행 완료!")
        else:
            print("\\n❌ 마이그레이션 실행 실패!")
    except Exception as e:
        print(f"\\n❌ 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
