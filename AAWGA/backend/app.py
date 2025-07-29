from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.langgraph_dynamic import graph

app = FastAPI()

class RunRequest(BaseModel):
    instruction: str
    content: str

class RunResponse(BaseModel):
    requirements: list[str]
    testcases: list[str]
    traceability: list[str]

@app.post("/run", response_model=RunResponse)
def run_workflow(req: RunRequest):
    """
    instruction에 따라 필요한 에이전트를 호출하여 결과를 반환합니다.
    """
    try:
        # LangGraph 동적 워크플로우 실행
        output = graph.invoke({
            "instruction": req.instruction,
            "content": req.content
        })
        # 필요한 키가 없다면 빈 리스트로 보장
        return {
            "requirements": output.get("requirements", []),
            "testcases": output.get("testcases", []),
            "traceability": output.get("traceability", [])
        }
    except Exception as e:
        # 내부 오류는 HTTP 500로 반환
        raise HTTPException(status_code=500, detail=str(e))
