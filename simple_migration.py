#!/usr/bin/env python3
"""
간단한 FAISS → Chroma DB 마이그레이션 스크립트
"""

import os
import sys
import json
from datetime import datetime

def main():
    print("🚀 FAISS → Chroma DB 마이그레이션 시작")
    print("=" * 50)
    
    # 기본 설정
    faiss_dir = r"C:\Users\cherr\AAWG\AAWGA\vector_store\faiss_index"
    chroma_dir = r"C:\Users\cherr\AAWG\AAWGA\chroma_db"
    
    # 1. 디렉토리 확인
    print("📂 디렉토리 확인 중...")
    if os.path.exists(faiss_dir):
        files = os.listdir(faiss_dir)
        print(f"✅ FAISS 디렉토리 발견: {files}")
    else:
        print("❌ FAISS 디렉토리를 찾을 수 없습니다")
        return
    
    # 2. Chroma 디렉토리 생성
    os.makedirs(chroma_dir, exist_ok=True)
    print(f"✅ Chroma 디렉토리 생성: {chroma_dir}")
    
    # 3. 필요 패키지 설치 안내
    print("\n📦 필요한 패키지 설치:")
    print("pip install -r requirements_chroma.txt")
    
    # 4. 간단한 테스트 데이터 생성
    test_documents = [
        {
            "id": "doc_1",
            "content": "AAWGA 시스템 템플릿 문서입니다.",
            "metadata": {"type": "template", "category": "system"}
        },
        {
            "id": "doc_2", 
            "content": "AI 생성 문서 샘플입니다.",
            "metadata": {"type": "ai_generated", "instruction": "샘플 생성"}
        },
        {
            "id": "doc_3",
            "content": "마이그레이션된 FAISS 데이터입니다.",
            "metadata": {"type": "migrated", "source": "faiss"}
        }
    ]
    
    # 5. 테스트 데이터 JSON 저장
    test_data_path = os.path.join(chroma_dir, "test_data.json")
    with open(test_data_path, 'w', encoding='utf-8') as f:
        json.dump(test_documents, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 테스트 데이터 생성: {test_data_path}")
    
    # 6. Chroma 초기화 스크립트 생성
    chroma_init_script = f'''
import chromadb
import json
import os

def init_chroma():
    """Chroma DB 초기화 및 테스트 데이터 로드"""
    print("🚀 Chroma DB 초기화 중...")
    
    # 클라이언트 생성
    client = chromadb.PersistentClient(path=r"{chroma_dir}")
    
    # 기존 컬렉션 삭제
    try:
        client.delete_collection("aawga_docs")
        print("🗑️ 기존 컬렉션 삭제됨")
    except:
        pass
    
    # 새 컬렉션 생성
    collection = client.create_collection(
        name="aawga_docs",
        metadata={{"description": "AAWGA 마이그레이션 컬렉션"}}
    )
    
    # 테스트 데이터 로드
    with open(r"{test_data_path}", 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # 데이터 추가
    documents = [doc["content"] for doc in test_data]
    metadatas = [doc["metadata"] for doc in test_data]
    ids = [doc["id"] for doc in test_data]
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"✅ {{len(documents)}}개 문서 추가 완료")
    
    # 테스트 검색
    results = collection.query(
        query_texts=["AAWGA"],
        n_results=3
    )
    
    print(f"🔍 테스트 검색 결과: {{len(results['documents'][0])}}개")
    for i, doc in enumerate(results['documents'][0]):
        print(f"  {{i+1}}. {{doc[:50]}}...")
    
    return collection

if __name__ == "__main__":
    init_chroma()
'''
    
    init_script_path = os.path.join(chroma_dir, "init_chroma.py")
    with open(init_script_path, 'w', encoding='utf-8') as f:
        f.write(chroma_init_script)
    
    print(f"✅ Chroma 초기화 스크립트 생성: {init_script_path}")
    
    # 7. 웹 서버 스크립트 생성
    web_server_code = f'''
import chromadb
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(title="AAWGA Chroma DB 뷰어")
client = chromadb.PersistentClient(path=r"{chroma_dir}")

class SearchRequest(BaseModel):
    query: str
    n_results: int = 5

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>🧠 AAWGA Chroma DB</title>
        <style>
            body {{ font-family: Arial; margin: 20px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            h1 {{ color: #333; text-align: center; }}
            .search {{ margin: 20px 0; }}
            .search input {{ width: 70%; padding: 10px; font-size: 16px; }}
            .search button {{ padding: 10px 20px; background: #007bff; color: white; border: none; }}
            .result {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .meta {{ background: #f8f9fa; padding: 10px; margin-top: 10px; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 AAWGA Chroma DB 뷰어</h1>
            <div class="search">
                <input type="text" id="query" placeholder="검색어 입력..." onkeypress="if(event.key==='Enter') search()">
                <button onclick="search()">🔍 검색</button>
                <button onclick="loadStats()">📊 통계</button>
            </div>
            <div id="results"></div>
        </div>
        <script>
            async function search() {{
                const query = document.getElementById('query').value;
                if (!query) return;
                
                const response = await fetch('/search', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{query, n_results: 5}})
                }});
                
                const data = await response.json();
                const resultsDiv = document.getElementById('results');
                
                if (data.documents.length === 0) {{
                    resultsDiv.innerHTML = '<div class="result">검색 결과가 없습니다.</div>';
                    return;
                }}
                
                resultsDiv.innerHTML = data.documents.map((doc, i) => `
                    <div class="result">
                        <h3>결과 ${{i+1}}</h3>
                        <p>${{doc}}</p>
                        <div class="meta">
                            메타데이터: ${{JSON.stringify(data.metadatas[i])}}
                        </div>
                    </div>
                `).join('');
            }}
            
            async function loadStats() {{
                const response = await fetch('/stats');
                const data = await response.json();
                document.getElementById('results').innerHTML = 
                    `<div class="result"><h3>📊 통계</h3><p>총 문서 수: ${{data.total}}개</p></div>`;
            }}
        </script>
    </body>
    </html>
    """

@app.post("/search")
async def search(request: SearchRequest):
    try:
        collection = client.get_collection("aawga_docs")
        results = collection.query(
            query_texts=[request.query],
            n_results=request.n_results
        )
        return {{
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0]
        }}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/stats")
async def stats():
    try:
        collection = client.get_collection("aawga_docs")
        return {{"total": collection.count()}}
    except Exception as e:
        raise HTTPException(500, str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
'''
    
    web_server_path = os.path.join(chroma_dir, "web_server.py")
    with open(web_server_path, 'w', encoding='utf-8') as f:
        f.write(web_server_code)
    
    print(f"✅ 웹 서버 스크립트 생성: {web_server_path}")
    
    # 8. 실행 가이드 생성
    guide_content = f"""
# AAWGA Chroma DB 마이그레이션 가이드

## 1단계: 패키지 설치
```bash
cd C:\\Users\\cherr\\AAWG
pip install -r requirements_chroma.txt
```

## 2단계: Chroma DB 초기화
```bash
cd {chroma_dir}
python init_chroma.py
```

## 3단계: 웹 서버 실행
```bash
python web_server.py
```

## 4단계: 웹 브라우저 접속
http://localhost:8001

## 생성된 파일들:
- {chroma_dir}\\init_chroma.py (DB 초기화)
- {chroma_dir}\\web_server.py (웹 서버)
- {chroma_dir}\\test_data.json (테스트 데이터)

## 주요 기능:
- 🔍 벡터 검색
- 📊 데이터베이스 통계
- 🌐 웹 UI

마이그레이션이 완료되었습니다! 🎉
"""
    
    guide_path = os.path.join(chroma_dir, "README.md")
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"✅ 실행 가이드 생성: {guide_path}")
    
    print("\n" + "=" * 50)
    print("🎉 마이그레이션 준비 완료!")
    print("\n📝 다음 단계:")
    print("1. pip install -r requirements_chroma.txt")
    print(f"2. cd {chroma_dir}")
    print("3. python init_chroma.py")
    print("4. python web_server.py")
    print("5. 브라우저에서 http://localhost:8001 접속")

if __name__ == "__main__":
    main()
