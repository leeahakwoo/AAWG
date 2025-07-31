# AAWGA (AI-based Automated Workflow for Generating Artifacts)

AI 기반 요구사항 분석 및 테스트케이스 생성 도구입니다.

## 🚀 주요 기능

### ✅ 완료된 기능
- **문서 업로드 및 파싱**: 다양한 형식의 문서 업로드 지원
- **RAG 검색 모듈**: FAISS 기반 벡터 검색
- **3개 Agent 구현**: 요구사항, 테스트케이스, 추적성 매트릭스 생성
- **템플릿 CRUD 기능**: MongoDB 기반 템플릿 관리 시스템
- **피드백 시스템**: 생성 결과에 대한 피드백 수집 및 관리
- **Streamlit UI**: 직관적인 웹 인터페이스

### 🔄 진행 중인 기능
- 템플릿 적용 결함 수정
- OpenAI Embeddings 연동
- 인증 시스템 구현

## 📋 시스템 요구사항

- Python 3.8+
- MongoDB (로컬 또는 Atlas)
- FastAPI
- Streamlit

## 🛠️ 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. MongoDB 설정
로컬 MongoDB 또는 MongoDB Atlas를 사용할 수 있습니다.

환경변수 설정:
```bash
export MONGODB_URL="mongodb://localhost:27017"  # 로컬
# 또는
export MONGODB_URL="mongodb+srv://username:password@cluster.mongodb.net"  # Atlas
export DATABASE_NAME="aawga"
```

### 3. 기본 템플릿 초기화
```bash
python scripts/init_templates.py
```

### 4. 서버 실행

#### Backend (FastAPI)
```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (Streamlit)
```bash
cd streamlit_app
streamlit run main.py
```

## 🎯 사용법

### 1. 문서 업로드 및 생성
1. Streamlit 앱에서 "문서 업로드" 페이지로 이동
2. 생성할 작업 유형 선택
3. 문서 파일 업로드
4. "실행" 버튼 클릭하여 결과 확인

### 2. 템플릿 관리
1. "템플릿 관리" 페이지로 이동
2. 템플릿 목록 조회, 생성, 수정, 삭제 가능
3. 카테고리별 필터링 지원
4. 기본 템플릿 설정 가능

### 3. 피드백 관리
1. "피드백 관리" 페이지로 이동
2. 생성 결과에 대한 피드백 제출
3. 피드백 목록 조회 및 분석

## 📁 프로젝트 구조

```
AAWGA/
├── agents/                 # LangChain Agent 구현
├── backend/               # FastAPI 백엔드
│   ├── routers/          # API 라우터
│   └── services/         # 비즈니스 로직
├── streamlit_app/        # Streamlit 프론트엔드
│   ├── pages/           # 페이지 컴포넌트
│   └── components/      # 재사용 컴포넌트
├── models/              # 데이터 모델
├── scripts/             # 유틸리티 스크립트
└── tests/              # 테스트 코드
```

## 🔧 API 엔드포인트

### 템플릿 관리
- `GET /templates/` - 템플릿 목록 조회
- `POST /templates/` - 템플릿 생성
- `GET /templates/{id}` - 템플릿 조회
- `PUT /templates/{id}` - 템플릿 수정
- `DELETE /templates/{id}` - 템플릿 삭제
- `GET /templates/default/{category}` - 기본 템플릿 조회

### 피드백 관리
- `GET /feedback/` - 피드백 목록 조회
- `POST /feedback/` - 피드백 생성

### 워크플로우 실행
- `POST /run` - 문서 기반 생성 워크플로우 실행

## 🧪 테스트

```bash
pytest tests/
```

## 📊 개발 우선순위

### 1단계 (완료) ✅
- [x] MongoDB 연동 및 템플릿 CRUD 기능
- [x] 피드백 UI 및 저장 기능
- [x] 기본 템플릿 초기화

### 2단계 (진행 중) 🔄
- [ ] 인증/보안 시스템 연동
- [ ] 컨테이너 배포 자동화
- [ ] OpenAI Embeddings 전환

### 3단계 (예정) 📋
- [ ] 전체 테스트 통합 및 마무리
- [ ] 성능 최적화
- [ ] 로깅 및 모니터링

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.
