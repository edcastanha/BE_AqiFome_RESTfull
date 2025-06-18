from pydantic import Field, validator
from .base import BaseEntity
from typing import Optional
from decimal import Decimal

class Favorito(BaseEntity):
    """
    Modelo que representa um produto favorito de um cliente.
    Segue os princípios de DDD e Clean Code.
    """
    cliente_id: int = Field(..., description="ID do cliente que favoritou o produto")
    produto_id: int = Field(..., description="ID do produto na API externa")
    titulo: str = Field(..., min_length=1, description="Título do produto")
    imagem: str = Field(..., description="URL da imagem do produto")
    preco: Decimal = Field(..., description="Preço do produto")
    review: Optional[str] = Field(default=None, max_length=500, description="Review/avaliação do produto")
    
    @validator('titulo')
    def validar_titulo(cls, v):
        """Valida se o título não está vazio."""
        if not v or not v.strip():
            raise ValueError('Título não pode estar vazio')
        return v.strip()
    
    @validator('preco')
    def validar_preco(cls, v):
        """Valida se o preço é positivo."""
        if v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }
        schema_extra = {
            "example": {
                "cliente_id": 1,
                "produto_id": 123,
                "titulo": "Produto Exemplo",
                "imagem": "https://example.com/imagem.jpg",
                "preco": 29.99,
                "review": "Excelente produto!"
            }
        }


