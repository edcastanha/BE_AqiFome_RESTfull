from core.domain.cliente import Cliente, ClienteCreate, ClienteInDB, ClienteUpdate
from core.config.db import SessionLocal
from core.repository.cliente_orm import ClienteORM
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import SecretStr

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

    def create(self, cliente: ClienteCreate) -> Cliente:
        """
        Cria um novo cliente no banco de dados.
        A senha já deve vir com hash do serviço.
        """
        db_cliente = ClienteORM(
            nome=cliente.nome,
            email=cliente.email,
            senha=cliente.senha.get_secret_value(),  # Extrai a string
            tipo=cliente.tipo,
        )
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return Cliente.model_validate(db_cliente)

    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """
        Busca um cliente pelo ID.

        Args:
            cliente_id (int): ID do cliente.
        Returns:
            Optional[Cliente]: Cliente encontrado ou None.
        """
        db_cliente = self.db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
        return Cliente.model_validate(db_cliente) if db_cliente else None

    def get_by_email(self, email: str) -> Optional[ClienteInDB]:
        """
        Busca um cliente pelo e-mail, retornando o modelo com a senha.

        Args:
            email (str): E-mail do cliente.
        Returns:
            Optional[ClienteInDB]: Cliente encontrado ou None.
        """
        db_cliente = self.db.query(ClienteORM).filter(ClienteORM.email == email).first()
        return ClienteInDB.model_validate(db_cliente) if db_cliente else None

    def list(self) -> List[Cliente]:
        """
        Lista todos os clientes cadastrados.

        Returns:
            List[Cliente]: Lista de clientes.
        """
        return [Cliente.model_validate(c) for c in self.db.query(ClienteORM).all()]

    def update(self, cliente_id: int, cliente_update: ClienteUpdate) -> Cliente | None:
        """
        Atualiza os dados de um cliente existente.

        Args:
            cliente_id (int): ID do cliente a ser atualizado.
            cliente_update (ClienteUpdate): Novos dados do cliente (parciais).
        Returns:
            Optional[Cliente]: Cliente atualizado ou None se não encontrado.
        """
        cliente_orm = self.db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
        if cliente_orm:
            update_data = cliente_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                # Se o valor for SecretStr, extrai a string antes de atribuir
                if isinstance(value, SecretStr):
                    setattr(cliente_orm, key, value.get_secret_value())
                else:
                    setattr(cliente_orm, key, value)
            self.db.commit()
            self.db.refresh(cliente_orm)
            return Cliente.model_validate(cliente_orm)
        return None

    def delete(self, cliente_id: int) -> bool:
        """
        Remove um cliente do banco de dados.

        Args:
            cliente_id (int): ID do cliente a ser removido.
        Returns:
            bool: True se removido, False se não encontrado.
        """
        db_cliente = (
            self.db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
        )
        if not db_cliente:
            return False
        self.db.delete(db_cliente)
        self.db.commit()
        return True
