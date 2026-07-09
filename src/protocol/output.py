from typing import Annotated, Optional, Any
from pydantic import BaseModel, Field

from src.models.commons import PromptContent


class PromptManagementStandardOutput(BaseModel):
    status: bool
    message: str
    content: Optional[Any] = None

class PromptManagementSignUpPromptOutput(PromptManagementStandardOutput):
    ...

class PromptManagementUpdatePromptOutput(PromptManagementStandardOutput):
    ...

class PromptManagementRollbackPromptOutput(PromptManagementStandardOutput):
    ...

class PromptManagementGetPromptOutput(PromptManagementStandardOutput):
    ...