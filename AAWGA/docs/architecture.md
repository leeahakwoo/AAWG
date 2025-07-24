# Architecture Overview

## 1. System Context
- 개요: AAWG의 목적과 역할
- 주요 사용자 및 외부 시스템

## 2. Component Diagram
- Streamlit Frontend
- FastAPI Backend
- Agents (Requirement, Testcase, Traceability)
- Vector DB / RAG 서비스
- Persistence 레이어 (DB 등)

## 3. Data Flow
1. 사용자가 스펙 문서를 업로드
2. Frontend → Backend로 전송
3. Backend: 텍스트 추출, 임베딩, 저장
4. Agent: LLM 호출, 결과 생성
5. 결과 전송 → Frontend에 표시

## 4. Deployment Architecture
- Docker 기반 배포
- CI/CD 파이프라인 요약 (.github/workflows/ci.yml)

## 5. Diagram
(여기에 PlantUML 또는 Mermaid 다이어그램 삽입)오너
