import os

from src.config.logger import set_logger
from src.use_cases.agents.base_agent import BaseAgent
from src.use_cases.agents.specialist_investment_analyst import SpecialistAgentInvestmentAnalyst
from src.use_cases.agents.specialist_markowitz import SpecialistAgentMarkowitz


logger = set_logger("ORCHESTRATOR AGENT")


class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__()

        self.__agent = self.build_agent(
            prompt_id=os.getenv("PROMPT_ID_ORCHESTRATOR_AGENT"),
            agent_name="orchestrator_agent",
            agents=[
                SpecialistAgentInvestmentAnalyst().get_agent(),
                SpecialistAgentMarkowitz().get_agent()
            ]
        )
    
    def get_agent(self):
        return self.__agent