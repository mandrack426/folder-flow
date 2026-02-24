import tempfile
import pandas as pd
from infrastructure.repository import CSVProductRepository


def test_repository_lookup():

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:

        df = pd.DataFrame({
            "CODIGO_BARRA": ["0001"],
            "CODIGO_PRODUTO": ["123"],
            "DESCRICAO_FAMILIA": ["Produto Teste"],
            "COR": ["AZUL"]
        })

        df.to_csv(tmp.name, index=False)

        repo = CSVProductRepository(tmp.name)

        product = repo.get_by_barcode("0001")

        assert product.codigo_produto == "123"