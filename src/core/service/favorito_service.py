from typing import List
from core.domain.favorito import Favorito, FavoritoCreate, FavoritoResponse, ProdutoExterno
from core.repository.favorito_repository import FavoritoRepository
from externos.fake_store_product import FakeStoreProduct
from core.config.redis_config import RedisConfig
import redis
import json

class FavoritoService:
    """
    Serviço de regras de negócio para favoritos de clientes.
    Utiliza cache Redis para produtos externos.
    """
    def __init__(self, repository: FavoritoRepository, fake_store_product: FakeStoreProduct, redis_client=None, redis_expires=None):
        self.repository = repository
        self.fake_store_product = fake_store_product
        if redis_client is None:
            redis_config = RedisConfig()
            self.redis = redis_config.get_client()
            self.redis_expires = redis_config.get_expires() if redis_expires is None else redis_expires
        else:
            self.redis = redis_client
            self.redis_expires = redis_expires or 3600

    async def adicionar_favoritos(self, cliente_id: int, produto_ids: list[int]) -> list[FavoritoResponse]:
        favoritos_para_criar = []
        produtos_processados = set()
        for produto_id in produto_ids:
            if produto_id in produtos_processados:
                continue
            if self.repository.exists(cliente_id, produto_id):
                continue
            produto_cache = self.redis.get(f"produto:{produto_id}")
            if produto_cache:
                produto_externo = json.loads(produto_cache)
            else:
                produto_externo = await self.fake_store_product.get_product(produto_id)
                if not produto_externo:
                    continue
                self.redis.set(f"produto:{produto_id}", json.dumps(produto_externo), ex=self.redis_expires)
            favoritos_para_criar.append(FavoritoCreate(cliente_id=cliente_id, produto_id=produto_id))
            produtos_processados.add(produto_id)
        if not favoritos_para_criar:
            return self.listar_favoritos(cliente_id)
        self.repository.create_many(favoritos_para_criar)
        return self.listar_favoritos(cliente_id)

    def listar_favoritos(self, cliente_id: int) -> list[FavoritoResponse]:
        favoritos = self.repository.list_by_cliente(cliente_id)
        response = []
        for fav in favoritos:
            produto_cache = self.redis.get(f"produto:{fav.produto_id}")
            if produto_cache:
                produto_externo = json.loads(produto_cache)
            else:
                # Busca na API externa e salva no cache se não estiver em cache
                produto_externo = self.fake_store_product.get_product_sync(fav.produto_id)
                if produto_externo:
                    self.redis.set(f"produto:{fav.produto_id}", json.dumps(produto_externo), ex=self.redis_expires)
            if produto_externo and fav.id is not None:
                response.append(FavoritoResponse(id=fav.id, cliente_id=fav.cliente_id, produto=produto_externo))
        return response

    def remover_favorito(self, cliente_id: int, produto_id: int) -> bool:
        return self.repository.delete(cliente_id, produto_id)