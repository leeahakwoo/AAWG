import os
from typing import List
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import HumanMessage
from langchain.agents import Tool, AgentExecutor, initialize_agent
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

def generate_requirements(input_text: str) -> List[str]:
    # 매 호출마다 dummy 모드 확인
    if os.getenv("USE_DUMMY_AGENT", "").lower() == "true":
        return [f"[DUMMY] 요구사항 예시: {input_text}"]

    # 실제 RAG+LLM 로직
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.create_documents([input_text])
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.from_documents(docs, embeddings)
    results = vectorstore.similarity_search(input_text, k=3)
    context = "\n---\n".join(doc.page_content for doc in results)

    llm = ChatOpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "당신은 소프트웨어 요구사항 분석가입니다.\n"
        "[문맥]\n" + context + "\n\n"
        "[요구사항 생성]\n" + input_text + "\n\n"
        "위 입력을 기반으로 요구사항을 번호 매겨서 나열해 주세요."
    )
    resp = llm([HumanMessage(content=prompt)])
    return [line.strip("- \r ") for line in resp.content.splitlines() if line.strip()]

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
