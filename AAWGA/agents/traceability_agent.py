import os
from typing import List, Dict
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import json

def generate_traceability(requirements: List[str], testcases: List[str]) -> List[Dict]:
    if os.getenv("USE_DUMMY_AGENT", "").lower() == "true":
        return [{"requirement": req, "testcases": []} for req in requirements]

    llm = ChatOpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "당신은 추적성 매트릭스 전문가입니다. 요구사항과 테스트케이스 매핑을 JSON으로 반환하세요.\n"
        "요구사항:\n" + "\n".join(f"{i+1}. {req}" for i, req in enumerate(requirements))
        + "\n테스트케이스:\n" + "\n".join(f"{j+1}. {tc}" for j, tc in enumerate(testcases))
    )
    resp = llm([HumanMessage(content=prompt)])
    try:
        return json.loads(resp.content)
    except json.JSONDecodeError:
        return []