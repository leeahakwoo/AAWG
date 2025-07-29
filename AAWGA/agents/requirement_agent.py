import os
from typing import List
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import HumanMessage

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