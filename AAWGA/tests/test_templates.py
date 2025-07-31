# tests/test_templates.py

import pytest
import requests
import json
from typing import Dict, Any

API_URL = "http://127.0.0.1:8000"

@pytest.fixture
def sample_template():
    return {
        "name": "테스트 템플릿",
        "description": "테스트용 템플릿입니다",
        "category": "requirements",
        "content": {
            "prompt": "테스트 프롬프트",
            "format": "테스트 형식",
            "output_type": "list"
        },
        "is_default": False
    }

@pytest.fixture
def created_template_id(sample_template):
    """템플릿 생성 후 ID 반환, 테스트 후 정리"""
    response = requests.post(f"{API_URL}/templates/", json=sample_template)
    if response.status_code == 200:
        template_id = response.json()["id"]
        yield template_id
        # 테스트 후 정리
        requests.delete(f"{API_URL}/templates/{template_id}")
    else:
        pytest.skip("템플릿 생성 실패")

def test_create_template(sample_template):
    """템플릿 생성 테스트"""
    response = requests.post(f"{API_URL}/templates/", json=sample_template)
    assert response.status_code == 200
    
    template = response.json()
    assert template["name"] == sample_template["name"]
    assert template["category"] == sample_template["category"]
    assert template["content"] == sample_template["content"]
    
    # 정리
    requests.delete(f"{API_URL}/templates/{template['id']}")

def test_get_templates():
    """템플릿 목록 조회 테스트"""
    response = requests.get(f"{API_URL}/templates/")
    assert response.status_code == 200
    
    templates = response.json()
    assert isinstance(templates, list)

def test_get_template_by_id(created_template_id):
    """특정 템플릿 조회 테스트"""
    response = requests.get(f"{API_URL}/templates/{created_template_id}")
    assert response.status_code == 200
    
    template = response.json()
    assert template["id"] == created_template_id

def test_update_template(created_template_id):
    """템플릿 수정 테스트"""
    update_data = {
        "name": "수정된 템플릿",
        "description": "수정된 설명"
    }
    
    response = requests.put(f"{API_URL}/templates/{created_template_id}", json=update_data)
    assert response.status_code == 200
    
    template = response.json()
    assert template["name"] == update_data["name"]
    assert template["description"] == update_data["description"]

def test_delete_template(created_template_id):
    """템플릿 삭제 테스트"""
    response = requests.delete(f"{API_URL}/templates/{created_template_id}")
    assert response.status_code == 200
    
    # 삭제 확인
    get_response = requests.get(f"{API_URL}/templates/{created_template_id}")
    assert get_response.status_code == 404

def test_get_templates_by_category():
    """카테고리별 템플릿 조회 테스트"""
    response = requests.get(f"{API_URL}/templates/?category=requirements")
    assert response.status_code == 200
    
    templates = response.json()
    for template in templates:
        assert template["category"] == "requirements"

def test_create_default_template():
    """기본 템플릿 생성 테스트"""
    default_template = {
        "name": "기본 요구사항 템플릿",
        "description": "기본 템플릿입니다",
        "category": "requirements",
        "content": {
            "prompt": "기본 프롬프트",
            "format": "기본 형식"
        },
        "is_default": True
    }
    
    response = requests.post(f"{API_URL}/templates/", json=default_template)
    assert response.status_code == 200
    
    template = response.json()
    assert template["is_default"] == True
    
    # 정리
    requests.delete(f"{API_URL}/templates/{template['id']}")

def test_get_default_template():
    """기본 템플릿 조회 테스트"""
    # 먼저 기본 템플릿 생성
    default_template = {
        "name": "테스트 기본 템플릿",
        "description": "테스트용 기본 템플릿",
        "category": "testcases",
        "content": {"prompt": "테스트 프롬프트"},
        "is_default": True
    }
    
    create_response = requests.post(f"{API_URL}/templates/", json=default_template)
    if create_response.status_code == 200:
        template_id = create_response.json()["id"]
        
        # 기본 템플릿 조회
        response = requests.get(f"{API_URL}/templates/default/testcases")
        assert response.status_code == 200
        
        template = response.json()
        assert template["category"] == "testcases"
        assert template["is_default"] == True
        
        # 정리
        requests.delete(f"{API_URL}/templates/{template_id}")
    else:
        pytest.skip("기본 템플릿 생성 실패") 