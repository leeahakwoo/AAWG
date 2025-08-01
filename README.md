# AAWGA (AbnI AI Workproduct Generation Agent)

AAWGA는 사용자가 업로드한 다양한 형식의 문서를 자동으로 파싱·처리하고, RAG(Retrieval-Augmented Generation) 기법을 통해 핵심 정보를 확보하여 요구사항, 테스트케이스, 추적성 매트릭스를 자동으로 생성하는 AI 에이전트입니다. 이 프로젝트는 소프트웨어 개발 전 과정을 지원하여 생산성과 품질을 극대화하는 것을 목표로 합니다.

**GitHub Repository:** [https://github.com/leeahakwoo/AAWG](https://github.com/leeahakwoo/AAWG) 
---

## 핵심 기능

* **파일 업로드 및 파싱**: txt, docx, pdf, xlsx, xls 포맷 지원  fileciteturn0file3
* **문서 청킹 및 임베딩**: 텍스트를 청크로 분할하고 벡터화
* **벡터 스토어 저장 및 검색**: FAISS 또는 외부 DB(Pinecone/Weaviate) 연동
* **Requirements Agent**: RAG 기반 컨텍스트에서 요구사항 자동 생성
* **Testcase Agent**: 정의된 요구사항을 바탕으로 테스트케이스 자동 생성
* **Traceability Agent**: 요구사항-테스트케이스 매핑 자동 생성
* **템플릿 관리**: MongoDB Atlas를 이용한 사용자 템플릿 CRUD 및 적용  fileciteturn0file3

---

## 아키텍처

프로젝트는 4계층 아키텍처로 구성됩니다:

1. **플랫폼 레벨**: Streamlit Cloud (프론트엔드), FastAPI 백엔드, LangChain Agent Manager, MongoDB Atlas, FAISS/외부 벡터 DB  

2. **모듈 레벨**:

   * `streamlit_app/`: UI 및 사용자 인터랙션 (업로드, 피드백 폼)  
   * `backend/`: FastAPI 앱 및 RAG 서비스 (`app.py`, `routers/`, `services/rag_search.py`)
   * `agents/`: 요구사항·테스트케이스·추적성 생성 에이전트
   * `models/`: Pydantic 스키마 및 MongoDB 스키마
   * `scripts/`: Docker 및 배포 스크립트
3. **플로우 레벨**: 문서 파싱 → 청킹 → 임베딩 → 벡터 검색 → 에이전트 초기화 → 실행  
4. **하위 컴포넌트**: 파일 리더, 텍스트 스플리터, Embeddings, VectorStore, PromptTemplates, Tool Wrappers, Agent Runner  

---

## 설치 및 실행

1. 리포지토리 클론:

   ```bash
   git clone https://github.com/leeahakwoo/AAWG.git
   cd AAWG
   ```
2. 가상환경 생성 및 활성화:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. 의존성 설치:

   ```bash
   pip install -r requirements.txt
   ```
4. 환경변수 설정:

   ```bash
   cp .env.example .env
   # .env 파일에 MongoDB URI, OpenAI API 키, Auth0 설정 등 추가
   ```
5. 애플리케이션 실행:

   ```bash
   streamlit run streamlit_app/main.py
   ```

   또는

   ```bash
   uvicorn backend.app:app --reload
   ```

---

## 사용 예시

1. Streamlit 앱에서 파일 업로드 페이지로 이동합니다.
2. 사업계획서(PDF/DOCX/XLSX) 업로드 시 자동으로 요구사항, 테스트케이스, 추적성 매트릭스가 생성됩니다.
3. 이미 정의된 요구사항 파일 업로드 시 테스트케이스 및 추적표만 생성할 수 있습니다.
4. 저장된 템플릿 선택 후 결과물을 원하는 형식으로 커스터마이징할 수 있습니다.

---

## 로드맵

* 프로덕션용 벡터 DB 연동 및 스케일링
* Auth0/Firebase 인증·권한 관리 추가
* 템플릿 CRUD UI/UX 개선 및 피드백 루프 구축
* CI/CD 파이프라인 및 컨테이너화 완성
* 성능 최적화 및 모니터링 통합  

---

## 기여 가이드

1. 이슈를 생성하거나 기존 이슈에 댓글을 남겨주세요.
2. 포크하여 새로운 브랜치를 생성합니다 (`feature/your-feature`).
3. 변경사항을 커밋하고 푸시합니다.
4. 풀 리퀘스트를 생성하고 리뷰를 요청해주세요.

---

## 라이선스

이 프로젝트는 MIT License하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
# AAWG