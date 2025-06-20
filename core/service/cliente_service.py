from core.domain.cliente import Cliente
from core.repository.cliente_repository import ClienteRepository

class ClienteService:
    """
    Serviço de regras de negócio para clientes.

    Responsável por validações e operações de alto nível envolvendo clientes.
    """
    def __init__(self, repository: ClienteRepository):
        """
        Inicializa o serviço de clientes.

        Args:
            repository (ClienteRepository): Instância do repositório de clientes.
        """
        self.repository = repository

    def criar_cliente(self, cliente: Cliente) -> Cliente:
        """
        Cria um novo cliente após validação de unicidade do e-mail.

        Args:
            cliente (Cliente): Dados do cliente a ser criado.
        Returns:
            Cliente: Cliente criado.
        Raises:
            ValueError: Se o e-mail já estiver cadastrado.
        """
        if self.repository.get_by_email(cliente.email):
            raise ValueError("E-mail já cadastrado")
        return self.repository.create(cliente)

    def listar_clientes(self):
        """
        Lista todos os clientes cadastrados.

        Returns:
            list[Cliente]: Lista de clientes.
        """
        return self.repository.list()

    def buscar_cliente(self, cliente_id: int):
        """
        Busca um cliente pelo ID.

        Args:
            cliente_id (int): ID do cliente.
        Returns:
            Cliente ou None: Cliente encontrado ou None.
        """
        return self.repository.get_by_id(cliente_id)

    def atualizar_cliente(self, cliente_id: int, cliente: Cliente):
        """
        Atualiza os dados de um cliente existente.

        Args:
            cliente_id (int): ID do cliente a ser atualizado.
            cliente (Cliente): Novos dados do cliente.
        Returns:
            Cliente ou None: Cliente atualizado ou None se não encontrado.
        """
        return self.repository.update(cliente_id, cliente)

    def deletar_cliente(self, cliente_id: int):
        """
        Remove um cliente do banco de dados.

        Args:
            cliente_id (int): ID do cliente a ser removido.
        Returns:
            bool: True se removido, False caso contrário.
        """
        return self.repository.delete(cliente_id)
