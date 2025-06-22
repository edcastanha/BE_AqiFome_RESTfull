from unittest.mock import MagicMock, AsyncMock, call
import pytest
from core.domain.favorito import Favorito, FavoritoResponse, FavoritoCreate
from core.domain.produto import Produto
from core.service.favorito_service import FavoritoService
from pydantic import HttpUrl, parse_obj_as

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_dependencies():
    """Fixture para criar mocks das dependências do FavoritoService."""
    mock_repo = MagicMock()
    mock_produto_repo = MagicMock()
    mock_client = AsyncMock()
    return mock_repo, mock_produto_repo, mock_client


async def test_adicionar_favoritos_com_sucesso(mock_dependencies):
    """Testa adicionar uma lista de favoritos com sucesso (cache miss e hit)."""
    mock_repo, mock_produto_repo, mock_client = mock_dependencies
    service = FavoritoService(mock_repo, mock_produto_repo, mock_client)

    # --- Configuração dos Mocks ---
    # Produto 1 (cache hit), Produto 2 (cache miss), Produto 3 (já favorito)
    mock_repo.exists.side_effect = [False, False, True] # P1, P2, P3
    mock_produto_repo.get_by_id.side_effect = [
        Produto(id=1, titulo="P1 Cache", preco=10, imagem="http://img1.com/img01.png"), # P1
        None, # P2 (não está no cache)
    ]
    mock_client.get_product.return_value = {
        "id": 2, "title": "P2 API", "price": 20, "image": "http://img2.com/img02.png",
        "description": "D", "category": "C", "rating": {"rate": 4}
    }
    # O serviço vai chamar listar_favoritos no final
    service.listar_favoritos = MagicMock(return_value=[
        FavoritoResponse(id=1, cliente_id=1, produto=Produto(id=1, titulo="P1", preco=10, imagem=HttpUrl('http://img1.com/img01.png', scheme='http', host='img1.com', tld='com', host_type='domain'))),
        FavoritoResponse(id=2, cliente_id=1, produto=Produto(id=2, titulo="P2", preco=20, imagem="http://img2.com/img02.png")),
    ])

    # --- Execução ---
    resultado = await service.adicionar_favoritos(cliente_id=1, produto_ids=[1, 2, 3])

    # --- Verificações ---
    # 1. Verificação de existência
    assert mock_repo.exists.call_count == 3
    mock_repo.exists.assert_has_calls([call(1, 1), call(1, 2), call(1, 3)])

    # 2. Acesso ao repositório de produtos
    mock_produto_repo.get_by_id.assert_has_calls([call(1), call(2)])

    # 3. Acesso à API externa (apenas para P2)
    mock_client.get_product.assert_called_once_with(2)

    # 4. Criação do produto P2 no cache
    mock_produto_repo.create.assert_called_once()

    # 5. Criação dos favoritos em lote (apenas P1 e P2)
    mock_repo.create_many.assert_called_once()
    args, _ = mock_repo.create_many.call_args
    assert len(args[0]) == 2
    assert args[0][0].produto_id == 1
    assert args[0][1].produto_id == 2

    # 6. Retorno final
    assert len(resultado) == 2
    service.listar_favoritos.assert_called_once_with(1)


async def test_adicionar_favoritos_ignora_nao_encontrados(mock_dependencies):
    """Testa que o serviço ignora produtos não encontrados na API externa."""
    mock_repo, mock_produto_repo, mock_client = mock_dependencies
    service = FavoritoService(mock_repo, mock_produto_repo, mock_client)

    # --- Configuração dos Mocks ---
    mock_repo.exists.return_value = False
    mock_produto_repo.get_by_id.return_value = None
    mock_client.get_product.return_value = None # API não encontra o produto 999
    service.listar_favoritos = MagicMock(return_value=[])

    # --- Execução ---
    await service.adicionar_favoritos(cliente_id=1, produto_ids=[999])

    # --- Verificações ---
    mock_client.get_product.assert_called_once_with(999)
    mock_repo.create_many.assert_not_called() # Não deve criar nenhum favorito
    service.listar_favoritos.assert_called_once_with(1)


async def test_adicionar_favoritos_sem_novos_favoritos(mock_dependencies):
    """Testa o fluxo onde nenhum novo favorito é adicionado (todos já existem)."""
    mock_repo, mock_produto_repo, mock_client = mock_dependencies
    service = FavoritoService(mock_repo, mock_produto_repo, mock_client)

    # --- Configuração dos Mocks ---
    mock_repo.exists.return_value = True # Todos os produtos já são favoritos
    service.listar_favoritos = MagicMock(return_value=[
        FavoritoResponse(id=1, cliente_id=1, produto=Produto(id=1, titulo="P1", preco=10, imagem=parse_obj_as(HttpUrl, "http://img1.com/img01.png")))
    ])

    # --- Execução --- 
    resultado = await service.adicionar_favoritos(cliente_id=1, produto_ids=[1])

    # --- Verificações ---
    mock_repo.exists.assert_called_once_with(1, 1)
    mock_produto_repo.get_by_id.assert_not_called()
    mock_repo.create_many.assert_not_called()
    service.listar_favoritos.assert_called_once_with(1)
    assert len(resultado) == 1 # Deve retornar a lista existente


async def test_remover_favorito_com_sucesso(mock_dependencies):
    """Testa a remoção de um favorito com sucesso."""
    mock_repo, mock_produto_repo, mock_client = mock_dependencies
    service = FavoritoService(mock_repo, mock_produto_repo, mock_client)

    # Configuração
    mock_repo.delete.return_value = True

    # Execução
    resultado = service.remover_favorito(cliente_id=1, produto_id=1)

    # Verificação
    mock_repo.delete.assert_called_once_with(1, 1)
    assert resultado is True


async def test_remover_favorito_nao_encontrado(mock_dependencies):
    """Testa a remoção de um favorito que não existe."""
    mock_repo, mock_produto_repo, mock_client = mock_dependencies
    service = FavoritoService(mock_repo, mock_produto_repo, mock_client)

    # Configuração
    mock_repo.delete.return_value = False

    # Execução
    resultado = service.remover_favorito(cliente_id=1, produto_id=999)

    # Verificação
    mock_repo.delete.assert_called_once_with(1, 999)
    assert resultado is False
