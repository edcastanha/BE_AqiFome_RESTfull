from unittest.mock import MagicMock, AsyncMock, call
import pytest
from core.domain.favorito import Favorito, FavoritoResponse, FavoritoCreate, ProdutoExterno
from core.service.favorito_service import FavoritoService
from externos.fake_store_product import FakeStoreProduct

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_dependencies():
    """Fixture para criar mocks das dependências do FavoritoService."""
    mock_repo = MagicMock()
    mock_fake_store = AsyncMock(spec=FakeStoreProduct)
    mock_redis = MagicMock()
    return mock_repo, mock_fake_store, mock_redis


@pytest.fixture
def service(mock_dependencies):
    """Fixture para criar uma instância do FavoritoService com mocks."""
    mock_repo, mock_fake_store, mock_redis = mock_dependencies
    return FavoritoService(
        repository=mock_repo, fake_store_product=mock_fake_store, redis_client=mock_redis
    )


async def test_adicionar_favoritos_com_sucesso(service, mock_dependencies):
    """Testa adicionar favoritos com sucesso (cache miss e hit)."""
    mock_repo, mock_fake_store, mock_redis = mock_dependencies

    # --- Configuração dos Mocks ---
    # Produto 1 (cache hit), Produto 2 (cache miss), Produto 3 (já favorito)
    mock_redis.get.side_effect = [
        b'{"id": 1, "titulo": "P1 Cache", "preco": 10, "imagem": "http://img1.com/img01.png"}', # P1
        None, # P2
    ]
    mock_fake_store.get_product.return_value = {
        "id": 2, "title": "P2 API", "price": 20, "image": "http://img2.com/img02.png"
    }
    mock_repo.exists.side_effect = [False, False, True] # P1, P2, P3
    service.listar_favoritos = MagicMock(return_value=[]) # Mock para a chamada final

    # --- Execução ---
    await service.adicionar_favoritos(cliente_id=1, produto_ids=[1, 2, 3])

    # --- Verificações ---
    # 1. Verificação de existência
    mock_repo.exists.assert_has_calls([call(1, 1), call(1, 2), call(1, 3)])

    # 2. Acesso ao cache Redis
    mock_redis.get.assert_has_calls([call("produto:1"), call("produto:2")])

    # 3. Acesso à API externa (apenas para P2, que não estava em cache)
    mock_fake_store.get_product.assert_called_once_with(2)

    # 4. Cache do produto P2
    mock_redis.set.assert_called_once()

    # 5. Criação dos favoritos em lote (apenas P1 e P2)
    mock_repo.create_many.assert_called_once()
    args, _ = mock_repo.create_many.call_args
    assert len(args[0]) == 2
    assert args[0][0].produto_id == 1
    assert args[0][1].produto_id == 2

async def test_listar_favoritos(service, mock_dependencies):
    """Testa a listagem de favoritos, buscando dados do cache e da API externa."""
    mock_repo, mock_fake_store, mock_redis = mock_dependencies

    # --- Configuração ---
    mock_repo.list_by_cliente.return_value = [
        Favorito(id=1, cliente_id=1, produto_id=10),
        Favorito(id=2, cliente_id=1, produto_id=20)
    ]
    mock_redis.get.side_effect = [
        b'{"id": 10, "titulo": "P10 Cache", "preco": 10, "imagem": "img10.png"}', # P10 (cache hit)
        None # P20 (cache miss)
    ]
    mock_fake_store.get_product_sync.return_value = {
        "id": 20, "titulo": "P20 API", "preco": 20, "imagem": "img20.png"
    }

    # --- Execução ---
    response = service.listar_favoritos(cliente_id=1)

    # --- Verificações -- -
    assert len(response) == 2
    assert response[0].produto.titulo == "P10 Cache"
    assert response[1].produto.titulo == "P20 API"
    mock_fake_store.get_product_sync.assert_called_once_with(20)

    # Verifica se o produto foi adicionado ao cache
    mock_redis.set.assert_called_once_with("produto:20", '''{"id": 20, "titulo": "P20 API", "preco": 20, "imagem": "img20.png"}''', ex=3600)

@pytest.mark.asyncio
async def test_remover_favorito(service, mock_dependencies):
    """Testa a remoção de um favorito."""
    mock_repo, _, _ = mock_dependencies
    mock_repo.delete.return_value = True

    result = service.remover_favorito(cliente_id=1, produto_id=1)

    mock_repo.delete.assert_called_once_with(1, 1)
    assert result is True
