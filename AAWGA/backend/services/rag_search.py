# backend/services/rag_search.py
import os
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

import pickle

# 경로는 실제 저장될 로컬 디렉토리
DB_PATH = "vector_store/faiss_index"

# 문서 청킹 함수
def chunk_documents(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs = splitter.create_documents([text])
    return docs

# 임베딩 및 벡터 DB 구축
def save_to_vectorstore(text: str):
    docs = chunk_documents(text)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(DB_PATH)

# 검색 함수 (Agent에서 호출)
def search_documents(query: str) -> str:
    if not os.path.exists(DB_PATH):
        return "벡터 DB가 존재하지 않습니다. 문서를 먼저 업로드하고 저장하세요."

    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local(DB_PATH, embeddings)
    results = db.similarity_search(query, k=3)

    context = "\n---\n".join([doc.page_content for doc in results])
    return context
