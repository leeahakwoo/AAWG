#!/usr/bin/env python3
"""
AAWGA Vector DB 상태 체크 스크립트
현재 FAISS와 ChromaDB 상태를 확인합니다.
실행: python check_vector_status.py
"""

import os
import json
from datetime import datetime

def check_faiss_status():
    """FAISS 상태 확인"""
    print("🔍 FAISS Vector DB 상태 확인")
    
    faiss_dir = r"C:\Users\cherr\AAWG\AAWGA\vector_store\faiss_index"
    faiss_files = ["index.faiss", "index.pkl", "metadata.json"]
    
    faiss_status = {
        "directory_exists": os.path.exists(faiss_dir),
        "files": {}
    }
    
    if faiss_status["directory_exists"]:
        for file_name in faiss_files:
            file_path = os.path.join(faiss_dir, file_name)
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                faiss_status["files"][file_name] = {
                    "exists": True,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                }
                print(f"  ✅ {file_name}: {stat.st_size} bytes")
            else:
                faiss_status["files"][file_name] = {"exists": False}
                print(f"  ❌ {file_name}: 없음")
    else:
        print("  ❌ FAISS 디렉토리가 존재하지 않습니다")
    
    return faiss_status

def check_chromadb_status():
    """ChromaDB 상태 확인"""
    print("\n🔍 ChromaDB 상태 확인")
    
    chroma_dir = r"C:\Users\cherr\AAWG\AAWGA\chroma_db"
    chroma_files = ["chroma.sqlite3", "init_chroma.py", "web_server.py"]
    
    chromadb_status = {
        "directory_exists": os.path.exists(chroma_dir),
        "files": {},
        "collections": [],
        "document_count": 0
    }
    
    if chromadb_status["directory_exists"]:
        print(f"  ✅ ChromaDB 디렉토리: {chroma_dir}")
        
        # 파일 확인
        for file_name in chroma_files:
            file_path = os.path.join(chroma_dir, file_name)
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                chromadb_status["files"][file_name] = {
                    "exists": True,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                }
                print(f"  ✅ {file_name}: {stat.st_size} bytes")
            else:
                chromadb_status["files"][file_name] = {"exists": False}
                print(f"  ❌ {file_name}: 없음")
        
        # ChromaDB 연결 시도
        try:
            import chromadb
            client = chromadb.PersistentClient(path=chroma_dir)
            collections = client.list_collections()
            
            chromadb_status["collections"] = [c.name for c in collections]
            print(f"  ✅ 컬렉션: {chromadb_status['collections']}")
            
            if collections:
                total_docs = sum(c.count() for c in collections)
                chromadb_status["document_count"] = total_docs
                print(f"  ✅ 총 문서 수: {total_docs}개")
            
        except Exception as e:
            print(f"  ⚠️ ChromaDB 연결 실패: {e}")
            chromadb_status["connection_error"] = str(e)
    else:
        print("  ❌ ChromaDB 디렉토리가 존재하지 않습니다")
    
    return chromadb_status

def check_application_config():
    """애플리케이션 설정 확인"""
    print("\n🔍 애플리케이션 설정 확인")
    
    config_status = {
        "vector_service_files": {},
        "environment_variables": {},
        "current_vector_db": "unknown"
    }
    
    # 벡터 서비스 파일들 확인
    service_files = [
        r"C:\Users\cherr\AAWG\AAWGA\backend\services\vector_service.py",
        r"C:\Users\cherr\AAWG\AAWGA\backend\services\vector_service_chroma.py",
        r"C:\Users\cherr\AAWG\AAWGA\backend\services\enhanced_vector_service.py"
    ]
    
    for file_path in service_files:
        file_name = os.path.basename(file_path)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            config_status["vector_service_files"][file_name] = {
                "exists": True,
                "uses_faiss": "FAISS" in content,
                "uses_chromadb": "chromadb" in content.lower(),
                "size": len(content)
            }
            print(f"  ✅ {file_name}")
            print(f"    - FAISS 사용: {'✅' if config_status['vector_service_files'][file_name]['uses_faiss'] else '❌'}")
            print(f"    - ChromaDB 사용: {'✅' if config_status['vector_service_files'][file_name]['uses_chromadb'] else '❌'}")
        else:
            config_status["vector_service_files"][file_name] = {"exists": False}
            print(f"  ❌ {file_name}: 없음")
    
    # 환경 변수 확인
    env_path = r"C:\Users\cherr\AAWG\AAWGA\backend\.env"
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
        
        # USE_CHROMADB 확인
        if "USE_CHROMADB" in env_content:
            for line in env_content.split('\n'):
                if line.startswith("USE_CHROMADB"):
                    use_chromadb = line.split('=')[1].strip().lower() == 'true'
                    config_status["environment_variables"]["USE_CHROMADB"] = use_chromadb
                    config_status["current_vector_db"] = "chromadb" if use_chromadb else "faiss"
                    print(f"  ✅ USE_CHROMADB: {use_chromadb}")
                    break
        else:
            config_status["environment_variables"]["USE_CHROMADB"] = None
            print("  ⚠️ USE_CHROMADB 설정이 없습니다")
        
        # API 키 확인
        api_key_exists = "GOOGLE_API_KEY" in env_content or "GEMINI_API_KEY" in env_content
        config_status["environment_variables"]["API_KEY"] = api_key_exists
        print(f"  ✅ API 키: {'설정됨' if api_key_exists else '없음'}")
        
    else:
        print("  ❌ .env 파일을 찾을 수 없습니다")
    
    return config_status

