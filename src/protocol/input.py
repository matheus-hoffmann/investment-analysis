from typing import Annotated, Literal
from pydantic import BaseModel, Field

from src.models.commons import (
    UserId,
    PromptId,
    PromptType,
    PromptContent,
    PromptVersion
)


class PromptManagementSignUpPromptInput(BaseModel):
    user_id: UserId
    prompt_id: PromptId
    prompt_type: PromptType
    prompt: PromptContent

class PromptManagementUpdatePromptInput(BaseModel):
    user_id: UserId
    prompt_id: PromptId
    prompt: PromptContent

class PromptManagementRollbackPromptInput(BaseModel):
    user_id: UserId
    prompt_id: PromptId
    version: PromptVersion
