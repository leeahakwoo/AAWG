# agents/langgraph_dynamic.py

from agents.requirement_agent import generate_requirements
from agents.testcase_agent    import generate_testcases
from agents.traceability_agent import generate_traceability

class StateGraph:
    def __init__(self):
        self.entry = None

    def state(self):
        def decorator(fn):
            return fn
        return decorator

    def set_entry_point(self, fn):
        self.entry = fn

    def compile(self):
        entry = self.entry
        class Graph:
            def invoke(self, data):
                # data: { "instruction": str, "content": str }
                state = {
                    "instruction": data["instruction"],
                    "content":     data["content"],
                }
                # 단일 상태만 실행
                out = entry(state)
                # 결과 리턴
                return out
        return Graph()

# 동적 실행 로직
builder = StateGraph()

@builder.state()
def dynamic_invoke(state):
    instr  = state["instruction"]
    content= state["content"]
    result = {}

    # 1) 요구사항 생성이 필요할 때
    if "요구사항" in instr:
        reqs = generate_requirements(content)
        result["requirements"] = reqs
    else:
        # 이후 단계에 필요하면 빈 리스트라도 넘겨 두기
        state["requirements"] = []

    # 2) 테스트케이스 생성이 필요할 때
    if "테스트케이스" in instr:
        # reqs가 없을 땐 빈 리스트
        reqs = result.get("requirements", state.get("requirements", []))
        tcs = generate_testcases(reqs)
        result["testcases"] = tcs

    # 3) 추적성 매트릭스 생성이 필요할 때
    if "추적성" in instr:
        # 이전 단계가 실행되지 않았다면 미리 수행
        reqs = result.get("requirements", state.get("requirements", []))
        tcs  = result.get("testcases",    generate_testcases(reqs))
        trace = generate_traceability(reqs, tcs)
        result["traceability"] = trace

    return result

builder.set_entry_point(dynamic_invoke)
graph = builder.compile()
