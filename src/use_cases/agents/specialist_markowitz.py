import os

from src.config.logger import set_logger
from src.use_cases.agents.base_agent import BaseAgent


logger = set_logger("SPECIALIST AGENT MARKOWITZ")


class SpecialistAgentMarkowitz(BaseAgent):
    def __init__(self):
        super().__init__()

        self.__agent = self.build_agent(
            prompt_id=os.getenv("PROMPT_ID_MARKOWITZ_AGENT"),
            agent_name="specialist_agent_markowitz"
        )
    
    def get_agent(self):
        return self.__agent