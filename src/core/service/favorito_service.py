from typing import List
from core.domain.favorito import Favorito, FavoritoResponse, FavoritoCreate
from core.repository.favorito_repository import FavoritoRepository
from core.externos.fake_store_product import FakeStoreProduct
import redis
import json

class FavoritoService:
    """
    Serviço de regras de negócio para favoritos de clientes.
    Agora utiliza cache Redis para produtos externos.
    """
    def __init__(self, repository: FavoritoRepository, fake_store_product: FakeStoreProduct, redis_client=None):
        """
        Inicializa o serviço de favoritos.

        Args:
            repository (FavoritoRepository): Instância do repositório de favoritos.
            fake_store_product (FakeStoreProduct): Cliente para a Fake Store API.
            redis_client: Cliente Redis para cache de produtos externos.
        """
        self.repository = repository
        self.fake_store_product = fake_store_product
        self.redis = redis_client or redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

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

            # Busca produto no cache Redis
            produto_cache = self.redis.get(f"produto:{produto_id}")
            if produto_cache:
                produto_externo = json.loads(produto_cache)
            else:
                produto_externo = await self.fake_store_product.get_product(produto_id)
                if not produto_externo:
                    # Pular produtos não encontrados na API externa
                    continue
                
                self.redis.set(f"produto:{produto_id}", json.dumps(produto_externo), ex=3600)

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
            produto_cache = self.redis.get(f"produto:{fav.produto_id}")
            if produto_cache:
                produto_externo = json.loads(produto_cache)
            else:
                produto_externo = None
            if produto_externo and fav.id is not None:
                response.append(FavoritoResponse(id=fav.id, cliente_id=fav.cliente_id, produto=produto_externo))
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
