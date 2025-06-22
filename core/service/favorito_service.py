from typing import List
from core.domain.favorito import Favorito, FavoritoResponse, FavoritoCreate
from core.domain.produto import Produto
from core.repository.favorito_repository import FavoritoRepository
from core.repository.produto_repository import ProdutoRepository
from core.externos.fake_store_product import FakeStoreProduct

class FavoritoService:
    """
    Serviço de regras de negócio para favoritos de clientes.

    Responsável por validações e operações envolvendo favoritos.
    """
    def __init__(self, repository: FavoritoRepository, produto_repository: ProdutoRepository, fake_store_product: FakeStoreProduct):
        """
        Inicializa o serviço de favoritos.

        Args:
            repository (FavoritoRepository): Instância do repositório de favoritos.
            produto_repository (ProdutoRepository): Instância do repositório de produtos.
            fake_store_product (FakeStoreProduct): Cliente para a Fake Store API.
        """
        self.repository = repository
        self.produto_repository = produto_repository
        self.fake_store_product = fake_store_product

    async def adicionar_favoritos(self, cliente_id: int, produto_ids: List[int]) -> List[FavoritoResponse]:
        """
        Adiciona uma lista de novos produtos favoritos para o cliente.

        Args:
            cliente_id (int): ID do cliente.
            produto_ids (List[int]): Lista de IDs dos produtos a serem adicionados.
        Returns:
            List[FavoritoResponse]: Lista de favoritos criados.
        Raises:
            ValueError: Se algum produto já for favorito ou não existir.
        """
        favoritos_para_criar = []
        produtos_processados = set()

        for produto_id in produto_ids:
            if produto_id in produtos_processados:
                continue

            if self.repository.exists(cliente_id, produto_id):
                # Pular produtos que já são favoritos em vez de lançar um erro
                continue

            produto = self.produto_repository.get_by_id(produto_id)
            if not produto:
                produto_externo = await self.fake_store_product.get_product(produto_id)
                if not produto_externo:
                    # Pular produtos não encontrados na API externa
                    continue
                
                produto = Produto(
                    id=produto_externo['id'],
                    titulo=produto_externo['title'],
                    preco=produto_externo['price'],
                    descricao=produto_externo.get('description'),
                    categoria=produto_externo.get('category'),
                    imagem=produto_externo['image'],
               )
                self.produto_repository.create(produto)

            favoritos_para_criar.append(FavoritoCreate(cliente_id=cliente_id, produto_id=produto_id))
            produtos_processados.add(produto_id)

        if not favoritos_para_criar:
            # Se nenhum favorito novo foi adicionado, retorna a lista atual
            return self.listar_favoritos(cliente_id)

        self.repository.create_many(favoritos_para_criar)
        
        # Retorna a lista completa e atualizada de favoritos
        return self.listar_favoritos(cliente_id)

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
