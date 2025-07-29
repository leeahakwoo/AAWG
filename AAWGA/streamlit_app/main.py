# streamlit_app/main.py
import streamlit as st
import requests

API_URL = st.secrets.get("api_url", "http://127.0.0.1:8000")

st.title("AAWGA Dynamic Runner")

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