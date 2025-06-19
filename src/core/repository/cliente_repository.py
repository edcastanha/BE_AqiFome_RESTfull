from src.core.domain.cliente import Cliente
from src.core.config.db import SessionLocal
from src.core.repository.cliente_orm import ClienteORM
from sqlalchemy.orm import Session
from typing import Optional, List

class ClienteRepository:
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def create(self, cliente: Cliente) -> Cliente:
        db_cliente = ClienteORM(nome=cliente.nome, email=cliente.email)
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return Cliente.from_orm(db_cliente)

    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        db_cliente = self.db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
        return Cliente.from_orm(db_cliente) if db_cliente else None

    def get_by_email(self, email: str) -> Optional[Cliente]:
        db_cliente = self.db.query(ClienteORM).filter(ClienteORM.email == email).first()
        return Cliente.from_orm(db_cliente) if db_cliente else None

    def list(self) -> List[Cliente]:
        return [Cliente.from_orm(c) for c in self.db.query(ClienteORM).all()]

    def update(self, cliente_id: int, cliente: Cliente) -> Optional[Cliente]:
        db_cliente = self.db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
        if not db_cliente:
            return None
        db_cliente.nome = cliente.nome
        db_cliente.email = cliente.email
        self.db.commit()
        self.db.refresh(db_cliente)
        return Cliente.from_orm(db_cliente)

    def delete(self, cliente_id: int) -> bool:
        db_cliente = self.db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
        if not db_cliente:
            return False
        self.db.delete(db_cliente)
        self.db.commit()
        return True
