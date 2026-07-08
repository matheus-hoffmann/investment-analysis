from pydantic import BaseModel

from src.models.commons import (
    UserId,
    PromptId,
    PromptVersion,
    PromptType,
    PromptContent
)


class PromptVersioningTableModel(BaseModel):
    user_id: UserId
    prompt_id: PromptId
    prompt_type: PromptType
    prompt: PromptContent
    version: PromptVersion
