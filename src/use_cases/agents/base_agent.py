from langchain.agents import create_agent
from langgraph_supervisor import create_supervisor

from src.config.logger import set_logger

from src.handlers.azure.openai_handler import AzureOpenAIHandler
from src.use_cases.prompt_management_uc import PromptManagementUC


logger = set_logger("BASE AGENT")


class BaseAgent:
    def build_agent(self, prompt_id: str, agent_name: str, tools: list = [], agents: list = []):
        system_prompt = self.get_prompt(prompt_id=prompt_id)
        if not system_prompt:
            logger.error(f"Error getting system prompt {prompt_id}")
            return None
        
        if (isinstance(agents, list) and len(agents) > 0):
            _tools = tools if (isinstance(tools, list) and len(tools) == 0) else None
            return create_supervisor(
                model=self.get_llm_client(),
                agents=agents,
                tools=_tools,
                prompt=system_prompt,
                supervisor_name=agent_name,
                add_handoff_back_messages=True,
                output_mode="full_history"
            ).compile()

        elif isinstance(tools, list):
            _tools = tools if len(tools) == 0 else None
            return create_agent(
                model=self.get_llm_client(),
                tools=tools,
                system_prompt=system_prompt,
                name=agent_name
            )
        else:
            return None
    
    @staticmethod
    def get_llm_client():
        return AzureOpenAIHandler().set_llm()

    @staticmethod
    def get_prompt(prompt_id):
        with PromptManagementUC() as pm_uc:
            status, _, prompt = pm_uc.get_prompt(prompt_id=prompt_id)
        if status:
            return prompt
        return None