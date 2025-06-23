from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class FavoritoBase(BaseModel):
    """Modelo base para Favorito com campos comuns."""
    cliente_id: int
    produto_id: int

class Favorito(FavoritoBase):
    """
    Modelo de domínio principal para Favorito.
    Representa um favorito como ele existe no banco de dados.
    """
    id: int

    model_config = ConfigDict(from_attributes=True)

class FavoritoCreate(FavoritoBase):
    """DTO para criar um favorito (cliente_id, produto_id)."""
    pass

class ProdutoExterno(BaseModel):
    id: int
    titulo: str
    imagem: str
    preco: float
    # Adicione outros campos relevantes conforme a API externa

class FavoritoResponse(BaseModel):
    id: int
    cliente_id: int
    produto: ProdutoExterno | dict

    model_config = ConfigDict(from_attributes=True)

class FavoritoCreateRequest(BaseModel):
    produto_ids: list[int]
