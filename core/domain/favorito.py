from typing import Optional
from pydantic import BaseModel, ConfigDict

class Favorito(BaseModel):
    """
    Modelo de dados para um produto favorito de um cliente.

    Atributos:
        id (Optional[int]): Identificador único do favorito.
        cliente_id (int): ID do cliente.
        produto_id (int): ID do produto (da API externa).
        titulo (str): Título do produto.
        imagem (str): URL da imagem do produto.
        preco (float): Preço do produto.
        review (Optional[str]): Avaliação do produto.
    """
    id: Optional[int]
    cliente_id: int
    produto_id: int
    titulo: str
    imagem: str
    preco: float
    review: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "cliente_id": 1,
                "produto_id": 123,
                "titulo": "Produto Exemplo",
                "imagem": "https://example.com/imagem.jpg",
                "preco": 29.99,
                "review": "Excelente produto!"
            }
        }
    )
