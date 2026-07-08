import uuid
import json
from abc import ABC, abstractmethod


class DataTableInterface(ABC):
    @abstractmethod
    def set_client(self):
        ...
    
    @abstractmethod
    def create_table(self, table_name: str):
        ...
    
    @abstractmethod
    def delete_table(self, table_name: str):
        ...
    
    @abstractmethod
    def check_if_table_exists(self, table_name: str):
        ...
    
    @abstractmethod
    def create_entity(self, table_name: str, data: dict):
        ...

    @abstractmethod
    def read_entity(self, table_name: str, column: str, value):
        ...
    
    @abstractmethod
    def update_entity(self, table_name: str, row_key: str, data: dict):
        ...

    @abstractmethod
    def delete_entity(self, table_name: str, row_key: str):
        ...
    
    @abstractmethod
    def generic_filter(self, table_name: str, filter: dict):
        ...

    def check_entity(self, data: dict):
        valid_data = data.copy()
        for k, v in valid_data.items():
            if type(v) is list or type(v) is dict:
                valid_data[k] = json.dumps(v)
        return valid_data.copy()
    
    def add_primary_key_infos(self, data: dict, table_name: str):
        entity = data.copy()
        entity['PartitionKey'] = table_name
        entity['RowKey'] = uuid.uuid4().__str__()
        return entity.copy()