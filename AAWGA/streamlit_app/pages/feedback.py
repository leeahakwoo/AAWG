import streamlit as st
import requests
import json
from datetime import datetime

API_URL = st.secrets.get("api_url", "http://127.0.0.1:8000")

def feedback_page():
    st.title("피드백 관리")
    
    # 사이드바에 피드백 관리 옵션
    feedback_action = st.sidebar.selectbox(
        "피드백 관리",
        ["피드백 목록", "피드백 생성"]
    )
    
    if feedback_action == "피드백 목록":
        show_feedback_list()
    elif feedback_action == "피드백 생성":
        create_feedback_form()

def show_feedback_list():
    st.subheader("피드백 목록")
    
    # 제한 개수 설정
    limit = st.slider("표시할 피드백 개수", min_value=10, max_value=100, value=50)
    
    try:
        response = requests.get(f"{API_URL}/feedback/?limit={limit}")
        if response.status_code == 200:
            feedback_list = response.json()
            
            if not feedback_list:
                st.info("등록된 피드백이 없습니다.")
                return
            
            for feedback in feedback_list:
                with st.expander(f"피드백 - {feedback['created_at'][:19]}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**지시사항:** {feedback['instruction']}")
                        st.write(f"**사용자 피드백:** {feedback['user_feedback']}")
                        if feedback.get('rating'):
                            st.write(f"**평점:** {'⭐' * feedback['rating']}")
                    
                    with col2:
                        if feedback.get('template_id'):
                            st.write(f"**템플릿 ID:** {feedback['template_id']}")
                        st.write(f"**생성일:** {feedback['created_at'][:10]}")
                    
                    # 원본 내용과 생성 결과 미리보기
                    with st.expander("원본 내용"):
                        st.text(feedback['original_content'][:500] + "..." if len(feedback['original_content']) > 500 else feedback['original_content'])
                    
                    with st.expander("생성 결과"):
                        st.json(feedback['generated_result'])
        else:
            st.error(f"피드백 목록 조회 실패: {response.status_code}")
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")

def create_feedback_form():
    st.subheader("피드백 생성")
    
    with st.form("create_feedback"):
        # 템플릿 선택 (선택사항)
        try:
            template_response = requests.get(f"{API_URL}/templates/")
            if template_response.status_code == 200:
                templates = template_response.json()
                template_options = {f"{t['name']} ({t['category']})": t['id'] for t in templates}
                template_options["템플릿 없음"] = None
                
                selected_template_name = st.selectbox("사용된 템플릿 (선택사항)", list(template_options.keys()))
                template_id = template_options[selected_template_name]
            else:
                template_id = None
        except:
            template_id = None
        
        instruction = st.text_area("사용자 지시사항 *")
        original_content = st.text_area("원본 문서 내용 *", height=150)
        
        st.write("생성된 결과 (JSON 형식)")
        generated_result_json = st.text_area(
            "생성된 결과",
            value='{\n  "requirements": [],\n  "testcases": [],\n  "traceability": []\n}',
            height=150
        )
        
        user_feedback = st.text_area("사용자 피드백 *", placeholder="생성 결과에 대한 피드백을 입력하세요...")
        rating = st.slider("평점 (1-5)", min_value=1, max_value=5, value=3)
        
        submitted = st.form_submit_button("피드백 제출")
        
        if submitted:
            if not instruction or not original_content or not user_feedback:
                st.error("필수 항목을 모두 입력해주세요.")
                return
            
            try:
                generated_result = json.loads(generated_result_json)
            except json.JSONDecodeError:
                st.error("올바른 JSON 형식으로 입력해주세요.")
                return
            
            payload = {
                "template_id": template_id,
                "instruction": instruction,
                "original_content": original_content,
                "generated_result": generated_result,
                "user_feedback": user_feedback,
                "rating": rating
            }
            
            try:
                response = requests.post(f"{API_URL}/feedback/", json=payload)
                if response.status_code == 200:
                    st.success("피드백이 성공적으로 제출되었습니다!")
                    st.json(response.json())
                else:
                    st.error(f"피드백 제출 실패: {response.status_code}")
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    feedback_page()
