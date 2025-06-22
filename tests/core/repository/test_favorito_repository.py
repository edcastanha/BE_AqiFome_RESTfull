import pytest
from unittest.mock import MagicMock, call
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, call
from sqlalchemy.orm import Session
from core.repository.favorito_repository import FavoritoRepository
from core.domain.favorito import FavoritoCreate
from core.repository.favorito_orm import FavoritoORM

from core.domain.favorito import FavoritoCreate
from core.repository.favorito_orm import FavoritoORM


@pytest.fixture
def mock_db():
    """Fixture que cria um mock para a sessão do banco de dados."""
    """Fixture que cria um mock para a sessão do banco de dados."""
    return MagicMock(spec=Session)



@pytest.fixture
def repository(mock_db):
    """Fixture que cria uma instância do repositório com o DB mockado."""
    return FavoritoRepository(db=mock_db)


def test_create_many(repository, mock_db):
    """Testa a criação de múltiplos favoritos em lote."""
    favoritos_data = [
        FavoritoCreate(cliente_id=1, produto_id=10),
        FavoritoCreate(cliente_id=1, produto_id=20),
    ]

    # Usar uma lista mutável para o contador
    counter = [1]
    def refresh_side_effect(fav):
        fav.id = counter[0]
        fav.cliente_id = fav.cliente_id if hasattr(fav, 'cliente_id') else 1
        fav.produto_id = fav.produto_id if hasattr(fav, 'produto_id') else 10
        counter[0] += 1
    mock_db.refresh.side_effect = refresh_side_effect

    repository.create_many(favoritos_data)

    assert mock_db.add_all.call_count == 1
    mock_db.commit.assert_called_once()


def test_list_by_cliente(repository, mock_db):
    """Testa a listagem de favoritos por cliente."""
    mock_favoritos_orm = [
        FavoritoORM(id=1, cliente_id=1, produto_id=10),
        FavoritoORM(id=2, cliente_id=1, produto_id=20),
    ]
    mock_db.query.return_value.filter.return_value.all.return_value = mock_favoritos_orm

    result = repository.list_by_cliente(cliente_id=1)

    mock_db.query.assert_called_once_with(FavoritoORM)
    assert len(result) == 2



def test_delete_favorito_found(repository, mock_db):
    """Testa a remoção de um favorito que existe."""
    mock_favorito = FavoritoORM()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_favorito

    result = repository.delete(cliente_id=1, produto_id=1)

    mock_db.delete.assert_called_once_with(mock_favorito)
    mock_db.commit.assert_called_once()
    assert result is True


def test_delete_favorito_not_found(repository, mock_db):
    """Testa a tentativa de remoção de um favorito que não existe."""
    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = repository.delete(cliente_id=1, produto_id=99)

    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()
    assert result is False


def test_exists_true(repository, mock_db):
    """Testa a verificação de existência quando o favorito existe."""
    mock_db.query.return_value.filter.return_value.first.return_value = FavoritoORM()
    result = repository.exists(cliente_id=1, produto_id=1)
    assert result is True


def test_exists_false(repository, mock_db):
    """Testa a verificação de existência quando o favorito não existe."""
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = repository.exists(cliente_id=1, produto_id=99)
    assert result is False
