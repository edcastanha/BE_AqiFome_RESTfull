"""Módulo que define o modelo de domínio para a entidade Produto."""
from typing import Optional
from pydantic import BaseModel, ConfigDict, HttpUrl


class Produto(BaseModel):
    """
    Modelo de domínio para Produto.

    Representa os dados de um produto como recebido da API externa e
    armazenado em nosso banco de dados local (cache).
    """
    id: int
    titulo: str
    preco: float
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    imagem: HttpUrl

    model_config = ConfigDict(from_attributes=True)
