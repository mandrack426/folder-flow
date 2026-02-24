import re
import unicodedata
from domain.entities import Product


def normalize_text(text: str) -> str:
    """
    Regras:
    - minúsculo
    - remove acentos
    - troca '/' por '-'
    - mantém hífen
    - remove caracteres especiais
    - espaços -> _
    """

    text = text.lower()
    text = text.replace("/", "-")

    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")

    text = re.sub(r"[^a-z0-9\-\s]", "", text)
    text = re.sub(r"\s+", "-", text.strip())

    return text


def build_folder_name(product: Product) -> str:
    descricao_norm = normalize_text(product.descricao_familia)
    cor_norm = normalize_text(product.cor)

    base = f"{descricao_norm}-{cor_norm}"

    return f"{product.codigo_produto}-{base}"