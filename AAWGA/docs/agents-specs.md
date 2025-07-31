# AI Agents Specifications

## Overview
AAWGA는 3개의 AI 에이전트를 통해 요구사항 분석, 테스트케이스 생성, 추적성 매트릭스 생성을 수행합니다.

## Agent Architecture

### 1. Dynamic Workflow Agent
**파일**: `agents/langgraph_dynamic.py`

#### 역할
- 사용자 지시사항에 따른 조건부 에이전트 실행
- 에이전트 간 데이터 전달 및 조율

#### 동작 방식
```python
def dynamic_invoke(state):
    instr = state["instruction"]
    content = state["content"]
    result = {}
    
    # 조건부 실행
    if "요구사항" in instr:
        result["requirements"] = generate_requirements(content)
    if "테스트케이스" in instr:
        result["testcases"] = generate_testcases(reqs)
    if "추적성" in instr:
        result["traceability"] = generate_traceability(reqs, tcs)
    
    return result
```

#### 입력
- `instruction`: 사용자 지시사항
- `content`: 분석할 문서 내용

#### 출력
- `requirements`: 생성된 요구사항 (조건부)
- `testcases`: 생성된 테스트케이스 (조건부)
- `traceability`: 생성된 추적성 매트릭스 (조건부)

### 2. Requirement Agent
**파일**: `agents/requirement_agent.py`

#### 역할
- 문서 내용에서 요구사항을 추출하고 정리
- RAG (Retrieval-Augmented Generation) 기반 분석

#### 동작 방식
1. **문서 분할**: CharacterTextSplitter로 청크 단위 분할
2. **벡터화**: OpenAI Embeddings로 임베딩 생성
3. **검색**: FAISS를 통한 유사 문서 검색
4. **생성**: LLM을 통한 요구사항 생성

#### 더미 모드
```python
if os.getenv("USE_DUMMY_AGENT", "").lower() == "true":
    return [f"[DUMMY] 요구사항 예시: {input_text}"]
```

#### 입력
- `input_text`: 분석할 문서 내용

#### 출력
- `List[str]`: 번호가 매겨진 요구사항 목록

#### 예시 출력
```
[
    "1. 사용자 로그인 기능 구현",
    "2. 이메일/비밀번호 인증 시스템",
    "3. 로그인 상태 관리"
]
```

### 3. Testcase Agent
**파일**: `agents/testcase_agent.py`

#### 역할
- 요구사항을 기반으로 테스트케이스 생성
- 각 요구사항에 대한 포괄적인 테스트 시나리오 작성

#### 동작 방식
1. **요구사항 분석**: 입력된 요구사항 목록 파싱
2. **테스트케이스 생성**: LLM을 통한 테스트케이스 생성
3. **결과 정리**: 생성된 테스트케이스를 리스트로 정리

#### 더미 모드
```python
if os.getenv("USE_DUMMY_AGENT", "").lower() == "true":
    return [f"[DUMMY] 테스트케이스 예시: {req}" for req in requirements]
```

#### 입력
- `requirements`: 요구사항 목록

#### 출력
- `List[str]`: 생성된 테스트케이스 목록

#### 예시 출력
```
[
    "1. 유효한 이메일/비밀번호로 로그인 성공",
    "2. 잘못된 비밀번호로 로그인 실패",
    "3. 존재하지 않는 이메일로 로그인 시도"
]
```

### 4. Traceability Agent
**파일**: `agents/traceability_agent.py`

#### 역할
- 요구사항과 테스트케이스 간의 매핑 생성
- 추적성 매트릭스 작성

#### 동작 방식
1. **매핑 분석**: 요구사항과 테스트케이스 간의 관계 분석
2. **JSON 생성**: LLM을 통한 JSON 형태 매핑 생성
3. **결과 검증**: JSON 파싱 및 오류 처리

#### 더미 모드
```python
if os.getenv("USE_DUMMY_AGENT", "").lower() == "true":
    return [{"requirement": req, "testcases": []} for req in requirements]
```

#### 입력
- `requirements`: 요구사항 목록
- `testcases`: 테스트케이스 목록

#### 출력
- `List[Dict]`: 추적성 매트릭스 (JSON 형태)

#### 예시 출력
```json
[
    {
        "requirement_id": "REQ-001",
        "requirement": "사용자 로그인 기능 구현",
        "testcase_ids": ["TC-001", "TC-002"],
        "testcases": [
            "유효한 이메일/비밀번호로 로그인 성공",
            "잘못된 비밀번호로 로그인 실패"
        ]
    }
]
```

## Agent Configuration

### 환경 변수
| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | OpenAI API 키 |
| `USE_DUMMY_AGENT` | `false` | 더미 모드 활성화 |

### LLM 설정
- **Model**: OpenAI GPT (기본값)
- **Temperature**: 0 (일관된 결과를 위해)
- **Max Tokens**: 모델 기본값

### RAG 설정 (Requirement Agent)
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 100 characters
- **Similarity Search**: Top 3 results
- **Vector Store**: FAISS

## Error Handling

### 일반적인 오류
1. **API 키 오류**: OpenAI API 키가 유효하지 않을 때
2. **네트워크 오류**: API 호출 실패 시
3. **JSON 파싱 오류**: Traceability Agent에서 JSON 파싱 실패 시

### 오류 처리 방식
```python
try:
    # 에이전트 실행
    result = agent_function(input)
except Exception as e:
    # 오류 로깅 및 기본값 반환
    logger.error(f"Agent error: {e}")
    return default_value
```

## Performance Considerations

### 최적화 전략
1. **더미 모드**: 개발/테스트 시 실제 API 호출 없이 실행
2. **조건부 실행**: 필요한 에이전트만 실행하여 비용 절약
3. **캐싱**: 동일한 입력에 대한 결과 캐싱 (향후 구현 예정)

### 성능 지표
- **응답 시간**: 일반적으로 3-10초
- **토큰 사용량**: 입력 길이에 비례
- **정확도**: RAG 기반으로 향상된 결과 품질

## Testing

### 단위 테스트
```python
# test_agents.py
def test_requirement_agent():
    result = generate_requirements("테스트 문서")
    assert isinstance(result, list)
    assert len(result) > 0

def test_testcase_agent():
    requirements = ["사용자 로그인 기능"]
    result = generate_testcases(requirements)
    assert isinstance(result, list)
    assert len(result) > 0
```

### 통합 테스트
```python
def test_dynamic_workflow():
    state = {
        "instruction": "요구사항과 테스트케이스 둘 다 생성해 줘",
        "content": "사용자 로그인 기능이 필요합니다."
    }
    result = dynamic_invoke(state)
    assert "requirements" in result
    assert "testcases" in result
``` 