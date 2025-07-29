import os
import pytest
from agents.langgraph_dynamic import graph

# 테스트 시 더미 모드 활성화
os.environ['USE_DUMMY_AGENT'] = 'true'

@pytest.mark.parametrize("instr, expected_keys", [
    ("문서에서 요구사항만 생성해 줘", ["requirements"]),
    ("테스트케이스만 생성해 줘",       ["testcases"]),
    ("추적성 매트릭스만 생성해 줘",   ["traceability"]),
    ("요구사항과 테스트케이스 둘 다 생성해 줘", ["requirements","testcases"]),
    ("요구사항, 테스트케이스, 추적성 매트릭스 생성해 줘", ["requirements","testcases","traceability"]),
])
def test_dynamic_invoke_keys(instr, expected_keys):
    """
    instruction에 따라 graph.invoke()가 올바른 키만 반환하는지 확인
    """
    output = graph.invoke({
        "instruction": instr,
        "content":     "샘플 텍스트"
    })
    # 반환 타입과 키 검증
    assert isinstance(output, dict)
    for key in expected_keys:
        assert key in output, f"'{instr}'에서 '{key}' 키가 누락되었습니다"
        assert isinstance(output[key], list), f"'{key}'의 값이 list가 아닙니다"
    # 불필요한 키가 없어야 함
    assert set(output.keys()) == set(expected_keys)
