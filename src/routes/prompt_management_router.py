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

from src.use_cases.prompt_management_uc import PromptManagementUC

router = APIRouter()
logger = set_logger("PROMPT MANAGEMENT ROUTER")


prompt_management_uc = PromptManagementUC()


@router.post("/sign-up", response_model=PromptManagementSignUpPromptOutput)
def sign_up_prompt(data: PromptManagementSignUpPromptInput):
    try:
        status, message = prompt_management_uc.sign_up_prompt(
            user_id=data.user_id,
            prompt_id=data.prompt_id,
            prompt_type=data.prompt_type,
            prompt=data.prompt
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        status = False
        message = f"Error creating prompt {data.prompt_id}. Ex.: {e}"
    output = {
        "status": status,
        "message": message
    }
    return PromptManagementSignUpPromptOutput(**output)

@router.post("/update", response_model=PromptManagementUpdatePromptOutput)
def update_prompt(data: PromptManagementUpdatePromptInput):
    try:
        status, message = prompt_management_uc.update_prompt(
            user_id=data.user_id,
            prompt_id=data.prompt_id,
            prompt=data.prompt
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        status = False
        message = f"Error updating prompt {data.prompt_id}. Ex.: {e}"
    output = {
        "status": status,
        "message": message
    }
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
