"""
Módulo que define o mapeamento ORM para a entidade Produto.
"""
from sqlalchemy import Column, Integer, String, Float
from core.config.db import Base


class ProdutoORM(Base):
    """Modelo ORM para a tabela 'produtos'."""
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    descricao = Column(String, nullable=True)
    categoria = Column(String, nullable=True)
    imagem = Column(String, nullable=False)
    avaliacao = Column(Float, nullable=True)
