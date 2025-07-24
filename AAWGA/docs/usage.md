# docs/usage.md

```markdown
# Usage Guide

## 1. Prerequisites

- Python 3.9+ 설치
- 가상 환경 사용 권장 (venv 또는 conda)
- 프로젝트 루트에서 가상 환경 생성 및 활성화:
  ```bash
  python -m venv .venv
  source .venv/bin/activate   # macOS/Linux
  .venv\Scripts\activate  # Windows
  ```
- 필수 패키지 설치:
  ```bash
  pip install -r requirements.txt
  ```

## 2. Installation
```bash
git clone https://github.com/{owner}/AAWGA.git
cd AAWGA
# 가상환경 활성화 후
pip install -r requirements.txt
```

## 3. Running the Application

### 3.1 개발용: 로컬 컴퓨터에서 실행
```bash
# Backend (FastAPI 개발 서버)
python -m uvicorn backend.app:app --reload

# Frontend (Streamlit 앱)
streamlit run streamlit_app/main.py
```
- FastAPI 문서: http://localhost:8000/docs
- Streamlit 앱: http://localhost:8501

### 3.2 프로덕션용 배포

#### Docker 컨테이너
```bash
docker build -t aawga .
docker run -d -p 8000:8000 -p 8501:8501 aawga
```
- FastAPI 문서: http://<서버 IP>:8000/docs
- Streamlit 앱: http://<서버 IP>:8501

#### Streamlit Cloud 배포
1. **리포지토리 푸시**: `main` (또는 설정한 브랜치)에 커밋 및 푸시
2. **앱 설정**:
   - https://share.streamlit.io 접속 후 GitHub 계정 연동
   - **Repository**: `leeahakwoo/AAWG`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app/main.py`
3. **환경 변수 설정**:
   - Settings → Secrets 에서 `PINECONE_API_KEY`, `OPENAI_API_KEY` 등 등록
4. **배포 확인**:
   - 빌드 완료 후 제공된 URL에서 앱 확인

필요 시 `.streamlit/config.toml`:
```toml
[server]
headless = true
enableCORS = false
port = $PORT

[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
```

## 4. Usage Examples
1. 브라우저로 `http://localhost:8501` 접속
2. 스펙 문서를 업로드
3. 요구사항, 테스트케이스, 매핑 결과 확인

## 5. API Endpoints
| Method | Endpoint        | Description                         |
| ------ | --------------- | ----------------------------------- |
| POST   | `/upload-spec`  | 스펙 문서 업로드 및 텍스트 반환       |
| GET    | `/requirements` | 저장된 요구사항 목록 조회          |
```
