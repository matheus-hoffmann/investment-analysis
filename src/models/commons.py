from typing import Annotated, Literal
from pydantic import Field

UserId = Annotated[
    str, 
    Field(description="ID do usuário")
    ]

PromptId = Annotated[
    str, 
    Field(description="Identificador único do prompt", min_length=1)
    ]

PromptVersion = Annotated[
    str, 
    Field(description="Versão do prompt (ex: v1.0.0)", pattern=r"^\d+\.\d+\.\d+$")
    ]

PromptType = Annotated[
    Literal['SYSTEM_PROMPT', 'TOOL_DESCRIPTION', 'OTHERS'], 
    Field(description="Tipo/papel do prompt na aplicação")
    ]

PromptContent = Annotated[
    str, 
    Field(description="O conteúdo textual do prompt", min_length=1)
    ]
