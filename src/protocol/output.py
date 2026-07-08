from typing import Annotated
from pydantic import BaseModel, Field


class PromptManagementStandardOutput(BaseModel):
    status: bool
    message: str

class PromptManagementSignUpPromptOutput(PromptManagementStandardOutput):
    ...

class PromptManagementUpdatePromptOutput(PromptManagementStandardOutput):
    ...

class PromptManagementRollbackPromptOutput(PromptManagementStandardOutput):
    ...

class PromptManagementGetPromptOutput(BaseModel):
    prompt: str