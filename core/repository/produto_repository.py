from sqlalchemy.orm import Session
from typing import Optional
from core.domain.produto import Produto
from core.repository.produto_orm import ProdutoORM
from core.config.db import SessionLocal

class ProdutoRepository:
    """
    Repositório para operações de persistência da entidade Produto.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, produto_id: int) -> Optional[Produto]:
        """
        Busca um produto pelo seu ID.
        """
        db_produto = self.db.query(ProdutoORM).filter(ProdutoORM.id == produto_id).first()
        return Produto.model_validate(db_produto) if db_produto else None

    def create(self, produto: Produto) -> Produto:
        """
        Salva um novo produto no banco de dados.
        """
        db_produto = ProdutoORM(
            id=produto.id,
            titulo=produto.titulo,
            imagem=produto.imagem,
            preco=produto.preco,
            review=produto.review
        )
        self.db.add(db_produto)
        self.db.commit()
        self.db.refresh(db_produto)
        return Produto.model_validate(db_produto)
