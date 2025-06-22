from core.domain.favorito import Favorito, FavoritoCreate
from core.config.db import SessionLocal
from core.repository.favorito_orm import FavoritoORM
from sqlalchemy.orm import Session
from typing import Optional, List

class FavoritoRepository:
    """
    Repositório para operações CRUD da entidade Favorito.
    Permite criar, listar, remover e verificar favoritos de clientes no banco de dados.
    """
    def __init__(self, db: Optional[Session] = None):
        """
        Inicializa uma instância do repositório de favoritos.

        Args:
            db (Session, opcional): Sessão do banco de dados SQLAlchemy. Se não fornecida, será criada uma nova sessão.
        """
        self.db = db or SessionLocal()

    def create_many(self, favoritos: List[FavoritoCreate]) -> List[Favorito]:
        """
        Cria múltiplos favoritos para um cliente em uma única transação.

        Args:
            favoritos (List[FavoritoCreate]): Lista de dados dos favoritos a serem criados.
        Returns:
            List[Favorito]: Lista de favoritos criados com IDs atribuídos.
        """
        db_favoritos = [FavoritoORM(cliente_id=f.cliente_id, produto_id=f.produto_id) for f in favoritos]
        self.db.add_all(db_favoritos)
        self.db.commit()
        for db_fav in db_favoritos:
            self.db.refresh(db_fav)
        return [Favorito.model_validate(fav) for fav in db_favoritos]

    def list_by_cliente(self, cliente_id: int) -> List[Favorito]:
        """
        Lista todos os favoritos de um cliente.

        Args:
            cliente_id (int): ID do cliente.
        Returns:
            List[Favorito]: Lista de favoritos do cliente.
        """
        return [Favorito.model_validate(f) for f in self.db.query(FavoritoORM).filter(FavoritoORM.cliente_id == cliente_id).all()]

    def delete(self, cliente_id: int, produto_id: int) -> bool:
        """
        Remove um favorito do cliente.

        Args:
            cliente_id (int): ID do cliente.
            produto_id (int): ID do produto favorito.
        Returns:
            bool: True se removido, False se não encontrado.
        """
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
        """
        Verifica se um produto já está nos favoritos do cliente.

        Args:
            cliente_id (int): ID do cliente.
            produto_id (int): ID do produto.
        Returns:
            bool: True se já existe, False caso contrário.
        """
        return self.db.query(FavoritoORM).filter(
            FavoritoORM.cliente_id == cliente_id,
            FavoritoORM.produto_id == produto_id
        ).first() is not None
