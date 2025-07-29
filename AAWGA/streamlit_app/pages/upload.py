import os
import streamlit as st

# 더미 모드 활성화를 위해 환경변수 설정
os.environ['USE_DUMMY_AGENT'] = 'true'

from agents.langgraph_dynamic import graph

st.title("AAWGA Workflow Upload")

uploaded = st.file_uploader("문서 업로드", type=["txt", "pdf", "docx", "xlsx"])
instr = st.selectbox(
    "할 작업을 선택하세요",
    [
        "문서에서 요구사항만 생성해 줘",
        "테스트케이스만 생성해 줘",
        "추적성 매트릭스만 생성해 줘",
        "요구사항과 테스트케이스 둘 다 생성해 줘",
        "요구사항, 테스트케이스, 추적성 매트릭스 모두 생성해 줘"
    ]
)

if uploaded and st.button("실행"):
    # 파일 내용 읽기 (텍스트 기반으로 처리)
    try:
        content = uploaded.read().decode("utf-8")
    except Exception:
        content = str(uploaded)

    # LangGraph 동적 워크플로우 실행
    output = graph.invoke({
        "instruction": instr,
        "content": content
    })

    # 결과 출력
    if output.get("requirements") is not None:
        st.subheader("요구사항")
        st.write(output["requirements"])
    if output.get("testcases") is not None:
        st.subheader("테스트케이스")
        st.write(output["testcases"])
    if output.get("traceability") is not None:
        st.subheader("추적성 매트릭스")
        st.write(output["traceability"])
