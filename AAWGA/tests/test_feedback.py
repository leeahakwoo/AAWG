# tests/test_feedback.py

import pytest
import requests
import json
from typing import Dict, Any

API_URL = "http://127.0.0.1:8000"

@pytest.fixture
def sample_feedback():
    return {
        "instruction": "테스트 지시사항",
        "original_content": "테스트 원본 내용",
        "generated_result": {
            "requirements": ["테스트 요구사항 1", "테스트 요구사항 2"],
            "testcases": ["테스트케이스 1", "테스트케이스 2"],
            "traceability": ["추적성 항목 1", "추적성 항목 2"]
        },
        "user_feedback": "테스트 피드백입니다",
        "rating": 4
    }

@pytest.fixture
def created_feedback_id(sample_feedback):
    """피드백 생성 후 ID 반환, 테스트 후 정리"""
    response = requests.post(f"{API_URL}/feedback/", json=sample_feedback)
    if response.status_code == 200:
        feedback_id = response.json()["id"]
        yield feedback_id
        # 테스트 후 정리 (현재는 삭제 API가 없으므로 생략)
    else:
        pytest.skip("피드백 생성 실패")

def test_create_feedback(sample_feedback):
    """피드백 생성 테스트"""
    response = requests.post(f"{API_URL}/feedback/", json=sample_feedback)
    assert response.status_code == 200
    
    feedback = response.json()
    assert feedback["instruction"] == sample_feedback["instruction"]
    assert feedback["user_feedback"] == sample_feedback["user_feedback"]
    assert feedback["rating"] == sample_feedback["rating"]
    assert feedback["generated_result"] == sample_feedback["generated_result"]

def test_create_feedback_with_template():
    """템플릿 ID가 포함된 피드백 생성 테스트"""
    # 먼저 템플릿 생성
    template_data = {
        "name": "테스트 템플릿",
        "description": "테스트용 템플릿",
        "category": "requirements",
        "content": {"prompt": "테스트 프롬프트"},
        "is_default": False
    }
    
    template_response = requests.post(f"{API_URL}/templates/", json=template_data)
    if template_response.status_code == 200:
        template_id = template_response.json()["id"]
        
        # 템플릿 ID가 포함된 피드백 생성
        feedback_with_template = {
            "template_id": template_id,
            "instruction": "템플릿 사용 테스트",
            "original_content": "테스트 내용",
            "generated_result": {"requirements": ["테스트"]},
            "user_feedback": "템플릿 테스트 피드백",
            "rating": 5
        }
        
        response = requests.post(f"{API_URL}/feedback/", json=feedback_with_template)
        assert response.status_code == 200
        
        feedback = response.json()
        assert feedback["template_id"] == template_id
        
        # 정리
        requests.delete(f"{API_URL}/templates/{template_id}")
    else:
        pytest.skip("템플릿 생성 실패")

def test_get_feedback():
    """피드백 목록 조회 테스트"""
    response = requests.get(f"{API_URL}/feedback/")
    assert response.status_code == 200
    
    feedback_list = response.json()
    assert isinstance(feedback_list, list)

def test_get_feedback_with_limit():
    """제한된 개수의 피드백 조회 테스트"""
    response = requests.get(f"{API_URL}/feedback/?limit=5")
    assert response.status_code == 200
    
    feedback_list = response.json()
    assert isinstance(feedback_list, list)
    assert len(feedback_list) <= 5

def test_feedback_required_fields():
    """필수 필드 검증 테스트"""
    # 필수 필드가 없는 경우
    incomplete_feedback = {
        "instruction": "테스트",
        # original_content 누락
        "generated_result": {"test": "data"},
        # user_feedback 누락
        "rating": 3
    }
    
    response = requests.post(f"{API_URL}/feedback/", json=incomplete_feedback)
    # 현재는 400 에러가 발생해야 하지만, 실제 구현에 따라 다를 수 있음
    assert response.status_code in [400, 422]

def test_feedback_rating_validation():
    """평점 검증 테스트"""
    # 유효하지 않은 평점
    invalid_rating_feedback = {
        "instruction": "테스트",
        "original_content": "테스트 내용",
        "generated_result": {"test": "data"},
        "user_feedback": "테스트 피드백",
        "rating": 6  # 1-5 범위를 벗어남
    }
    
    response = requests.post(f"{API_URL}/feedback/", json=invalid_rating_feedback)
    # 현재는 400 에러가 발생해야 하지만, 실제 구현에 따라 다를 수 있음
    assert response.status_code in [400, 422]

def test_feedback_without_rating():
    """평점이 없는 피드백 생성 테스트"""
    feedback_without_rating = {
        "instruction": "테스트 지시사항",
        "original_content": "테스트 내용",
        "generated_result": {"test": "data"},
        "user_feedback": "테스트 피드백"
        # rating 필드 없음
    }
    
    response = requests.post(f"{API_URL}/feedback/", json=feedback_without_rating)
    assert response.status_code == 200
    
    feedback = response.json()
    assert "rating" not in feedback or feedback["rating"] is None

def test_feedback_json_validation():
    """JSON 형식 검증 테스트"""
    # 잘못된 JSON 형식
    invalid_json_feedback = {
        "instruction": "테스트",
        "original_content": "테스트 내용",
        "generated_result": "잘못된 형식",  # dict가 아닌 string
        "user_feedback": "테스트 피드백",
        "rating": 3
    }
    
    response = requests.post(f"{API_URL}/feedback/", json=invalid_json_feedback)
    # 현재는 400 에러가 발생해야 하지만, 실제 구현에 따라 다를 수 있음
    assert response.status_code in [400, 422] 