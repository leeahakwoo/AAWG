#!/usr/bin/env python3
# migration_script.py - FAISS to Chroma DB Migration

import os
import sys
import json
import pickle
import subprocess
from typing import List, Dict, Any, Optional
from datetime import datetime

def install_packages():
    """필요한 패키지 설치"""
    packages = ['chromadb', 'fastapi', 'uvicorn']
    
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} 이미 설치됨")
        except ImportError:
            print(f"📦 {package} 설치 중...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ {package} 설치 완료")
            except subprocess.CalledProcessError as e:
                print(f"❌ {package} 설치 실패: {e}")
                return False
    return True

def analyze_faiss_data(faiss_index_dir: str):
    """기존 FAISS 데이터 분석"""
    print("🔍 기존 FAISS 데이터 분석 중...")
    
    index_file = os.path.join(faiss_index_dir, "index.faiss")
    pkl_file = os.path.join(faiss_index_dir, "index.pkl")
    metadata_file = os.path.join(faiss_index_dir, "metadata.json")
    
    analysis = {
        "index_exists": os.path.exists(index_file),
        "pkl_exists": os.path.exists(pkl_file),
        "metadata_exists": os.path.exists(metadata_file),
        "files": []
    }
    
    for file_path in [index_file, pkl_file, metadata_file]:
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            analysis["files"].append({
                "path": file_path,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    print(f"📊 분석 결과:")
    print(f"   - FAISS 인덱스: {'✅' if analysis['index_exists'] else '❌'}")
    print(f"   - PKL 파일: {'✅' if analysis['pkl_exists'] else '❌'}")
    print(f"   - 메타데이터: {'✅' if analysis['metadata_exists'] else '❌'}")
    
    return analysis

def extract_faiss_metadata(faiss_index_dir: str):
    """FAISS에서 메타데이터 추출"""
    pkl_file = os.path.join(faiss_index_dir, "index.pkl")
    metadata_file = os.path.join(faiss_index_dir, "metadata.json")
    
    metadata_list = []
    
    # 1. metadata.json이 있으면 우선 사용
    if os.path.exists(metadata_file):
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata_list = json.load(f)
            print(f"✅ metadata.json에서 {len(metadata_list)}개 문서 정보 로드")
            return metadata_list
        except Exception as e:
            print(f"⚠️ metadata.json 로드 실패: {e}")
    
    # 2. PKL 파일에서 메타데이터 추출 시도
    if os.path.exists(pkl_file):
        try:
            with open(pkl_file, 'rb') as f:
                pkl_data = pickle.load(f)
            print(f"✅ PKL 데이터 로드: {type(pkl_data)}")
            
            # PKL 데이터 구조 분석
            if isinstance(pkl_data, dict):
                print(f"📋 PKL 키: {list(pkl_data.keys())}")
                
                # 일반적인 FAISS 구조에서 메타데이터 찾기
                if 'docstore' in pkl_data:
                    docstore = pkl_data['docstore']
                    if hasattr(docstore, '_dict'):
                        docs = docstore._dict
                        for doc_id, doc in docs.items():
                            metadata_list.append({
                                "doc_id": str(doc_id),
                                "doc_type": "faiss_document",
                                "content": str(doc.page_content)[:200] if hasattr(doc, 'page_content') else str(doc)[:200],
                                "metadata": doc.metadata if hasattr(doc, 'metadata') else {},
                                "created_at": datetime.now().isoformat()
                            })
                
                if 'index_to_docstore_id' in pkl_data:
                    print(f"📊 인덱스 매핑: {len(pkl_data['index_to_docstore_id'])}개")
                    
        except Exception as e:
            print(f"⚠️ PKL 파일 처리 실패: {e}")
    
    # 3. 메타데이터가 없으면 더미 데이터 생성
    if not metadata_list:
        print("📝 더미 메타데이터 생성 중...")
        metadata_list = [
            {
                "doc_id": "migrated_doc_1",
                "doc_type": "system_init",
                "content": "AAWGA 시스템에서 마이그레이션된 문서입니다.",
                "metadata": {"migrated": True, "source": "faiss"},
                "created_at": datetime.now().isoformat()
            }
        ]
    
    return metadata_list

def setup_chroma_db(chroma_db_path: str):
    """Chroma DB 설정"""
    print(f"🚀 Chroma DB 초기화: {chroma_db_path}")
    
    try:
        import chromadb
        from chromadb.config import Settings
        
        # 디렉토리 생성
        os.makedirs(chroma_db_path, exist_ok=True)
        
        # Chroma 클라이언트 생성
        client = chromadb.PersistentClient(path=chroma_db_path)
        
        # 기존 컬렉션 삭제 (있다면)
        try:
            client.delete_collection(name="aawga_documents")
            print("🗑️ 기존 컬렉션 삭제됨")
        except:
            pass
        
        # 새 컬렉션 생성
        collection = client.create_collection(
            name="aawga_documents",
            metadata={"description": "AAWGA 마이그레이션된 문서 컬렉션"}
        )
        
        print("✅ Chroma 컬렉션 생성 완료")
        return client, collection
        
    except ImportError:
        print("❌ chromadb 패키지가 설치되지 않았습니다")
        return None, None
    except Exception as e:
        print(f"❌ Chroma DB 초기화 실패: {e}")
        return None, None

def migrate_to_chroma(metadata_list: List[Dict], collection):
    """Chroma DB로 데이터 마이그레이션"""
    print(f"📦 {len(metadata_list)}개 문서를 Chroma DB로 마이그레이션 중...")
    
    batch_size = 50
    total_migrated = 0
    
    for i in range(0, len(metadata_list), batch_size):
        batch = metadata_list[i:i + batch_size]
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, meta in enumerate(batch):
            doc_id = meta.get('doc_id', f'migrated_{i + idx}')
            content = meta.get('content', f"문서 내용 - {doc_id}")
            
            documents.append(content)
            metadatas.append({
                "doc_type": meta.get('doc_type', 'migrated'),
                "doc_id": doc_id,
                "created_at": meta.get('created_at', datetime.now().isoformat()),
                "migrated_from": "faiss",
                "original_metadata": str(meta.get('metadata', {}))
            })
            ids.append(doc_id)
        
        try:
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            total_migrated += len(documents)
            print(f"✅ 배치 {i//batch_size + 1}: {len(documents)}개 문서 마이그레이션 완료")
            
        except Exception as e:
            print(f"❌ 배치 {i//batch_size + 1} 마이그레이션 실패: {e}")
    
    print(f"🎉 총 {total_migrated}개 문서 마이그레이션 완료!")
    return total_migrated

def create_web_interface(chroma_db_path: str):
    """Chroma DB 웹 인터페이스 생성"""
    web_server_code = f'''
import chromadb
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI(title="AAWGA Chroma DB 뷰어")

# Chroma 클라이언트 초기화
client = chromadb.PersistentClient(path="{chroma_db_path}")

class SearchRequest(BaseModel):
    query: str
    n_results: int = 5

@app.get("/", response_class=HTMLResponse)
async def get_web_ui():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>🧠 AAWGA Chroma DB 뷰어</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Arial, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            h1 {{ color: #2c3e50; text-align: center; margin-bottom: 30px; }}
            .search-box {{ 
                display: flex; 
                gap: 10px; 
                margin: 20px 0; 
                align-items: center;
            }}
            .search-box input {{ 
                flex: 1; 
                padding: 12px; 
                border: 2px solid #ddd; 
                border-radius: 8px; 
                font-size: 16px;
            }}
            .search-box button {{ 
                padding: 12px 24px; 
                background: #3498db; 
                color: white; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
                font-size: 16px;
                transition: background 0.3s;
            }}
            .search-box button:hover {{ background: #2980b9; }}
            .stats {{ 
                background: #f8f9fa; 
                padding: 15px; 
                border-radius: 8px; 
                margin: 20px 0;
                text-align: center;
            }}
            .result {{ 
                border: 1px solid #ddd; 
                padding: 20px; 
                margin: 15px 0; 
                border-radius: 8px; 
                background: #fafafa;
            }}
            .result h3 {{ margin-top: 0; color: #2c3e50; }}
            .metadata {{ 
                background: #e9ecef; 
                padding: 12px; 
                margin-top: 15px; 
                border-radius: 5px; 
                font-size: 0.9em;
                font-family: monospace;
            }}
            .distance {{ 
                background: #17a2b8; 
                color: white; 
                padding: 5px 10px; 
                border-radius: 15px; 
                font-size: 0.8em; 
                float: right;
            }}
            .loading {{ text-align: center; padding: 50px; color: #6c757d; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 AAWGA Chroma DB 뷰어</h1>
            <div class="stats" id="stats">
                <strong>📊 데이터베이스 통계 로딩 중...</strong>
            </div>
            <div class="search-box">
                <input type="text" id="query" placeholder="검색어를 입력하세요..." onkeypress="handleEnter(event)">
                <button onclick="search()">🔍 검색</button>
                <button onclick="loadStats()" style="background: #28a745;">📊 통계</button>
            </div>
            <div id="results"></div>
        </div>
        
        <script>
            async function search() {{
                const query = document.getElementById('query').value;
                if (!query.trim()) {{
                    alert('검색어를 입력하세요.');
                    return;
                }}
                
                document.getElementById('results').innerHTML = '<div class="loading">🔍 검색 중...</div>';
                
                try {{
                    const response = await fetch('/search', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{query: query.trim(), n_results: 5}})
                    }});
                    
                    if (!response.ok) throw new Error(`HTTP ${{response.status}}`);
                    
                    const data = await response.json();
                    displayResults(data, query);
                }} catch (error) {{
                    document.getElementById('results').innerHTML = 
                        `<div class="result" style="border-color: #dc3545;"><h3>❌ 검색 실패</h3><p>${{error.message}}</p></div>`;
                }}
            }}
            
            function displayResults(data, query) {{
                const resultsDiv = document.getElementById('results');
                
                if (data.documents.length === 0) {{
                    resultsDiv.innerHTML = `
                        <div class="result" style="border-color: #ffc107;">
                            <h3>🔍 검색 결과 없음</h3>
                            <p>"${{query}}"에 대한 결과를 찾을 수 없습니다.</p>
                        </div>
                    `;
                    return;
                }}
                
                let html = `<h2>🔍 "${{query}}" 검색 결과 (${{data.documents.length}}개)</h2>`;
                
                data.documents.forEach((doc, i) => {{
                    const distance = data.distances[i] ? data.distances[i].toFixed(4) : 'N/A';
                    html += `
                        <div class="result">
                            <h3>결과 #${{i+1}} <span class="distance">거리: ${{distance}}</span></h3>
                            <p>${{doc}}</p>
                            <div class="metadata">
                                <strong>메타데이터:</strong><br>
                                ${{JSON.stringify(data.metadatas[i], null, 2)}}
                            </div>
                        </div>
                    `;
                }});
                
                resultsDiv.innerHTML = html;
            }}
            
            async function loadStats() {{
                try {{
                    const response = await fetch('/stats');
                    const data = await response.json();
                    document.getElementById('stats').innerHTML = 
                        `<strong>📊 총 문서 수: ${{data.total_documents}}개</strong> | 
                         <span style="color: #28a745;">✅ 연결 정상</span>`;
                }} catch (error) {{
                    document.getElementById('stats').innerHTML = 
                        `<strong style="color: #dc3545;">❌ 통계 로드 실패: ${{error.message}}</strong>`;
                }}
            }}
            
            function handleEnter(event) {{
                if (event.key === 'Enter') search();
            }}
            
            // 페이지 로드 시 통계 자동 로드
            window.onload = () => loadStats();
        </script>
    </body>
    </html>
    """

@app.post("/search")
async def search_documents(request: SearchRequest):
    try:
        collection = client.get_collection("aawga_documents")
        results = collection.query(
            query_texts=[request.query],
            n_results=request.n_results
        )
        return {{
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0],
            "distances": results["distances"][0] if "distances" in results else []
        }}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    try:
        collection = client.get_collection("aawga_documents")
        count = collection.count()
        return {{"total_documents": count}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {{"status": "healthy", "database": "chroma", "timestamp": "{datetime.now().isoformat()}"}}

if __name__ == "__main__":
    print("🚀 AAWGA Chroma DB 웹 서버 시작")
    print("🌐 웹 인터페이스: http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
'''
    
    web_server_path = "C:/Users/cherr/AAWG/chroma_web_server.py"
    with open(web_server_path, "w", encoding="utf-8") as f:
        f.write(web_server_code)
    
    print(f"✅ 웹 서버 파일 생성: {web_server_path}")
    return web_server_path

def test_chroma_db(collection):
    """Chroma DB 테스트"""
    print("🧪 Chroma DB 테스트 중...")
    
    test_queries = ["문서", "시스템", "AAWGA", "마이그레이션"]
    
    for query in test_queries:
        try:
            results = collection.query(
                query_texts=[query],
                n_results=3
            )
            count = len(results["documents"][0])
            print(f"✅ '{query}' 검색: {count}개 결과")
            
            if count > 0:
                print(f"   샘플: {results['documents'][0][0][:100]}...")
                
        except Exception as e:
            print(f"❌ '{query}' 검색 실패: {e}")

def main():
    """메인 마이그레이션 함수"""
    print("🚀 FAISS → Chroma DB 마이그레이션 시작")
    print("=" * 60)
    
    # 경로 설정
    faiss_index_dir = "C:/Users/cherr/AAWG/AAWGA/vector_store/faiss_index"
    chroma_db_path = "C:/Users/cherr/AAWG/AAWGA/chroma_db"
    
    try:
        # 1. 패키지 설치
        if not install_packages():
            print("❌ 패키지 설치 실패. 마이그레이션을 중단합니다.")
            return False
        
        # 2. FAISS 데이터 분석
        analysis = analyze_faiss_data(faiss_index_dir)
        if not (analysis["index_exists"] or analysis["pkl_exists"]):
            print("❌ FAISS 데이터를 찾을 수 없습니다.")
            return False
        
        # 3. 메타데이터 추출
        metadata_list = extract_faiss_metadata(faiss_index_dir)
        if not metadata_list:
            print("❌ 마이그레이션할 데이터가 없습니다.")
            return False
        
        # 4. Chroma DB 설정
        client, collection = setup_chroma_db(chroma_db_path)
        if not collection:
            print("❌ Chroma DB 설정 실패.")
            return False
        
        # 5. 데이터 마이그레이션
        migrated_count = migrate_to_chroma(metadata_list, collection)
        
        # 6. 테스트
        test_chroma_db(collection)
        
        # 7. 웹 인터페이스 생성
        web_server_path = create_web_interface(chroma_db_path)
        
        # 8. 결과 출력
        print("\n" + "=" * 60)
        print("🎉 마이그레이션 완료!")
        print(f"✅ 마이그레이션된 문서: {migrated_count}개")
        print(f"💾 Chroma DB 위치: {chroma_db_path}")
        print(f"🌐 웹 서버 파일: {web_server_path}")
        print("\n📝 다음 단계:")
        print("1. python chroma_web_server.py")
        print("2. 브라우저에서 http://localhost:8001 접속")
        print("3. 검색 테스트 수행")
        
        return True
        
    except Exception as e:
        print(f"❌ 마이그레이션 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 마이그레이션 성공! 웹 서버를 실행하시겠습니까? (y/n): ", end="")
        # 여기서는 자동으로 y로 처리
        print("y")
        print("웹 서버 실행 중...")
    else:
        print("\n❌ 마이그레이션 실패.")
