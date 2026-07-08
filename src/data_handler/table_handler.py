import pandas as pd

from src.utils.utils import normalize_list, inverse_normalize_list


class TableHandler:
    def __init__(self, path: str):
        self.df = pd.read_excel(path, engine="openpyxl")
    
    def normalize_columns(self, columns: list[str], prefix: str = "norm_", inverted_columns: list[str] = []):
        for column in columns:
            if column in inverted_columns:
                self.df[f"{prefix}{column}"] = inverse_normalize_list(self.df[column].to_list())
            else:
                self.df[f"{prefix}{column}"] = normalize_list(self.df[column].to_list())
    
    def save_table(self, desired_path: str):
        self.df.to_excel(desired_path, index=False, engine="openpyxl")

    def get_table(self):
        return self.df.copy()
    
    def set_table(self, df: pd.DataFrame):
        self.df = df.copy()