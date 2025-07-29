# backend/services/rag_search.py

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

__all__ = ["save_to_vectorstore", "search_documents"]

# ───── 더미 Embeddings 정의 ─────
class DummyEmbeddings:
    """
    - embed_documents: 입력된 텍스트 리스트마다 동일한 [0.1,...] 벡터 반환
    - embed_query: 쿼리 하나당 동일한 [0.1,...] 벡터 반환
    - __call__: FAISS 내부 호출 지원
    """
    def __init__(self, dim: int = 5):
        self.dim = dim

    def __call__(self, text: str):
        return self.embed_query(text)

    def embed_documents(self, texts):
        return [[0.1] * self.dim for _ in texts]

    def embed_query(self, text):
        return [0.1] * self.dim

# ───── 벡터 스토어 경로 ─────
DB_PATH = "vector_store/faiss_index_dummy"

def chunk_documents(text: str):
    """
    긴 문서를 500자씩 끊어 Document 객체 리스트로 반환.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.create_documents([text])

def save_to_vectorstore(text: str):
    """
    1) 텍스트 청킹
    2) 더미 임베딩
    3) FAISS 인덱스 저장
    """
    os.makedirs(DB_PATH, exist_ok=True)
    docs = chunk_documents(text)
    embeddings = DummyEmbeddings(dim=5)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(DB_PATH)

def search_documents(query: str) -> str:
    """
    1) 저장된 FAISS 인덱스 로드
    2) 더미 임베딩으로 유사도 검색 (k=3)
    3) 청크들을 문자열로 합쳐 반환
    """
    if not os.path.exists(DB_PATH):
        return "벡터 DB가 존재하지 않습니다. 먼저 save_to_vectorstore()를 호출하세요."

    embeddings = DummyEmbeddings(dim=5)
    db = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    results = db.similarity_search(query, k=3)
    return "\n---\n".join(doc.page_content for doc in results)
