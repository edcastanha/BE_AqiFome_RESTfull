from typing import List
from core.domain.favorito import Favorito, FavoritoResponse
from core.domain.produto import Produto
from core.repository.favorito_repository import FavoritoRepository
from core.repository.produto_repository import ProdutoRepository
from core.externos.fake_store_client import FakeStoreClient

class FavoritoService:
    """
    Serviço de regras de negócio para favoritos de clientes.

    Responsável por validações e operações envolvendo favoritos.
    """
    def __init__(self, repository: FavoritoRepository, produto_repository: ProdutoRepository, fake_store_client: FakeStoreClient):
        """
        Inicializa o serviço de favoritos.

        Args:
            repository (FavoritoRepository): Instância do repositório de favoritos.
            produto_repository (ProdutoRepository): Instância do repositório de produtos.
            fake_store_client (FakeStoreClient): Cliente para a Fake Store API.
        """
        self.repository = repository
        self.produto_repository = produto_repository
        self.fake_store_client = fake_store_client

    async def adicionar_favorito(self, favorito: Favorito) -> Favorito:
        """
        Adiciona um novo favorito para o cliente, validando duplicidade.

        Args:
            favorito (Favorito): Dados do favorito a ser adicionado.
        Returns:
            Favorito: Favorito criado.
        Raises:
            ValueError: Se o produto já estiver nos favoritos do cliente ou não existir.
        """
        if self.repository.exists(favorito.cliente_id, favorito.produto_id):
            raise ValueError("Produto já está nos favoritos do cliente")

        produto = self.produto_repository.get_by_id(favorito.produto_id)
        # Se não estiver no cache, busca na API externa
        if not produto:
            produto_externo = await self.fake_store_client.get_product(favorito.produto_id)
            if not produto_externo:
                raise ValueError("Produto não encontrado")

            # Cria o objeto Produto com os dados externos, agora com todos os campos
            produto = Produto(
                id=produto_externo['id'],
                titulo=produto_externo['title'],
                preco=produto_externo['price'],
                descricao=produto_externo.get('description'),
                categoria=produto_externo.get('category'),
                imagem=produto_externo['image'],
                avaliacao=produto_externo.get('rating', {}).get('rate')
            )
            # Salva o novo produto no nosso banco de dados (cache)
            self.produto_repository.create(produto)

        # Cria a associação do favorito no banco de dados
        return self.repository.create(favorito)

    def listar_favoritos(self, cliente_id: int) -> List[FavoritoResponse]:
        """
        Lista todos os favoritos de um cliente com os detalhes dos produtos.

        Args:
            cliente_id (int): ID do cliente.
        Returns:
            List[FavoritoResponse]: Lista de favoritos do cliente com produtos.
        """
        favoritos = self.repository.list_by_cliente(cliente_id)
        response = []
        for fav in favoritos:
            produto = self.produto_repository.get_by_id(fav.produto_id)
            if produto and fav.id is not None:
                response.append(FavoritoResponse(id=fav.id, cliente_id=fav.cliente_id, produto=produto))
        return response

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
