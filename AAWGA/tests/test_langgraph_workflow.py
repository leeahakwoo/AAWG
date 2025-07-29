# tests/test_langgraph_workflow.py

import pytest
from agents.langgraph_workflow import graph

@pytest.fixture
def sample_input():
    # 실제 문서가 아니라 단순 텍스트 청크로 테스트
    return "테스트용 문서 내용"

def test_langgraph_workflow_structure(sample_input):
    """
    graph.invoke가 올바른 키들을 반환하는지 확인
    """
    output = graph.invoke({"input": sample_input})
    # 요구사항, 테스트케이스, 추적성 매트릭스가 모두 있어야 함
    assert "requirements" in output, "requirements 키가 없습니다"
    assert "testcases"   in output, "testcases 키가 없습니다"
    assert "traceability" in output, "traceability 키가 없습니다"

def test_requirements_type(sample_input):
    """
    requirements가 리스트 타입인지 확인
    """
    output = graph.invoke({"input": sample_input})
    assert isinstance(output["requirements"], list)
    # 최소 하나의 항목이라도 생성됐으면 좋겠지만
    # 실제 함수 로직에 따라 유동적이므로 빈 리스트도 허용

def test_testcases_type(sample_input):
    """
    testcases가 리스트 타입인지 확인
    """
    output = graph.invoke({"input": sample_input})
    assert isinstance(output["testcases"], list)

def test_traceability_type(sample_input):
    """
    traceability가 리스트 타입인지 확인
    """
    output = graph.invoke({"input": sample_input})
    assert isinstance(output["traceability"], list)
