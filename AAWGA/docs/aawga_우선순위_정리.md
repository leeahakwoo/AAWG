# AAWGA 개발 우선순위 및 진행 정리 (2025-07-31 기준)

## 📌 관점별 정리

### 1. 기술 구현 관점
#### ✅ 완료
- 문서 업로드 및 파싱 기능 구현
- RAG 검색 모듈 및 FAISS 연동
- DummyEmbeddings 적용
- 3개 Agent (요구사항, TC, Traceability) 프로토타입 구현
- **FastAPI 서버 정상 실행 확인**
- **Pydantic v2 호환성 문제 해결** (`__modify_schema__` → `__get_pydantic_json_schema__`)
- **LangChain 임포트 경고 해결** (deprecated import 수정)
- **MongoDB 연결 실패 시 더미 데이터 반환 로직 구현**
- **MongoDB Atlas 클라우드 연동 완료**
- **Docker 컨테이너화 완료** (Dockerfile, docker-compose.yml)
- **환경 변수 관리 체계 구축** (.env 파일, 설정 분리)

#### 🔜 예정
- OpenAI Embeddings 실제 연동 및 환각 대응 전략
- Pinecone/Weaviate 연동 검토
- 성능 최적화, 로깅 및 예외 처리 통합
- CI/CD 자동 배포 구성

### 2. 제품 기능 관점
#### ✅ 완료
- 완전 자동 생성/부분 생성 시나리오 설계
- 템플릿 저장 기능 기본 설계
- **템플릿 CRUD API 엔드포인트 구현** (POST, GET, PUT, DELETE)
- **피드백 시스템 API 엔드포인트 구현** (POST, GET)
- **Streamlit UI 페이지 구현** (템플릿 관리, 피드백 관리)
- **MongoDB Atlas 기반 데이터베이스 서비스 레이어 완성**
- **OpenAPI 문서화** (Swagger UI 자동 생성)

#### 🔜 예정
- 사용자 커스터마이징 (포맷 선택, 출력 형태 설정)
- 피드백 기반 생성 결과 수정 기능 구현
- 다국어 지원 기능 검토
- 대시보드 및 통계 기능