def generate_status_report():
    """전체 상태 리포트 생성"""
    print("\n" + "=" * 60)
    print("📊 AAWGA Vector DB 상태 리포트")
    print("=" * 60)
    
    # 각 상태 확인
    faiss_status = check_faiss_status()
    chromadb_status = check_chromadb_status()
    config_status = check_application_config()
    
    # 전체 리포트 구성
    full_report = {
        "timestamp": datetime.now().isoformat(),
        "faiss": faiss_status,
        "chromadb": chromadb_status,
        "application_config": config_status,
        "summary": {
            "faiss_active": faiss_status.get("directory_exists", False) and 
                           any(f.get("exists", False) for f in faiss_status.get("files", {}).values()),
            "chromadb_active": chromadb_status.get("directory_exists", False) and 
                              chromadb_status.get("document_count", 0) > 0,
            "current_vector_db": config_status.get("current_vector_db", "unknown"),
            "migration_needed": None
        }
    }
    
    # 마이그레이션 필요성 판단
    if full_report["summary"]["faiss_active"] and full_report["summary"]["chromadb_active"]:
        if full_report["summary"]["current_vector_db"] == "chromadb":
            full_report["summary"]["migration_needed"] = False
            migration_status = "✅ ChromaDB 사용 중 (마이그레이션 완료)"
        else:
            full_report["summary"]["migration_needed"] = True
            migration_status = "⚠️ FAISS 사용 중 (ChromaDB로 전환 필요)"
    elif full_report["summary"]["faiss_active"] and not full_report["summary"]["chromadb_active"]:
        full_report["summary"]["migration_needed"] = True
        migration_status = "❌ FAISS만 존재 (ChromaDB 마이그레이션 필요)"
    elif not full_report["summary"]["faiss_active"] and full_report["summary"]["chromadb_active"]:
        full_report["summary"]["migration_needed"] = False
        migration_status = "✅ ChromaDB만 존재 (마이그레이션 완료)"
    else:
        full_report["summary"]["migration_needed"] = True
        migration_status = "❌ 벡터 DB가 없음 (초기 설정 필요)"
    
    # 요약 출력
    print(f"\n📋 상태 요약:")
    print(f"  FAISS 활성: {'✅' if full_report['summary']['faiss_active'] else '❌'}")
    print(f"  ChromaDB 활성: {'✅' if full_report['summary']['chromadb_active'] else '❌'}")
    print(f"  현재 사용 중: {full_report['summary']['current_vector_db']}")
    print(f"  마이그레이션 상태: {migration_status}")
    
    # 권장 사항
    print(f"\n💡 권장 사항:")
    if full_report["summary"]["migration_needed"]:
        print("  1. 🚀_마이그레이션_실행.bat 파일을 실행하세요")
        print("  2. 또는 python execute_migration.py 를 실행하세요")
        print("  3. 마이그레이션 후 python test_migration.py 로 테스트하세요")
    else:
        print("  ✅ 마이그레이션이 완료되었습니다!")
        print("  📊 python test_migration.py 로 테스트해보세요")
    
    # 리포트 파일 저장
    report_path = r"C:\Users\cherr\AAWG\vector_db_status_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(full_report, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 상세 리포트 저장: {report_path}")
    
    return full_report

def main():
    print("🔍 AAWGA Vector DB 상태 체크")
    print("현재 시간: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    report = generate_status_report()
    
    print("\n" + "=" * 60)
    print("🏁 상태 체크 완료!")
    print("=" * 60)
    
    return report

if __name__ == "__main__":
    try:
        report = main()
        
        # 마이그레이션 필요 여부에 따른 종료 코드
        if report["summary"]["migration_needed"]:
            exit_code = 1  # 마이그레이션 필요
        else:
            exit_code = 0  # 정상 상태
        
        exit(exit_code)
        
    except Exception as e:
        print(f"\n❌ 상태 체크 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        exit(2)  # 오류 발생
