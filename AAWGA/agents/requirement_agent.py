# agents/requirement_agent.py
from langchain.agents import Tool, AgentExecutor, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.tools import tool

from backend.services.rag_search import search_documents

@tool
def get_context_from_docs(query: str) -> str:
    """문서에서 관련된 정보를 검색하여 반환합니다."""
    return search_documents(query)

# 요구사항 생성용 프롬프트 템플릿
requirement_template = PromptTemplate(
    input_variables=["input", "context"],
    template="""
당신은 소프트웨어 요구사항 분석가입니다. 다음 문맥 정보를 참고하여 사용자의 입력을 바탕으로 요구사항 명세서를 작성하세요.

[문맥 정보]
{context}

[사용자 입력]
{input}

[요구사항 명세서]
"""
)

def get_requirement_agent():
    llm = ChatOpenAI(temperature=0, model="gpt-4")

    tools = [get_context_from_docs]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )

    def run(input_text: str):
        context = search_documents(input_text)
        prompt = requirement_template.format(input=input_text, context=context)
        return agent.run(prompt)

    return run
