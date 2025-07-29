# agents/agent_runner.py

from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from agents.tools import requirement_tool, testcase_tool, traceability_tool

TOOLS = [requirement_tool, testcase_tool, traceability_tool]

class AAWGAgent:
    def __init__(self):
        llm = ChatOpenAI(temperature=0)
        # zero-shot-react-description 은 툴 호출 기반 에이전트를 만듭니다
        self.agent = initialize_agent(
            tools=TOOLS,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def run(self, instruction: str, context: dict = None):
        """
        instruction: 자연어로 '요구사항 생성해 줘' | '테스트케이스만 부탁해' 등
        context: 필요한 경우 사전 검색 결과 등을 담음
        """
        # Agent 내부가 어떤 툴을 호출할지 판단
        return self.agent.run(instruction)
