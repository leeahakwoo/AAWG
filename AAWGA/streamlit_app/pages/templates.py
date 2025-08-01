import streamlit as st
import requests
import json
from typing import Dict, Any

API_URL = st.secrets.get("api_url", "http://127.0.0.1:8000")

def templates_page():
    st.title("템플릿 관리")
    
    # 사이드바에 템플릿 관리 옵션
    template_action = st.sidebar.selectbox(
        "템플릿 관리",
        ["템플릿 목록", "템플릿 생성", "템플릿 수정", "템플릿 삭제"]
    )
    
    if template_action == "템플릿 목록":
        show_template_list()
    elif template_action == "템플릿 생성":
        create_template_form()
    elif template_action == "템플릿 수정":
        update_template_form()
    elif template_action == "템플릿 삭제":
        delete_template_form()

def show_template_list():
    st.subheader("템플릿 목록")
    
    # 카테고리 필터
    category_filter = st.selectbox(
        "카테고리 필터",
        ["전체", "requirements", "testcases", "traceability"]
    )
    
    try:
        url = f"{API_URL}/templates/"
        if category_filter != "전체":
            url += f"?category={category_filter}"
        
        response = requests.get(url)
        if response.status_code == 200:
            templates = response.json()
            
            if not templates:
                st.info("등록된 템플릿이 없습니다.")
                return
            
            for template in templates:
                with st.expander(f"{template['name']} ({template['category']})"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**설명:** {template.get('description', '설명 없음')}")
                        st.write(f"**기본 템플릿:** {'예' if template.get('is_default') else '아니오'}")
                        st.write(f"**생성일:** {template['created_at'][:10]}")
                    
                    with col2:
                        st.write(f"**ID:** {template['id']}")
                        
                    # 템플릿 내용 미리보기
                    if st.button(f"내용 보기", key=f"view_{template['id']}"):
                        st.json(template['content'])
        else:
            st.error(f"템플릿 목록 조회 실패: {response.status_code}")
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")

def create_template_form():
    st.subheader("템플릿 생성")
    
    with st.form("create_template"):
        name = st.text_input("템플릿 이름 *")
        description = st.text_area("설명")
        category = st.selectbox(
            "카테고리 *",
            ["requirements", "testcases", "traceability"]
        )
        is_default = st.checkbox("기본 템플릿으로 설정")
        
        st.write("템플릿 내용 (JSON 형식)")
        content_json = st.text_area(
            "템플릿 내용",
            value='{\n  "prompt": "템플릿 프롬프트",\n  "format": "출력 형식"\n}',
            height=200
        )
        
        submitted = st.form_submit_button("템플릿 생성")
        
        if submitted:
            if not name:
                st.error("템플릿 이름을 입력해주세요.")
                return
            
            try:
                content = json.loads(content_json)
            except json.JSONDecodeError:
                st.error("올바른 JSON 형식으로 입력해주세요.")
                return
            
            payload = {
                "name": name,
                "description": description,
                "category": category,
                "content": content,
                "is_default": is_default
            }
            
            try:
                response = requests.post(f"{API_URL}/templates/", json=payload)
                if response.status_code == 200:
                    st.success("템플릿이 성공적으로 생성되었습니다!")
                    st.json(response.json())
                else:
                    st.error(f"템플릿 생성 실패: {response.status_code}")
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")

def update_template_form():
    st.subheader("템플릿 수정")
    
    # 템플릿 목록 가져오기
    try:
        response = requests.get(f"{API_URL}/templates/")
        if response.status_code == 200:
            templates = response.json()
            template_options = {f"{t['name']} ({t['category']})": t['id'] for t in templates}
            
            if not template_options:
                st.info("수정할 템플릿이 없습니다.")
                return
            
            selected_template_name = st.selectbox("수정할 템플릿 선택", list(template_options.keys()))
            template_id = template_options[selected_template_name]
            
            # 기존 템플릿 정보 가져오기
            template_response = requests.get(f"{API_URL}/templates/{template_id}")
            if template_response.status_code == 200:
                template = template_response.json()
                
                with st.form("update_template"):
                    new_name = st.text_input("템플릿 이름", value=template['name'])
                    new_description = st.text_area("설명", value=template.get('description', ''))
                    new_category = st.selectbox(
                        "카테고리",
                        ["requirements", "testcases", "traceability"],
                        index=["requirements", "testcases", "traceability"].index(template['category'])
                    )
                    new_is_default = st.checkbox("기본 템플릿으로 설정", value=template.get('is_default', False))
                    
                    st.write("템플릿 내용 (JSON 형식)")
                    new_content_json = st.text_area(
                        "템플릿 내용",
                        value=json.dumps(template['content'], indent=2),
                        height=200
                    )
                    
                    submitted = st.form_submit_button("템플릿 수정")
                    
                    if submitted:
                        try:
                            new_content = json.loads(new_content_json)
                        except json.JSONDecodeError:
                            st.error("올바른 JSON 형식으로 입력해주세요.")
                            return
                        
                        payload = {
                            "name": new_name,
                            "description": new_description,
                            "category": new_category,
                            "content": new_content,
                            "is_default": new_is_default
                        }
                        
                        try:
                            response = requests.put(f"{API_URL}/templates/{template_id}", json=payload)
                            if response.status_code == 200:
                                st.success("템플릿이 성공적으로 수정되었습니다!")
                                st.json(response.json())
                            else:
                                st.error(f"템플릿 수정 실패: {response.status_code}")
                        except Exception as e:
                            st.error(f"오류 발생: {str(e)}")
            else:
                st.error("템플릿 정보를 가져올 수 없습니다.")
        else:
            st.error("템플릿 목록을 가져올 수 없습니다.")
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")

def delete_template_form():
    st.subheader("템플릿 삭제")
    
    # 템플릿 목록 가져오기
    try:
        response = requests.get(f"{API_URL}/templates/")
        if response.status_code == 200:
            templates = response.json()
            template_options = {f"{t['name']} ({t['category']})": t['id'] for t in templates}
            
            if not template_options:
                st.info("삭제할 템플릿이 없습니다.")
                return
            
            selected_template_name = st.selectbox("삭제할 템플릿 선택", list(template_options.keys()))
            template_id = template_options[selected_template_name]
            
            if st.button("템플릿 삭제", type="primary"):
                try:
                    response = requests.delete(f"{API_URL}/templates/{template_id}")
                    if response.status_code == 200:
                        st.success("템플릿이 성공적으로 삭제되었습니다!")
                    else:
                        st.error(f"템플릿 삭제 실패: {response.status_code}")
                except Exception as e:
                    st.error(f"오류 발생: {str(e)}")
        else:
            st.error("템플릿 목록을 가져올 수 없습니다.")
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    templates_page() 