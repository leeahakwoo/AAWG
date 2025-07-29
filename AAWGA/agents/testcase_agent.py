import os
from typing import List
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

def generate_testcases(requirements: List[str]) -> List[str]:
    if os.getenv("USE_DUMMY_AGENT", "").lower() == "true":
        return [f"[DUMMY] 테스트케이스 예시: {req}" for req in requirements]

    llm = ChatOpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "당신은 테스트 엔지니어입니다. 다음 요구사항 각각에 대해 테스트케이스를 작성하세요:\n"
        + "\n".join(f"{i+1}. {req}" for i, req in enumerate(requirements))
    )
    resp = llm([HumanMessage(content=prompt)])
    return [line.strip("- \r ") for line in resp.content.splitlines() if line.strip()]