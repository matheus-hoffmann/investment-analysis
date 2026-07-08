from fastapi import APIRouter

from src.config.logger import set_logger

from src.protocol.input import (
    PromptManagementSignUpPromptInput,
    PromptManagementUpdatePromptInput,
    PromptManagementRollbackPromptInput
)
from src.protocol.output import (
    PromptManagementSignUpPromptOutput,
    PromptManagementUpdatePromptOutput,
    PromptManagementRollbackPromptOutput,
    PromptManagementGetPromptOutput
)


router = APIRouter()
logger = set_logger("PROMPT MANAGEMENT ROUTER")


@router.post("/sign-up", response_model=PromptManagementSignUpPromptOutput)
def sign_up_prompt(data: PromptManagementSignUpPromptInput):
    try:
        _data = data.model_dump_json()
        output = {'status': "..."}
    except Exception as e:
        logger.error(f"Error: {e}")
        output = {'status': ""}
    return PromptManagementSignUpPromptOutput(**output)

@router.post("/update", response_model=PromptManagementUpdatePromptOutput)
def update_prompt(data: PromptManagementUpdatePromptInput):
    try:
        _data = data.model_dump_json()
        output = {'status': "..."}
    except Exception as e:
        logger.error(f"Error: {e}")
        output = {'status': ""}
    return PromptManagementUpdatePromptOutput(**output)

@router.post("/rollback", response_model=PromptManagementRollbackPromptOutput)
def rollback_prompt(data: PromptManagementRollbackPromptInput):
    try:
        _data = data.model_dump_json()
        output = {'status': "..."}
    except Exception as e:
        logger.error(f"Error: {e}")
        output = {'status': ""}
    return PromptManagementRollbackPromptOutput(**output)

@router.get("/get/{prompt_id}", response_model=PromptManagementGetPromptOutput)
def get_prompt(prompt_id: str):
    ...
