from typing import Optional
from pydantic import BaseModel, ConfigDict
from core.domain.produto import Produto


class FavoritoBase(BaseModel):
    """Modelo base para Favorito com campos comuns."""
    cliente_id: int
    produto_id: int


class FavoritoCreate(FavoritoBase):
    """
    DTO para a criação de um novo favorito (entrada da API).
    Contém os IDs do cliente e do produto."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "cliente_id": 1,
                "produto_id": 10
            }
        } 
    )


class FavoritoCreateRequest(BaseModel):
    """DTO para a requisição de criação de um favorito."""
    produto_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "produto_id": 1
            }
        }
    )


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
