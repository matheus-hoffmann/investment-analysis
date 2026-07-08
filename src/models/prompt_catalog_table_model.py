from typing import Annotated
from pydantic import BaseModel, Field

from src.models.commons import (
    PromptId,
    PromptVersion,
    PromptType,
    PromptContent
)

    
class PromptCatalogTableModel(BaseModel):
    prompt_id: PromptId
    prompt_type: PromptType
    prompt: PromptContent
    version: PromptVersion
    updated_by: Annotated[str, Field(description="ID do usuário ou sistema que atualizou para a versão estável")]