from core.domain.favorito import Favorito
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

    def create(self, favorito: Favorito) -> Favorito:
        """
        Cria um novo favorito para um cliente.

        Args:
            favorito (Favorito): Dados do favorito a ser criado.
        Returns:
            Favorito: Favorito criado com ID atribuído.
        """
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
        """
        Lista todos os favoritos de um cliente.

        Args:
            cliente_id (int): ID do cliente.
        Returns:
            List[Favorito]: Lista de favoritos do cliente.
        """
        return [Favorito.from_orm(f) for f in self.db.query(FavoritoORM).filter(FavoritoORM.cliente_id == cliente_id).all()]

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
