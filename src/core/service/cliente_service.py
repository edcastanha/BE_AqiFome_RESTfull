from src.core.domain.cliente import Cliente
from src.core.repository.cliente_repository import ClienteRepository

class ClienteService:
    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    def criar_cliente(self, cliente: Cliente) -> Cliente:
        if self.repository.get_by_email(cliente.email):
            raise ValueError("E-mail já cadastrado")
        return self.repository.create(cliente)

    def listar_clientes(self):
        return self.repository.list()

    def buscar_cliente(self, cliente_id: int):
        return self.repository.get_by_id(cliente_id)

    def atualizar_cliente(self, cliente_id: int, cliente: Cliente):
        return self.repository.update(cliente_id, cliente)

    def deletar_cliente(self, cliente_id: int):
        return self.repository.delete(cliente_id)
