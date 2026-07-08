import pandas as pd
from src.data_handler.table_handler import TableHandler


class ComputeScoreUC:
    """
    https://fundamentus.com.br/fii_resultado.php
    """
    def __init__(self, path: str):
        self.tb_handler = TableHandler(path=path)

        self.__segments = [
            'Outros',
            'Shoppings',
            'Multicategoria',
            'Logística',
            'Títulos e Val. Mob.',
            'Varejo',
            'Escritórios',
            'Residencial',
            'Híbrido',
            'Hotel',
            'Hospital',
            'Lajes Corporativas'
        ]
        self.__normalized_prefix = "norm_"

        self.important_columns = {
            "Dividend Yield": 0.3,
            "P/VP": 0.35,
            "Liquidez": 0.1,
            "Qtd de imóveis": 0.1,
            "Vacância Média": 0.15
        }

        self.tb_handler.normalize_columns(columns=list(self.important_columns.keys()), prefix=self.__normalized_prefix, inverted_columns=["Vacância Média"])
    
    def execute(self, 
                min_dividend_yield: float = 0.07,
                max_dividend_yield: float = 0.25,
                min_liquidez: float = 1500000,
                max_vacancia: float = 0.3,
                min_p_vp: float = 0.85,
                max_p_vp: float = 1.05,
                segmento: list = []
                ) -> pd.DataFrame:

        _segmento = self.__segments if segmento == [] else segmento

        df = self.tb_handler.get_table()
        valid_df = df[
            (df['Dividend Yield'] >= min_dividend_yield) &
            (df['Dividend Yield'] <= max_dividend_yield) &
            (df['P/VP'] >= min_p_vp) &
            (df['P/VP'] <= max_p_vp) &
            (df['Liquidez'] >= min_liquidez) &
            (df['Vacância Média'] <= max_vacancia) &
            (df['Segmento'].isin(_segmento))
        ].reset_index(drop=True)

        scores = []
        for _, row in valid_df.iterrows():
            score = sum([weight * row[f"{self.__normalized_prefix}{column}"] for column, weight in self.important_columns.items()])
            scores.append(score)

        valid_df['score'] = scores

        valid_df = valid_df.sort_values(
            "score",
            ascending=False
        ).reset_index(drop=True)

        return valid_df.copy()