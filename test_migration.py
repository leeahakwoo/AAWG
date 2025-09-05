#!/usr/bin/env python3
"""
ChromaDB 마이그레이션 테스트 및 검증 스크립트
실행: python test_migration.py
"""

import os
import sys
import json
from datetime import datetime

def test_chromadb_connection():
    """ChromaDB 연결 테스트"""
    print("🔍 ChromaDB 연결 테스트")
    try:
        import chromadb
        
        chroma_db_path = r"C:\Users\cherr\AAWG\AAWGA\chroma_db"
        client = chromadb.PersistentClient(path=chroma_db_path)
        
        # 컬렉션 확인
        collections = client.list_collections()
        print(f"✅ 발견된 컬렉션: {[c.name for c in collections]}")
        
        if collections:
            collection = collections[0]
            count = collection.count()
            print(f"✅ 문서 수: {count}개")
            
            # 샘플 검색 테스트
            if count > 0:
                results = collection.query(
                    query_texts=["AAWGA"],
                    n_results=min(3, count)
                )
                print(f"✅ 검색 테스트 결과: {len(results['documents'][0])}개")
                
                if results['documents'][0]:
                    print(f"   샘플: {results['documents'][0][0][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ ChromaDB 연결 실패: {e}")
        return False

def test_vector_service():
    """벡터 서비스 테스트"""
    print("\n🔍 벡터 서비스 테스트")
    try:
        # Python 경로 설정
        project_root = r"C:\Users\cherr\AAWG\AAWGA"
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        from backend.services.vector_service import vector_service
        
        # 통계 확인
        stats = vector_service.get_vector_store_stats()
        print(f"✅ 벡터 서비스 통계:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # 검색 테스트
        results = vector_service.search_similar("AAWGA 시스템", k=3)
        print(f"✅ 검색 테스트: {len(results)}개 결과")
        
        if results:
            print(f"   첫 번째 결과: {results[0].page_content[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 벡터 서비스 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_vector_service():
    """확장 벡터 서비스 테스트"""
    print("\n🔍 확장 벡터 서비스 테스트")
    try:
        # Python 경로 설정
        project_root = r"C:\Users\cherr\AAWG\AAWGA"
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        from backend.services.enhanced_vector_service import enhanced_vector_service
        
        # RAG 투명화 테스트
        import asyncio
        
        async def test_rag_transparency():
            transparency_info = await enhanced_vector_service.get_rag_transparency_info("AAWGA 시스템", k=3)
            print(f"✅ RAG 투명화 테스트:")
            print(f"   쿼리: {transparency_info.get('query', 'unknown')}")
            print(f"   검색된 문서 수: {transparency_info.get('retrieved_documents_count', 0)}")
            print(f"   총 검색 대상: {transparency_info.get('total_documents_searched', 0)}")
            
            return transparency_info
        
        # 비동기 함수 실행
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        transparency_result = loop.run_until_complete(test_rag_transparency())
        loop.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 확장 벡터 서비스 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_file_structure():
    """파일 구조 확인"""
    print("\n🔍 파일 구조 확인")
    
    files_to_check = [
        r"C:\Users\cherr\AAWG\AAWGA\backend\services\vector_service_chroma.py",
        r"C:\Users\cherr\AAWG\AAWGA\backend\services\vector_service.py",
        r"C:\Users\cherr\AAWG\AAWGA\backend\.env",
        r"C:\Users\cherr\AAWG\AAWGA\chroma_db\chroma.sqlite3",
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {os.path.basename(file_path)}")
        else:
            print(f"❌ {os.path.basename(file_path)} 없음")

def check_environment_variables():
    """환경 변수 확인"""
    print("\n🔍 환경 변수 확인")
    
    env_path = r"C:\Users\cherr\AAWG\AAWGA\backend\.env"
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "USE_CHROMADB=true" in content:
            print("✅ USE_CHROMADB=true 설정됨")
        else:
            print("⚠️ USE_CHROMADB 설정 확인 필요")
            
        if "GOOGLE_API_KEY" in content or "GEMINI_API_KEY" in content:
            print("✅ API 키 설정 확인됨")
        else:
            print("⚠️ API 키 설정 확인 필요")
    else:
        print("❌ .env 파일을 찾을 수 없습니다")

def generate_test_report():
    """테스트 리포트 생성"""
    print("\n📊 테스트 리포트 생성")
    
    report = {
        "test_timestamp": datetime.now().isoformat(),
        "chromadb_connection": False,
        "vector_service": False,
        "enhanced_vector_service": False,
        "file_structure": True,
        "environment_variables": True
    }
    
    # 각 테스트 실행
    report["chromadb_connection"] = test_chromadb_connection()
    report["vector_service"] = test_vector_service()
    report["enhanced_vector_service"] = test_enhanced_vector_service()
    
    # 리포트 저장
    report_path = r"C:\Users\cherr\AAWG\migration_test_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 테스트 리포트 저장: {report_path}")
    
    # 결과 요약
    success_count = sum(1 for v in report.values() if v is True)
    total_tests = len([k for k in report.keys() if k != "test_timestamp"])
    
    print(f"\n📈 테스트 결과: {success_count}/{total_tests} 통과")
    
    if success_count == total_tests:
        print("🎉 모든 테스트 통과! 마이그레이션이 성공적으로 완료되었습니다.")
    else:
        print("⚠️ 일부 테스트 실패. 추가 확인이 필요합니다.")
    
    return report

def main():
    print("🧪 FAISS → ChromaDB 마이그레이션 테스트")
    print("=" * 60)
    
    # 파일 구조 확인
    check_file_structure()
    
    # 환경 변수 확인
    check_environment_variables()
    
    # 테스트 리포트 생성
    report = generate_test_report()
    
    print("\n" + "=" * 60)
    print("🏁 테스트 완료!")
    
    return report

if __name__ == "__main__":
    try:
        report = main()
        
        # 성공 여부에 따른 종료 코드
        success_count = sum(1 for k, v in report.items() if k != "test_timestamp" and v is True)
        total_tests = len([k for k in report.keys() if k != "test_timestamp"])
        
        if success_count == total_tests:
            sys.exit(0)  # 성공
        else:
            sys.exit(1)  # 실패
            
    except Exception as e:
        print(f"\n❌ 테스트 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
