#!/usr/bin/env python3
"""
기본 템플릿 초기화 스크립트
MongoDB에 기본 템플릿들을 생성합니다.
"""

import requests
import json
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# 기본 템플릿 정의
DEFAULT_TEMPLATES = [
    {
        "name": "기본 요구사항 템플릿",
        "description": "일반적인 소프트웨어 요구사항 추출을 위한 기본 템플릿",
        "category": "requirements",
        "content": {
            "prompt": "다음 문서에서 소프트웨어 요구사항을 추출하여 정리해주세요. 각 요구사항은 명확하고 구체적으로 작성되어야 합니다.",
            "format": "목록 형태로 각 요구사항을 번호와 함께 정리",
            "output_type": "list"
        },
        "is_default": True
    },
    {
        "name": "기본 테스트케이스 템플릿",
        "description": "요구사항 기반 테스트케이스 생성을 위한 기본 템플릿",
        "category": "testcases",
        "content": {
            "prompt": "주어진 요구사항을 바탕으로 상세한 테스트케이스를 생성해주세요. 각 테스트케이스는 테스트 목적, 전제조건, 테스트 단계, 예상 결과를 포함해야 합니다.",
            "format": "테이블 형태로 테스트케이스 ID, 제목, 목적, 전제조건, 단계, 예상 결과를 정리",
            "output_type": "table"
        },
        "is_default": True
    },
    {
        "name": "기본 추적성 매트릭스 템플릿",
        "description": "요구사항과 테스트케이스 간의 추적성을 매핑하는 기본 템플릿",
        "category": "traceability",
        "content": {
            "prompt": "요구사항과 테스트케이스 간의 추적성 매트릭스를 생성해주세요. 각 요구사항이 어떤 테스트케이스로 검증되는지 명확히 매핑해야 합니다.",
            "format": "매트릭스 형태로 요구사항 ID와 테스트케이스 ID 간의 관계를 표시",
            "output_type": "matrix"
        },
        "is_default": True
    },
    {
        "name": "상세 요구사항 템플릿",
        "description": "기능적/비기능적 요구사항을 구분하여 상세히 추출하는 템플릿",
        "category": "requirements",
        "content": {
            "prompt": "문서에서 기능적 요구사항과 비기능적 요구사항을 구분하여 추출해주세요. 각 요구사항에 우선순위와 담당자를 명시하세요.",
            "format": "기능적/비기능적 요구사항을 구분하여 표 형태로 정리",
            "output_type": "table"
        },
        "is_default": False
    },
    {
        "name": "사용자 시나리오 기반 테스트케이스 템플릿",
        "description": "사용자 시나리오를 기반으로 한 테스트케이스 생성 템플릿",
        "category": "testcases",
        "content": {
            "prompt": "사용자 시나리오를 기반으로 테스트케이스를 생성해주세요. 정상 시나리오와 예외 시나리오를 모두 포함해야 합니다.",
            "format": "시나리오별로 테스트케이스를 그룹화하여 정리",
            "output_type": "grouped_list"
        },
        "is_default": False
    }
]

def create_template(template_data):
    """템플릿 생성"""
    try:
        response = requests.post(f"{API_URL}/templates/", json=template_data)
        if response.status_code == 200:
            print(f"✅ 템플릿 생성 성공: {template_data['name']}")
            return True
        else:
            print(f"❌ 템플릿 생성 실패: {template_data['name']} - {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 템플릿 생성 오류: {template_data['name']} - {str(e)}")
        return False

def check_api_connection():
    """API 연결 확인"""
    try:
        response = requests.get(f"{API_URL}/")
        return response.status_code == 200
    except:
        return False

def main():
    print("🚀 AAWGA 기본 템플릿 초기화 시작")
    
    # API 연결 확인
    if not check_api_connection():
        print(f"❌ API 서버에 연결할 수 없습니다: {API_URL}")
        print("FastAPI 서버가 실행 중인지 확인해주세요.")
        return
    
    print(f"✅ API 서버 연결 확인: {API_URL}")
    
    # 기존 템플릿 확인
    try:
        response = requests.get(f"{API_URL}/templates/")
        if response.status_code == 200:
            existing_templates = response.json()
            if existing_templates:
                print(f"⚠️  이미 {len(existing_templates)}개의 템플릿이 존재합니다.")
                overwrite = input("기본 템플릿을 다시 생성하시겠습니까? (y/N): ")
                if overwrite.lower() != 'y':
                    print("템플릿 생성이 취소되었습니다.")
                    return
    except Exception as e:
        print(f"⚠️  기존 템플릿 확인 중 오류: {str(e)}")
    
    # 기본 템플릿 생성
    success_count = 0
    for template in DEFAULT_TEMPLATES:
        if create_template(template):
            success_count += 1
    
    print(f"\n📊 템플릿 생성 완료: {success_count}/{len(DEFAULT_TEMPLATES)}")
    
    if success_count == len(DEFAULT_TEMPLATES):
        print("🎉 모든 기본 템플릿이 성공적으로 생성되었습니다!")
    else:
        print("⚠️  일부 템플릿 생성에 실패했습니다.")

if __name__ == "__main__":
    main() 