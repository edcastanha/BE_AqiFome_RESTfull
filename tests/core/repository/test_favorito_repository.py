import pytest
from core.repository.favorito_repository import FavoritoRepository
from core.domain.favorito import Favorito
from sqlalchemy.orm import Session
from unittest.mock import MagicMock

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def repo(mock_db):
    return FavoritoRepository(db=mock_db)

def test_create_favorito(db_session):
    """Testa a criação de um novo favorito no repositório."""
    repo = FavoritoRepository(db_session)
    novo_favorito = Favorito(cliente_id=cliente.id, produto_id=produto.id)

    favorito_criado = repo.create(novo_favorito)

    assert favorito_criado.id is not None
    assert favorito_criado.cliente_id == cliente.id
    assert favorito_criado.produto_id == produto.id

def test_list_by_cliente(repo, mock_db):
    favoritos_orm = [MagicMock(), MagicMock()]
    mock_db.query.return_value.filter.return_value.all.return_value = favoritos_orm
    Favorito.from_orm = MagicMock(side_effect=[Favorito(id=1, cliente_id=1, produto_id=1, titulo="A", imagem="", preco=1, review=""), Favorito(id=2, cliente_id=1, produto_id=2, titulo="B", imagem="", preco=2, review="")])
    result = repo.list_by_cliente(1)
    assert len(result) == 2
    assert result[0].titulo == "A"
    assert result[1].titulo == "B"

def test_delete_favorito_found(repo, mock_db):
    db_fav = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = db_fav
    mock_db.delete.return_value = None
    mock_db.commit.return_value = None
    result = repo.delete(1, 2)
    assert result is True

def test_delete_favorito_not_found(repo, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = repo.delete(1, 2)
    assert result is False

def test_exists_true(repo, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = MagicMock()
    result = repo.exists(1, 2)
    assert result is True

def test_exists_false(repo, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = repo.exists(1, 2)
    assert result is False
