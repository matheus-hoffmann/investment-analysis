"""
Duas tabelas
Tabela 1: Prompt Versioning
    used_id
    prompt_id
    prompt_type
    prompt
    version
    datetime

Tabela 2: Stable Version
    prompt_id
    prompt_type
    prompt
    version
    datetime
    updated_by
"""
from src.config.logger import set_logger
from src.decorators.singleton import singleton
from src.handlers.azure.storage_account_table_handler import StorageAccountTableHandler

from src.models.commons import (
    UserId,
    PromptId,
    PromptType,
    PromptContent
)
from src.models.prompt_catalog_table_model import PromptCatalogTableModel
from src.models.prompt_versioning_table_model import PromptVersioningTableModel

from src.utils.utils import get_highest_version_index, increment_version


logger = set_logger("PROMPT MANAGEMENT USE CASE")


@singleton
class PromptManagementUC:
    def __init__(self):
        self.__PROMPT_CATALOG_TABLE_NAME = "promptCatalog"
        self.__PROMPT_VERSIONING_TABLE_NAME = "promptVersioning"

        self.__st_handler = StorageAccountTableHandler()
        self.__st_handler.create_table_if_not_exists(table_name=self.__PROMPT_CATALOG_TABLE_NAME)
        self.__st_handler.create_table_if_not_exists(table_name=self.__PROMPT_VERSIONING_TABLE_NAME)

    def __check_if_prompt_already_exists(self, prompt_id: PromptId) -> bool:
        return len(self.__st_handler.generic_filter(table_name=self.__PROMPT_CATALOG_TABLE_NAME, filter={"prompt_id": prompt_id})) > 0

    def __check_if_prompt_is_the_same_in_catalog(self, prompt_id: PromptId, prompt: PromptContent) -> bool:
        return len(self.__st_handler.generic_filter(table_name=self.__PROMPT_CATALOG_TABLE_NAME, filter={"prompt_id": prompt_id, "prompt": prompt})) > 0

    def sign_up_prompt(self, user_id: UserId, prompt_id: PromptId, prompt_type: PromptType, prompt: PromptContent) -> bool:
        try:
            if self.__check_if_prompt_already_exists(prompt_id=prompt_id):
                return False, f"Prompt {prompt_id} already exists, only update it"
            
            catalog_model = PromptCatalogTableModel(
                prompt_id=prompt_id,
                prompt_type=prompt_type,
                prompt=prompt,
                version="0.0.0",
                updated_by=user_id
            )
            versioning_model = PromptVersioningTableModel(
                user_id=user_id,
                prompt_id=prompt_id,
                prompt_type=prompt_type,
                prompt=prompt,
                version="0.0.0"
            )

            self.__st_handler.create_entity(
                table_name=self.__PROMPT_CATALOG_TABLE_NAME,
                data=catalog_model.model_dump()
            )
            self.__st_handler.create_entity(
                table_name=self.__PROMPT_VERSIONING_TABLE_NAME,
                data=versioning_model.model_dump()
            )
            return True, f"Prompt successfully registered prompt {prompt_id}"
        except Exception as e:
            return False, f"Error signing up prompt: {e}"

    def update_prompt(self, user_id: UserId, prompt_id: PromptId, prompt: PromptContent) -> bool:
        try:
            if self.__check_if_prompt_is_the_same_in_catalog(prompt_id=prompt_id, prompt=prompt):
                return False, f"Prompt {prompt_id} is already this"
            
            # Check if prompt_id exist in catalog
            catalog_entity = self.__st_handler.read_entity(table_name=self.__PROMPT_CATALOG_TABLE_NAME,
                                                           column="prompt_id",
                                                           value=prompt_id)
            if catalog_entity is None:
                return False, "Error reading current prompt in catalog"
            elif len(catalog_entity) == 0:
                return False, "Prompt is not in catalog, first sign up the prompt"
            catalog_entity = catalog_entity[0]

            # Check if prompt_id exist in versioning table
            versioning_entity = self.__st_handler.read_entity(table_name=self.__PROMPT_VERSIONING_TABLE_NAME,
                                                              column="prompt_id",
                                                              value=prompt_id)
            if versioning_entity is None:
                return False, "Error reading current prompt in versioning table"
            elif len(versioning_entity) == 0:
                return False, "Prompt is not in versioning table, first sign up the prompt"
            versioning_entity = versioning_entity[get_highest_version_index(data_list=versioning_entity.copy(), version_key="version")]

            # Create the updated models
            new_prompt_version = increment_version(versioning_entity.get("version"))
            catalog_model = PromptCatalogTableModel(prompt_id=prompt_id,
                                                    prompt_type=catalog_entity.get("prompt_type"),
                                                    prompt=prompt,
                                                    updated_by=user_id,
                                                    version=new_prompt_version)
            versioning_model = PromptVersioningTableModel(user_id=user_id,
                                                          prompt_id=prompt_id,
                                                          prompt_type=versioning_entity.get("prompt_type"),
                                                          prompt=prompt,
                                                          version=new_prompt_version)
            
            # Create prompt on versioning table
            self.__st_handler.create_entity(
                table_name=self.__PROMPT_VERSIONING_TABLE_NAME,
                data=versioning_model.model_dump()
            )

            # Update prompt on catalog table
            self.__st_handler.update_entity(
                row_key=catalog_entity.get("RowKey"),
                table_name=self.__PROMPT_CATALOG_TABLE_NAME,
                data=versioning_model.model_dump()
            ) 
            return True, f"Prompt successfully updated prompt {prompt_id}"
        except Exception as e:
            return False, f"Error signing up prompt: {e}"
