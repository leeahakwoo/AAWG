# API Specifications

## Overview
AAWGA API는 AI 에이전트 기반의 동적 워크플로우 실행을 위한 REST API입니다.

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## Authentication
현재 버전에서는 인증이 필요하지 않습니다.

## Endpoints

### 1. POST /run

#### Description
사용자의 지시사항과 문서 내용을 받아 AI 에이전트를 실행하고 결과를 반환합니다.

#### Request Body
```json
{
  "instruction": "string",
  "content": "string"
}
```

#### Request Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instruction | string | Yes | 실행할 작업 지시사항 |
| content | string | Yes | 분석할 문서 내용 |

#### Instruction Examples
- `"문서에서 요구사항만 생성해 줘"`
- `"테스트케이스만 생성해 줘"`
- `"추적성 매트릭스만 생성해 줘"`
- `"요구사항과 테스트케이스 둘 다 생성해 줘"`
- `"요구사항, 테스트케이스, 추적성 매트릭스 모두 생성해 줘"`

#### Response
```json
{
  "requirements": ["string"],
  "testcases": ["string"],
  "traceability": ["object"]
}
```

#### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| requirements | array[string] | 생성된 요구사항 목록 |
| testcases | array[string] | 생성된 테스트케이스 목록 |
| traceability | array[object] | 생성된 추적성 매트릭스 |

#### Example Request
```bash
curl -X POST "http://localhost:8000/run" \
  -H "Content-Type: application/json" \
  -d '{
    "instruction": "요구사항과 테스트케이스 둘 다 생성해 줘",
    "content": "사용자 로그인 기능이 필요합니다. 이메일과 비밀번호로 로그인할 수 있어야 합니다."
  }'
```

#### Example Response
```json
{
  "requirements": [
    "1. 사용자 로그인 기능 구현",
    "2. 이메일/비밀번호 인증 시스템",
    "3. 로그인 상태 관리"
  ],
  "testcases": [
    "1. 유효한 이메일/비밀번호로 로그인 성공",
    "2. 잘못된 비밀번호로 로그인 실패",
    "3. 존재하지 않는 이메일로 로그인 시도"
  ],
  "traceability": []
}
```

#### Error Responses

##### 500 Internal Server Error
```json
{
  "detail": "Error message"
}
```

## Error Codes
| Code | Description |
|------|-------------|
| 500 | Internal server error (에이전트 실행 실패, API 키 오류 등) |

## Rate Limits
현재 버전에서는 rate limit이 설정되지 않았습니다.

## Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| OPENAI_API_KEY | Yes | OpenAI API 키 |
| USE_DUMMY_AGENT | No | 더미 모드 활성화 (true/false) |

## Testing

### Using curl
```bash
# 요구사항만 생성
curl -X POST "http://localhost:8000/run" \
  -H "Content-Type: application/json" \
  -d '{"instruction": "문서에서 요구사항만 생성해 줘", "content": "테스트 문서 내용"}'

# 모든 기능 생성
curl -X POST "http://localhost:8000/run" \
  -H "Content-Type: application/json" \
  -d '{"instruction": "요구사항, 테스트케이스, 추적성 매트릭스 모두 생성해 줘", "content": "테스트 문서 내용"}'
```

### Using Python requests
```python
import requests

url = "http://localhost:8000/run"
payload = {
    "instruction": "요구사항과 테스트케이스 둘 다 생성해 줘",
    "content": "사용자 로그인 기능이 필요합니다."
}

response = requests.post(url, json=payload)
data = response.json()

print("Requirements:", data.get("requirements", []))
print("Testcases:", data.get("testcases", []))
print("Traceability:", data.get("traceability", []))
```

## OpenAPI Documentation
API 문서는 다음 URL에서 확인할 수 있습니다:
- **Development**: `http://localhost:8000/docs`
- **Production**: `https://your-domain.com/docs` 