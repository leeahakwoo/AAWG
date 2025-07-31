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

#### 🔜 예정
- OpenAI Embeddings 실제 연동 (우선순위 낮음)
- Pinecone/Weaviate 연동
- 성능 최적화, 로깅 및 예외 처리 통합
- 컨테이너화 및 자동 배포 구성

### 2. 제품 기능 관점
#### ✅ 완료
- 완전 자동 생성/부분 생성 시나리오 설계
- 템플릿 저장 기능 기본 설계
- **템플릿 CRUD API 엔드포인트 구현** (POST, GET, PUT, DELETE)
- **피드백 시스템 API 엔드포인트 구현** (POST, GET)
- **Streamlit UI 페이지 구현** (템플릿 관리, 피드백 관리)
- **데이터베이스 서비스 레이어 구현** (MongoDB 연동)

#### 🔜 예정
- **MongoDB 실제 설치 및 연동** (현재 연결 실패 상태)
- 사용자 커스터마이징 (포맷 선택, 출력 형태 설정)
- 피드백 기반 생성 결과 수정 기능 구현

### 3. 시스템 아키텍처 및 배포 관점
#### ✅ 완료
- Streamlit UI + FastAPI backend 기본 아키텍처 구성
- LangChain Agent 구조 설계 및 작동 확인
- **FastAPI 서버 정상 실행** (http://localhost:8000)
- **API 엔드포인트 구조 완성** (templates, feedback, run)

#### 🔜 예정
- **MongoDB Atlas 연동** (1차: 템플릿, 2차: 피드백, 3차: 사용자별 문서 관리)
- 인증 시스템 연동 (Auth0/Firebase)
- 배포 자동화 (Docker + GitHub Actions)

### 4. 운영 및 품질 관점
#### ✅ 완료
- 일부 유닛 테스트 수행
- 요구사항 > TC 생성 연결 흐름 점검
- **Pydantic v2 호환성 문제 해결**
- **LangChain 임포트 경고 해결**

#### 🔜 예정
- 전체 단위/통합 테스트 커버리지 확보
- 템플릿 적용 결함 수정 (예: 요구사항 사라짐 문제)
- 문서 수정 결과 추적 및 동기화 기능 구현

---

## 🚨 현재 해결된 오류들

### 1. Pydantic v2 호환성 문제
**문제**: `PyObjectId` 클래스에서 `__modify_schema__` 메서드가 Pydantic v2에서 지원되지 않음
**해결**: `__get_pydantic_json_schema__` 메서드로 변경
**파일**: `models/db_models.py`

### 2. LangChain 임포트 경고
**문제**: `from langchain.embeddings.openai import OpenAIEmbeddings` deprecated 경고
**해결**: `from langchain_community.embeddings import OpenAIEmbeddings`로 변경
**파일**: `backend/services/rag_search.py`

### 3. FastAPI 서버 시작 오류
**문제**: `ModuleNotFoundError: No module named 'agents'`
**해결**: `backend/app.py`에 sys.path 추가하여 import 경로 해결

### 4. MongoDB 연결 실패 처리
**문제**: MongoDB가 설치되지 않아 연결 실패 시 서버 오류 발생
**해결**: `DatabaseService`에 연결 실패 시 더미 데이터 반환 로직 구현
**파일**: `backend/services/database.py`

---

## ⚠️ 현재 남은 문제

### 1. MongoDB 설치 필요
**상태**: MongoDB가 설치되지 않아 실제 데이터 저장 불가
**영향**: 템플릿 CRUD 기능이 더미 데이터만 반환
**해결 방안**: 
- MongoDB Community Edition 설치
- 또는 Docker를 통한 MongoDB 실행
- 또는 MongoDB Atlas 클라우드 서비스 사용

### 2. 테스트 실행 시 서버 연결 오류
**상태**: `pytest` 실행 시 FastAPI 서버가 실행되지 않아 연결 실패
**해결 방안**: 테스트 실행 전 서버 자동 시작 스크립트 구현

---

## 💡 이슈: OpenAI 연동 시기
- 현재 더미 모드로 전체 기능 흐름 검증 가능
- OpenAI Embeddings는 **MVP 직전 도입** 우선순위로 미뤄도 무방
- 단, 실제 품질 검증/성능 테스트/환각 대응 위해 추후 반드시 필요

## 💡 이슈: MongoDB 구축 시점
- 템플릿 CRUD 및 피드백 저장 구현 위해 **중상위 우선순위**
- UI 기반 기능 완성 후 바로 시작 권장
- 3단계 활용: 템플릿 저장 → 피드백 → 사용자 분리

---

## ⏳ 권장 우선순위 요약
1. **MongoDB 설치 및 연동** (현재 최우선)
2. 템플릿 CRUD + MongoDB 연동 완성
3. 피드백 UI + 저장 기능 완성
4. 인증/보안 연동
5. 컨테이너 배포 자동화
6. OpenAI Embeddings 전환
7. 전체 테스트 통합 및 마무리

---

## 🔧 기술적 개선사항

### 완료된 개선사항
- Pydantic v2 호환성 확보
- LangChain 최신 버전 적용
- MongoDB 연결 실패 시 graceful degradation 구현
- FastAPI 서버 안정화

### 다음 개선사항
- MongoDB 설치 및 연동
- 테스트 자동화 스크립트 구현
- 로깅 시스템 구축
- 에러 핸들링 강화

