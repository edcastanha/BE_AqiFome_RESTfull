from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class Produtos_Cache(BaseModel):
    """ 
    Modelo que representa um produto da Fake Store API.
    Segue os princípios de DDD e Clean Code para representar
    a entidade externa de forma clara e consistente.
    """
    id: int = Field(description="Identificador único do produto")
    titulo: str = Field(description="Nome/título do produto")
    preco: Decimal = Field(description="Preço do produto")
    descricao: str = Field(description="Descrição detalhada do produto")
    categoria: str = Field(description="Categoria do produto")
    imagem: str = Field(description="URL da imagem do produto")
    rating: Optional[dict] = Field(default=None, description="Informações de avaliação do produto")
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        } 