### 3. 시스템 아키텍처 및 배포 관점
#### ✅ 완료
- Streamlit UI + FastAPI backend 기본 아키텍처 구성
- LangChain Agent 구조 설계 및 작동 확인
- **FastAPI 서버 정상 실행** (http://localhost:8000)
- **API 엔드포인트 구조 완성** (templates, feedback, run)
- **Docker Compose를 통한 전체 서비스 통합 실행**
- **MongoDB Atlas 프로덕션 환경 연동**

#### 🔜 예정
- 인증 시스템 연동 (Auth0/Firebase)
- 배포 자동화 (GitHub Actions)
- 모니터링 시스템 (Prometheus, Grafana)
- 로드 밸런싱 및 스케일링 구성

### 4. 운영 및 품질 관점
#### ✅ 완료
- 일부 유닛 테스트 수행
- 요구사항 > TC 생성 연결 흐름 점검
- **Pydantic v2 호환성 문제 해결**
- **LangChain 임포트 경고 해결**
- **Docker 환경에서의 서비스 통합 테스트**

#### 🔜 예정
- 전체 단위/통합 테스트 커버리지 90% 이상 확보
- 템플릿 적용 결함 수정 (예: 요구사항 사라짐 문제)
- 문서 수정 결과 추적 및 동기화 기능 구현
- 성능 테스트 및 최적화

---

## 🚨 해결된 주요 오류들

### 1. Pydantic v2 호환성 문제 ✅
**문제**: `PyObjectId` 클래스에서 `__modify_schema__` 메서드가 Pydantic v2에서 지원되지 않음
**해결**: `__get_pydantic_json_schema__` 메서드로 변경
**파일**: `models/db_models.py`

### 2. LangChain 임포트 경고 ✅
**문제**: `from langchain.embeddings.openai import OpenAIEmbeddings` deprecated 경고
**해결**: `from langchain_community.embeddings import OpenAIEmbeddings`로 변경
**파일**: `backend/services/rag_search.py`

### 3. FastAPI 서버 시작 오류 ✅
**문제**: `ModuleNotFoundError: No module named 'agents'`
**해결**: `backend/app.py`에 sys.path 추가하여 import 경로 해결

### 4. MongoDB 연결 문제 ✅
**문제**: MongoDB 로컬 설치 및 연결 이슈
**해결**: MongoDB Atlas 클라우드 서비스로 전환, 연결 실패 시 graceful degradation 구현
**파일**: `backend/services/database.py`

### 5. Docker 컨테이너화 ✅
**문제**: 서비스 간 연결 및 환경 설정 복잡성
**해결**: Docker Compose로 멀티 서비스 통합, 환경 변수 표준화
**파일**: `docker-compose.yml`, `Dockerfile`

---

## ⚠️ 현재 진행 중인 작업

### 1. 성능 최적화 🔄
**상태**: RAG 검색 성능 및 Agent 응답 시간 개선 작업 중
**목표**: 평균 응답 시간 3초 이내 달성
**방법**: 벡터 DB 최적화, 캐싱 전략 도입

### 2. 테스트 커버리지 확대 🔄
**상태**: 현재 약 60% 수준, 90% 목표로 확대 중
**방법**: 
- 단위 테스트 추가 작성
- 통합 테스트 시나리오 확대
- CI/CD 파이프라인에 테스트 자동화 통합

### 3. OpenAI 실제 연동 준비 🔄
**상태**: DummyEmbeddings에서 실제 OpenAI API로 전환 준비
**고려사항**: 
- API 사용량 모니터링
- 환각(Hallucination) 대응 전략
- 비용 최적화 방안

---

## 💡 전략적 이슈 및 결정사항

### 1. OpenAI 연동 시기
- **현재 전략**: MVP 완성 직전 도입으로 변경 없음
- **이유**: 더미 모드로 전체 기능 흐름 검증 가능, 비용 효율성
- **일정**: 베타 테스트 직전 (예상: 2025년 8월 중순)

### 2. 데이터베이스 전략
- **결정**: MongoDB Atlas 클라우드 서비스 채택
- **이유**: 관리 부담 감소, 확장성, 백업 자동화
- **단계별 활용**: 템플릿 저장 → 피드백 → 사용자별 문서 관리

### 3. 배포 전략
- **결정**: Docker 기반 컨테이너화 완료
- **다음 단계**: Kubernetes 또는 Docker Swarm 검토
- **목표**: 무중단 배포, 자동 스케일링

---

## ⏳ 업데이트된 우선순위

### 🔥 최우선 (1-2주 내)
1. **성능 최적화 및 로딩 시간 단축**
2. **테스트 커버리지 90% 달성**
3. **OpenAI Embeddings 실제 연동**

### 🎯 고우선순위 (2-4주 내)
4. **인증/보안 시스템 도입**
5. **CI/CD 자동 배포 파이프라인 완성**
6. **모니터링 및 로깅 시스템 구축**

### 📋 중우선순위 (1-2개월 내)
7. **사용자 커스터마이징 기능 확대**
8. **다국어 지원 기능**
9. **대시보드 및 분석 기능**

### 🔮 장기 계획 (2개월 이후)
10. **Pinecone/Weaviate 연동 검토**
11. **모바일 앱 개발**
12. **엔터프라이즈 기능 확장**

---

## 🔧 기술 스택 현황

### ✅ 확정된 기술 스택
- **Backend**: FastAPI, Python 3.9+
- **Frontend**: Streamlit
- **Database**: MongoDB Atlas
- **Vector DB**: FAISS (현재), Pinecone (검토 중)
- **ML/AI**: LangChain, OpenAI GPT (예정)
- **Container**: Docker, Docker Compose
- **Documentation**: OpenAPI/Swagger

### 🔄 검토 중인 기술
- **Authentication**: Auth0 vs Firebase Auth
- **Monitoring**: Prometheus + Grafana vs DataDog
- **CI/CD**: GitHub Actions vs GitLab CI
- **Orchestration**: Kubernetes vs Docker Swarm

---

## 📊 프로젝트 진행률

### 전체 진행률: **75%** 📈

#### 세부 진행률
- **백엔드 개발**: 85% ✅
- **프론트엔드 개발**: 70% 🔄
- **데이터베이스 연동**: 90% ✅
- **테스트 작성**: 60% 🔄
- **배포 준비**: 80% ✅
- **문서화**: 75% 🔄

---

## 🎯 다음 마일스톤

### 마일스톤 1: MVP 완성 (2025-08-15 목표)
- [ ] OpenAI 실제 연동
- [ ] 테스트 커버리지 90%
- [ ] 성능 최적화 완료
- [ ] 기본 인증 시스템

### 마일스톤 2: 베타 출시 (2025-09-01 목표)
- [ ] CI/CD 자동화
- [ ] 모니터링 시스템
- [ ] 사용자 피드백 수집

### 마일스톤 3: 정식 출시 (2025-09-30 목표)
- [ ] 확장성 검증
- [ ] 보안 감사
- [ ] 운영 매뉴얼 완성