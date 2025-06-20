from core.domain.favorito import Favorito
from core.repository.favorito_repository import FavoritoRepository
from typing import List

class FavoritoService:
    """
    Serviço de regras de negócio para favoritos de clientes.

    Responsável por validações e operações envolvendo favoritos.
    """
    def __init__(self, repository: FavoritoRepository):
        """
        Inicializa o serviço de favoritos.

        Args:
            repository (FavoritoRepository): Instância do repositório de favoritos.
        """
        self.repository = repository

    def adicionar_favorito(self, favorito: Favorito) -> Favorito:
        """
        Adiciona um novo favorito para o cliente, validando duplicidade.

        Args:
            favorito (Favorito): Dados do favorito a ser adicionado.
        Returns:
            Favorito: Favorito criado.
        Raises:
            ValueError: Se o produto já estiver nos favoritos do cliente.
        """
        if self.repository.exists(favorito.cliente_id, favorito.produto_id):
            raise ValueError("Produto já está nos favoritos do cliente")
        return self.repository.create(favorito)

    def listar_favoritos(self, cliente_id: int) -> List[Favorito]:
        """
        Lista todos os favoritos de um cliente.

        Args:
            cliente_id (int): ID do cliente.
        Returns:
            List[Favorito]: Lista de favoritos do cliente.
        """
        return self.repository.list_by_cliente(cliente_id)

    def remover_favorito(self, cliente_id: int, produto_id: int) -> bool:
        """
        Remove um favorito do cliente.

        Args:
            cliente_id (int): ID do cliente.
            produto_id (int): ID do produto favorito.
        Returns:
            bool: True se removido, False caso contrário.
        """
        return self.repository.delete(cliente_id, produto_id)
