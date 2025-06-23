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
    descricao = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    imagem = Column(String, nullable=False)

    def __init__(self, *args, **kwargs):
        if 'imagem' in kwargs and hasattr(kwargs['imagem'], 'unicode_string'):
            kwargs['imagem'] = kwargs['imagem'].unicode_string()
        elif 'imagem' in kwargs and not isinstance(kwargs['imagem'], str):
            kwargs['imagem'] = str(kwargs['imagem'])

        super().__init__(*args, **kwargs)
