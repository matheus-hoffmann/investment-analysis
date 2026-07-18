import os

from src.config.logger import set_logger
from src.use_cases.agents.base_agent import BaseAgent


logger = set_logger("SPECIALIST AGENT JBI")


class SpecialistAgentJBI(BaseAgent):
    def __init__(self):
        super().__init__()

        self.__agent = self.build_agent(
            prompt_id=os.getenv("PROMPT_ID_JBI_AGENT"),
            agent_name="specialist_agent_jbi"
        )
    
    def get_agent(self):
        return self.__agent