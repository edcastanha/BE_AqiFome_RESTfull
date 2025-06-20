from core.domain.cliente import Cliente
from core.config.db import SessionLocal
from core.repository.cliente_orm import ClienteORM
from sqlalchemy.orm import Session
from typing import Optional, List

class ClienteRepository:
    """
    Repositório para operações CRUD da entidade Cliente.

    Permite criar, buscar, listar, atualizar e deletar clientes no banco de dados.
    Pode receber uma sessão do SQLAlchemy para facilitar testes e integração.
    """
    def __init__(self, db: Optional[Session] = None):
        """
        Inicializa uma instância do repositório de clientes.

        Args:
            db (Optional[Session]): Sessão do banco de dados SQLAlchemy. Se não fornecida, será criada uma nova sessão.
        """
        self.db = db or SessionLocal()

    def create(self, cliente: Cliente) -> Cliente:
        """
        Cria um novo cliente no banco de dados.

        Args:
            cliente (Cliente): Dados do cliente a ser criado.
        Returns:
            Cliente: Cliente criado com ID atribuído.
        """
        db_cliente = ClienteORM(nome=cliente.nome, email=cliente.email)
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return Cliente.from_orm(db_cliente)

    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """
        Busca um cliente pelo ID.

        Args:
            cliente_id (int): ID do cliente.
        Returns:
            Optional[Cliente]: Cliente encontrado ou None.
        """
        db_cliente = self.db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
        return Cliente.from_orm(db_cliente) if db_cliente else None

    def get_by_email(self, email: str) -> Optional[Cliente]:
        """
        Busca um cliente pelo e-mail.

        Args:
            email (str): E-mail do cliente.
        Returns:
            Optional[Cliente]: Cliente encontrado ou None.
        """
        db_cliente = self.db.query(ClienteORM).filter(ClienteORM.email == email).first()
        return Cliente.from_orm(db_cliente) if db_cliente else None

    def list(self) -> List[Cliente]:
        """
        Lista todos os clientes cadastrados.

        Returns:
            List[Cliente]: Lista de clientes.
        """
        return [Cliente.from_orm(c) for c in self.db.query(ClienteORM).all()]

    def update(self, cliente_id: int, cliente: Cliente) -> Optional[Cliente]:
        """
        Atualiza os dados de um cliente existente.

        Args:
            cliente_id (int): ID do cliente a ser atualizado.
            cliente (Cliente): Novos dados do cliente.
        Returns:
            Optional[Cliente]: Cliente atualizado ou None se não encontrado.
        """
        db_cliente = self.db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
        if not db_cliente:
            return None
        db_cliente.nome = cliente.nome
        db_cliente.email = cliente.email
        self.db.commit()
        self.db.refresh(db_cliente)
        return Cliente.from_orm(db_cliente)

    def delete(self, cliente_id: int) -> bool:
        """
        Remove um cliente do banco de dados.

        Args:
            cliente_id (int): ID do cliente a ser removido.
        Returns:
            bool: True se removido, False se não encontrado.
        """
        db_cliente = self.db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
        if not db_cliente:
            return False
        self.db.delete(db_cliente)
        self.db.commit()
        return True
