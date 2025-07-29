# agents/tools.py

from langchain.tools import Tool
from agents.requirement_agent import generate_requirements
from agents.testcase_agent    import generate_testcases
from agents.traceability_agent import generate_traceability

requirement_tool = Tool(
    name="generate_requirements",
    func=generate_requirements,
    description="문서 텍스트를 받아 요구사항 리스트를 반환"
)

testcase_tool = Tool(
    name="generate_testcases",
    func=lambda args: generate_testcases(args["requirements"]),
    description="요구사항 리스트를 받아 테스트케이스 리스트를 반환"
)

traceability_tool = Tool(
    name="generate_traceability",
    func=lambda args: generate_traceability(
        args["requirements"], args["testcases"]
    ),
    description="요구사항과 테스트케이스를 받아 추적성 매트릭스를 반환"
)
