import pytest
from unittest.mock import MagicMock
from pydantic import ValidationError
from sqlalchemy.orm import Session

from core.domain.cliente import Cliente, ClienteCreate, TipoCliente
from core.repository.cliente_repository import ClienteRepository
from core.repository.cliente_orm import ClienteORM


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def repo(mock_db):
    return ClienteRepository(mock_db)


def test_create_cliente(repo, mock_db):
    cliente_data = ClienteCreate(nome="Novo Cliente", email="novo@exemplo.com", senha="password", tipo=TipoCliente.USER)
    # O repo irá criar um ClienteORM internamente
    # Precisamos mockar o que acontece depois do add, commit e refresh
    def refresh_side_effect(orm_object):
        orm_object.id = 1
        orm_object.nome = cliente_data.nome
        orm_object.email = cliente_data.email
        orm_object.senha = "password"  # A senha que foi passada
        orm_object.tipo = cliente_data.tipo

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = refresh_side_effect

    # A senha com hash é tratada no service, o repo recebe o objeto com a senha já definida
    created_cliente = repo.create(cliente_data)

    assert created_cliente.id == 1
    assert created_cliente.nome == cliente_data.nome
    assert created_cliente.senha == "password"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_get_by_id_found(repo, mock_db):
    cliente_orm = ClienteORM(
        id=2,
        nome="Maria",
        email="maria@email.com",
        tipo=TipoCliente.USER,
        senha="hashed_password",  # Adicionado campo senha
    )
    mock_db.query.return_value.filter.return_value.first.return_value = cliente_orm
    cliente = repo.get_by_id(2)
    assert cliente is not None
    assert cliente.id == 2
    assert cliente.nome == "Maria"
    assert cliente.senha is not None


def test_get_by_id_not_found(repo, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    cliente = repo.get_by_id(999)
    assert cliente is None


def test_list_clientes(repo, mock_db):
    clientes_orm = [
        ClienteORM(
            id=1, nome="A", email="a@a.com", tipo=TipoCliente.USER, senha="pass1"
        ),
        ClienteORM(
            id=2, nome="B", email="b@b.com", tipo=TipoCliente.USER, senha="pass2"
        ),
    ]
    mock_db.query.return_value.all.return_value = clientes_orm
    clientes = repo.list()
    assert len(clientes) == 2
    assert clientes[0].nome == "A"
    assert clientes[1].senha == "pass2"


def test_update_cliente_found(repo, mock_db):
    cliente_orm = ClienteORM(
        id=3,
        nome="Antigo",
        email="antigo@email.com",
        tipo=TipoCliente.USER,
        senha="antiga_senha",
    )
    mock_db.query.return_value.filter.return_value.first.return_value = cliente_orm
    cliente_update_data = Cliente(
        id=3,
        nome="Novo Nome",
        email="novo@email.com",
        senha="nova_senha",
        tipo=TipoCliente.ADMIN,
    )

    updated_cliente = repo.update(3, cliente_update_data)

    assert updated_cliente is not None
    assert updated_cliente.nome == "Novo Nome"
    assert updated_cliente.tipo == TipoCliente.ADMIN
    mock_db.commit.assert_called_once()


def test_update_cliente_not_found(repo, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    cliente_update_data = Cliente(
        id=4, nome="Nao Existe", email="nao@existe.com", senha="password", tipo=TipoCliente.USER
    )
    updated_cliente = repo.update(4, cliente_update_data)
    assert updated_cliente is None


def test_delete_cliente_found(repo, mock_db):
    cliente_orm = ClienteORM(id=5, nome="Para Deletar", email="del@del.com")
    mock_db.query.return_value.filter.return_value.first.return_value = cliente_orm
    deleted = repo.delete(5)
    assert deleted is True
    mock_db.delete.assert_called_once_with(cliente_orm)
    mock_db.commit.assert_called_once()


def test_delete_cliente_not_found(repo, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    deleted = repo.delete(999)
    assert deleted is False
