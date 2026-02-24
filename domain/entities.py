from dataclasses import dataclass


@dataclass
class Product:
    codigo_barra: str
    codigo_produto: str
    descricao_familia: str
    cor: str