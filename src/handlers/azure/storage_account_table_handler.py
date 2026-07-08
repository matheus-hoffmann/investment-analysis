import os
import json
from azure.data.tables import TableServiceClient, UpdateMode

from src.config.logger import set_logger
from src.handlers.abstract.data_table_interface import DataTableInterface

logger = set_logger("AZURE STORAGE ACCOUNT TABLE")


class StorageAccountTableHandler(DataTableInterface):
    def __init__(self):
        super().__init__()
    
    def set_client(self):
        try:
            account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
            api_key = os.getenv('AZURE_STORAGE_API_KEY')
            connection_string = f"AccountName={account_name};AccountKey={api_key};EndpointSuffix=core.windows.net"
            client = TableServiceClient.from_connection_string(conn_str=connection_string)
            return client
        except Exception as e:
            logger.error(f"Error creating service client: {e}")
            return None
    
    def create_table(self, table_name: str):
        try:
            self.set_client().create_table(table_name=table_name)
            return True
        except Exception as e:
            logger.error(f"Error creating table {table_name}: {e}")
            return False
    
    def delete_table(self, table_name: str):
        try:
            self.set_client().delete_table(table_name=table_name)
            return True
        except Exception as e:
            logger.error(f"Error deleting table {table_name}: {e}")
            return False
    
    def check_if_table_exists(self, table_name: str):
        try:
            list(self.set_client().get_table_client(table_name=table_name).list_entities(results_per_page=1))
            return True
        except Exception as e:
            return False

    def create_entity(self, table_name: str, data: dict):
        try:
            entity = self.check_entity(data.copy())
            entity = self.add_primary_key_infos(entity.copy(), table_name)
            table_client = self.set_client().get_table_client(table_name=table_name)
            table_client.create_entity(entity=entity)
            return entity['RowKey']
        except Exception as e:
            logger.error(f"Error creating entity on table {table_name}: {e}")
            return None

    def read_entity(self, table_name: str, column: str, value):
        try:
            table_client = self.set_client().get_table_client(table_name=table_name)
            if type(value) is str:
                filter_string = f"{column} eq '{value}'"
            else:
                filter_string = f"{column} eq {json.dumps(value)}"
            entities = [entity for entity in table_client.query_entities(filter_string)]
            return entities
        except Exception as e:
            logger.error(f"Error searching entity on table {table_name}: {e}")
            return None
    
    def update_entity(self, table_name: str, row_key: str, data: dict):
        try:
            entity = self.check_entity(data.copy())
            entity['PartitionKey'] = table_name
            entity['RowKey'] = row_key
            table_client = self.set_client().get_table_client(table_name=table_name)
            table_client.upsert_entity(entity=entity, mode=UpdateMode.MERGE)
            return True
        except Exception as e:
            logger.error(f"Error updating entity on table {table_name}: {e}")
            return False

    def delete_entity(self, table_name: str, row_key: str):
        try:
            table_client = self.set_client().get_table_client(table_name=table_name)
            table_client.delete_entity(partition_key=table_name, row_key=row_key)
            return True
        except Exception as e:
            logger.error(f"Error deleting entity on table {table_name}: {e}")
            return False
    
    def generic_filter(self, table_name: str, filter: dict):
        try:
            table_client = self.set_client().get_table_client(table_name=table_name)
            conditions_list = []
            for k, v in filter.items():
                if type(v) is str:
                    conditions_list.append(f"{k} eq '{v}'")
                else:
                    conditions_list.append(f"{k} eq {json.dumps(v)}")
            filter_string = " and ".join(conditions_list)
            entities = [entity for entity in table_client.query_entities(filter_string)]
            return entities
        except Exception as e:
            logger.error(f"Error searching entity on table {table_name}: {e}")
            return None