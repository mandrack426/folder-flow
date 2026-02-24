import pandas as pd
from domain.interfaces import ProductRepositoryInterface
from domain.entities import Product


class CSVProductRepository(ProductRepositoryInterface):

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._cache: dict[str, Product] = {}
        self._load_data()

    def _load_data(self):

        if self.file_path.endswith(".csv"):
            df = pd.read_csv(self.file_path, dtype=str)
        else:
            df = pd.read_excel(self.file_path, dtype=str)

        df = df.fillna("")

        required_columns = [
            "CODIGO_BARRA",
            "CODIGO_PRODUTO",
            "DESCRICAO_FAMILIA",
            "COR"
        ]

        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Coluna obrigatória ausente: {col}")

        for _, row in df.iterrows():
            product = Product(
                codigo_barra=row["CODIGO_BARRA"],
                codigo_produto=row["CODIGO_PRODUTO"],
                descricao_familia=row["DESCRICAO_FAMILIA"],
                cor=row["COR"]
            )

            self._cache[row["CODIGO_BARRA"]] = product

    def get_by_barcode(self, barcode: str):
        return self._cache.get(str(barcode))