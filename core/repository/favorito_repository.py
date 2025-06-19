from core.domain.favorito import Favorito
from core.config.db import SessionLocal
from core.repository.favorito_orm import FavoritoORM
from sqlalchemy.orm import Session
from typing import Optional, List

class FavoritoRepository:
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def create(self, favorito: Favorito) -> Favorito:
        db_fav = FavoritoORM(
            cliente_id=favorito.cliente_id,
            produto_id=favorito.produto_id,
            titulo=favorito.titulo,
            imagem=favorito.imagem,
            preco=favorito.preco,
            review=favorito.review
        )
        self.db.add(db_fav)
        self.db.commit()
        self.db.refresh(db_fav)
        return Favorito.from_orm(db_fav)

    def list_by_cliente(self, cliente_id: int) -> List[Favorito]:
        return [Favorito.from_orm(f) for f in self.db.query(FavoritoORM).filter(FavoritoORM.cliente_id == cliente_id).all()]

    def delete(self, cliente_id: int, produto_id: int) -> bool:
        db_fav = self.db.query(FavoritoORM).filter(
            FavoritoORM.cliente_id == cliente_id,
            FavoritoORM.produto_id == produto_id
        ).first()
        if not db_fav:
            return False
        self.db.delete(db_fav)
        self.db.commit()
        return True

    def exists(self, cliente_id: int, produto_id: int) -> bool:
        return self.db.query(FavoritoORM).filter(
            FavoritoORM.cliente_id == cliente_id,
            FavoritoORM.produto_id == produto_id
        ).first() is not None
