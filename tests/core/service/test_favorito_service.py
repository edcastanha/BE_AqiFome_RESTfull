from unittest.mock import MagicMock, AsyncMock
import pytest
from core.domain.favorito import Favorito
from core.domain.produto import Produto
from core.service.favorito_service import FavoritoService

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_dependencies():
    """Fixture para criar mocks das dependências do FavoritoService."""
    mock_repo = MagicMock()
    mock_produto_repo = MagicMock()
    mock_client = AsyncMock()
    return mock_repo, mock_produto_repo, mock_client


async def test_adicionar_favorito_cache_hit(mock_dependencies):
    """Testa adicionar favorito quando o produto JÁ EXISTE no cache local."""
    mock_repo, mock_produto_repo, mock_client = mock_dependencies
    service = FavoritoService(mock_repo, mock_produto_repo, mock_client)

    # Configuração dos mocks
    mock_repo.exists.return_value = False
    mock_produto_repo.get_by_id.return_value = Produto(id=101, titulo="Produto do Cache", preco=10.0, imagem="http://cache.com/img.png")

    favorito_data = Favorito(cliente_id=1, produto_id=101)
    await service.adicionar_favorito(favorito_data)

    # Verificações
    mock_repo.exists.assert_called_once_with(1, 101)
    mock_produto_repo.get_by_id.assert_called_once_with(101)
    mock_client.get_product.assert_not_called()  # API externa NÃO deve ser chamada
    mock_repo.create.assert_called_once_with(favorito_data)


async def test_adicionar_favorito_cache_miss(mock_dependencies):
    """Testa adicionar favorito quando o produto NÃO EXISTE no cache (cache miss)."""
    mock_repo, mock_produto_repo, mock_client = mock_dependencies
    service = FavoritoService(mock_repo, mock_produto_repo, mock_client)

    # Configuração dos mocks
    mock_repo.exists.return_value = False
    mock_produto_repo.get_by_id.return_value = None  # Produto não está no cache
    mock_client.get_product.return_value = {
        "id": 101, "title": "Produto da API", "price": 20.0, "image": "http://api.com/img.png",
        "description": "Desc", "category": "Cat", "rating": {"rate": 4.5}
    }

    favorito_data = Favorito(cliente_id=1, produto_id=101)
    await service.adicionar_favorito(favorito_data)

    # Verificações
    mock_produto_repo.get_by_id.assert_called_once_with(101)
    mock_client.get_product.assert_called_once_with(101)  # API externa DEVE ser chamada
    mock_produto_repo.create.assert_called_once()       # Repositório de produto DEVE ser chamado
    mock_repo.create.assert_called_once_with(favorito_data)


async def test_adicionar_favorito_produto_nao_encontrado(mock_dependencies):
    """Testa a falha ao tentar favoritar um produto que não existe em lugar nenhum."""
    mock_repo, mock_produto_repo, mock_client = mock_dependencies
    service = FavoritoService(mock_repo, mock_produto_repo, mock_client)

    # Configuração dos mocks
    mock_repo.exists.return_value = False
    mock_produto_repo.get_by_id.return_value = None
    mock_client.get_product.return_value = None  # API externa não encontrou

    favorito_data = Favorito(cliente_id=1, produto_id=999)

    with pytest.raises(ValueError, match="Produto não encontrado"):
        await service.adicionar_favorito(favorito_data)
