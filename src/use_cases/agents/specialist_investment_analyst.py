import os

from src.config.logger import set_logger
from src.use_cases.agents.base_agent import BaseAgent
from src.use_cases.agents.specialist_jbi import SpecialistAgentJBI
from src.use_cases.agents.specialist_gd import SpecialistAgentGD


logger = set_logger("SPECIALIST AGENT INVESTMENT ANALYST")


class SpecialistAgentInvestmentAnalyst(BaseAgent):
    def __init__(self):
        super().__init__()

        self.__agent = self.build_agent(
            prompt_id=os.getenv("PROMPT_ID_INVESTMENT_ANALYST_AGENT"),
            agent_name="specialist_agent_investment_analyst",
            agents=[
                SpecialistAgentJBI().get_agent(),
                SpecialistAgentGD().get_agent()
            ]
        )
    
    def get_agent(self):
        return self.__agent