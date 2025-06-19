from typing import Optional
from pydantic import BaseModel, ConfigDict

class Favorito(BaseModel):
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
