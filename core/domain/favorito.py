from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from core.domain.produto import Produto


class FavoritoBase(BaseModel):
    """Modelo base para Favorito com campos comuns."""
    cliente_id: int
    produto_id: int


class FavoritoCreateRequest(BaseModel):
    """DTO para a requisição de criação de um ou mais favoritos."""
    produto_ids: List[int]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "produto_ids": [1, 2, 3]
            }
        }
    )


class FavoritoCreate(FavoritoBase):
    """DTO interno para criar um favorito."""
    pass


class Favorito(FavoritoBase):
    """
    Modelo de domínio principal para Favorito.
    Representa um favorito como ele existe no banco de dados.
    """
    id: int
    produto: Optional[Produto] = None

    model_config = ConfigDict(from_attributes=True)


class FavoritoResponse(BaseModel):
    """
    Modelo de resposta para um favorito, incluindo os detalhes do produto.
    """
    id: int
    cliente_id: int
    produto: Produto

    model_config = ConfigDict(from_attributes=True)
