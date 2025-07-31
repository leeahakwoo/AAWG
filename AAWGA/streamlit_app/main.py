# streamlit_app/main.py
import streamlit as st
import requests
from pages import templates, feedback

API_URL = st.secrets.get("api_url", "http://127.0.0.1:8000")

# 페이지 설정
st.set_page_config(
    page_title="AAWGA Dynamic Runner",
    page_icon="🤖",
    layout="wide"
)

# 사이드바 네비게이션
st.sidebar.title("AAWGA")
page = st.sidebar.selectbox(
    "페이지 선택",
    ["홈", "문서 업로드", "템플릿 관리", "피드백 관리"]
)

if page == "홈":
    st.title("AAWGA Dynamic Runner")
    st.write("AI 기반 요구사항 분석 및 테스트케이스 생성 도구입니다.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📄 문서 업로드")
        st.write("문서를 업로드하여 요구사항, 테스트케이스, 추적성 매트릭스를 생성합니다.")
    
    with col2:
        st.info("📋 템플릿 관리")
        st.write("생성에 사용할 템플릿을 관리하고 커스터마이징합니다.")
    
    with col3:
        st.info("💬 피드백 관리")
        st.write("생성 결과에 대한 피드백을 관리하고 개선합니다.")

elif page == "문서 업로드":
    st.title("문서 업로드 및 생성")
    
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

    uploaded = st.file_uploader("문서 업로드", type=["txt", "pdf", "docx", "xlsx"])
    if uploaded and st.button("실행"):
        try:
            content = uploaded.read().decode("utf-8")
        except:
            content = str(uploaded)
        
        payload = {"instruction": instr, "content": content}
        response = requests.post(f"{API_URL}/run", json=payload)
        data = response.json()

        if data.get("requirements") is not None:
            st.subheader("요구사항")
            st.write(data["requirements"])
        if data.get("testcases") is not None:
            st.subheader("테스트케이스")
            st.write(data["testcases"])
        if data.get("traceability") is not None:
            st.subheader("추적성 매트릭스")
            st.write(data["traceability"])

elif page == "템플릿 관리":
    templates.templates_page()

elif page == "피드백 관리":
    feedback.feedback_page()