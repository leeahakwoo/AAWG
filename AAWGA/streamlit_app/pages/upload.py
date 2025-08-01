import os
import sys
from dotenv import load_dotenv
import streamlit as st

# ─── .env 자동 로드 ─────────────────────────────────────────────
load_dotenv()  # .env 파일에 정의된 키들(PINECONE_API_KEY 등)을 os.environ에 주입
# ───────────────────────────────────────────────────────────────

# ─── 프로젝트 루트를 모듈 검색 경로에 추가 ────────────────────────
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# ───────────────────────────────────────────────────────────────

# 더미 모드 환경변수가 없다면 기본으로 true
os.environ.setdefault('USE_DUMMY_AGENT', 'true')

from agents.langgraph_dynamic import graph

st.set_page_config(page_title="AAWGA Upload", layout="wide")

st.title("AAWGA Workflow Upload")

uploaded = st.file_uploader(
    "문서를 업로드해주세요", 
    type=["txt", "pdf", "docx", "xlsx"],
    help="Limit 200MB per file • TXT, PDF, DOCX, XLSX"
)

instr = st.selectbox(
    "할 작업을 선택하세요",
    [
        "문서에서 요구사항만 생성해 줘",
        "테스트케이스만 생성해 줘",
        "추적성 매트릭스만 생성해 줘",
        "요구사항과 테스트케이스 둘 다 생성해 줘",
        "요구사항, 테스트케이스, 추적성 매트릭스 모두 생성해 줘"
    ],
    help="원하는 결과를 골라주세요"
)

if uploaded and st.button("실행"):
    # 파일 내용 읽기 (텍스트 기반 처리)
    try:
        raw = uploaded.read()
        content = raw.decode("utf-8", errors="ignore")
    except Exception:
        content = f"[Non-text file] {uploaded.name}"

    with st.spinner("에이전트를 실행 중입니다..."):
        output = graph.invoke({
            "instruction": instr,
            "content": content
        })

    st.success("완료!")
    # 결과 출력
    if output.get("requirements"):
        st.subheader("✅ 요구사항")
        st.write(output["requirements"])
    if output.get("testcases"):
        st.subheader("✅ 테스트케이스")
        st.write(output["testcases"])
    if output.get("traceability"):
        st.subheader("✅ 추적성 매트릭스")
        st.json(output["traceability"])
