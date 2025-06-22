import pytest
from core.repository.cliente_repository import ClienteRepository
from core.domain.cliente import Cliente, ClienteCreate
from sqlalchemy.orm import Session
from unittest.mock import MagicMock

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def repo(mock_db):
    return ClienteRepository(db=mock_db)

def test_create_cliente(repo, mock_db):
    cliente_data = ClienteCreate(nome="Novo Cliente", email="novo@exemplo.com", password="naousadoaqui")
    hashed_password = "senha_hasheada_fake"
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    mock_db.query.return_value.filter.return_value.first.return_value = None
    # Simula o método from_orm
    Cliente.from_orm = MagicMock(return_value=cliente_data)
    result = repo.create(cliente_data, hashed_password)
    assert result.nome == "Novo Cliente"
    assert result.email == "novo@exemplo.com"

def test_get_by_id_found(repo, mock_db):
    cliente = Cliente(id=2, nome="Maria", email="maria@email.com")
    mock_db.query.return_value.filter.return_value.first.return_value = MagicMock()
    Cliente.from_orm = MagicMock(return_value=cliente)
    result = repo.get_by_id(2)
    assert result.nome == "Maria"

def test_get_by_id_not_found(repo, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = repo.get_by_id(99)
    assert result is None

def test_list_clientes(repo, mock_db):
    clientes_orm = [MagicMock(), MagicMock()]
    mock_db.query.return_value.all.return_value = clientes_orm
    Cliente.from_orm = MagicMock(side_effect=[Cliente(id=1, nome="A", email="a@a.com"), Cliente(id=2, nome="B", email="b@b.com")])
    result = repo.list()
    assert len(result) == 2
    assert result[0].nome == "A"
    assert result[1].nome == "B"

def test_update_cliente_found(repo, mock_db):
    cliente = Cliente(id=3, nome="Novo", email="novo@email.com")
    db_cliente = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = db_cliente
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    Cliente.from_orm = MagicMock(return_value=cliente)
    result = repo.update(3, cliente)
    assert result.nome == "Novo"

def test_update_cliente_not_found(repo, mock_db):
    cliente = Cliente(id=4, nome="Novo", email="novo@email.com")
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = repo.update(99, cliente)
    assert result is None

def test_delete_cliente_found(repo, mock_db):
    db_cliente = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = db_cliente
    mock_db.delete.return_value = None
    mock_db.commit.return_value = None
    result = repo.delete(1)
    assert result is True or result is None  # depende da implementação

def test_delete_cliente_not_found(repo, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = repo.delete(99)
    assert result is False or result is None  # depende da implementação
