import pytest
from pydantic import ValidationError

from core.domain.cliente import (
    Cliente,
    ClienteBase,
    ClienteCreate,
    ClienteInDB,
    TipoCliente,
)


def test_cliente_creation_with_defaults():
    """Testa a criação de um Cliente com o tipo padrão."""
    cliente = ClienteBase(email="test@example.com", senha="password")
    assert cliente.tipo == TipoCliente.NORMAL


def test_cliente_creation_as_admin():
    """Testa a criação de um Cliente como ADMIN."""
    cliente = ClienteBase(
        email="admin@example.com", senha="admin_password", tipo=TipoCliente.ADMIN
    )
    assert cliente.tipo == TipoCliente.ADMIN


def test_cliente_create_model():
    """Testa o modelo ClienteCreate."""
    cliente_data = {
        "nome": "Ed Lourenco",
        "email": "ed.ourenco@example.com",
        "senha": "a_safe_password",
    }
    cliente = ClienteCreate(**cliente_data)
    assert cliente.nome == "Ed Lourenco"
    assert cliente.email == "ed.ourenco@example.com"


def test_cliente_model_from_orm():
    """Testa a criação do modelo Cliente a partir de um objeto ORM (simulado)."""

    class OrmCliente:
        id = 1
        nome = "Jane Doe"
        email = "jane.doe@example.com"
        senha = "hashed_password"
        tipo = TipoCliente.NORMAL

    cliente = Cliente.model_validate(OrmCliente())
    assert cliente.id == 1
    assert cliente.nome == "Jane Doe"
    assert cliente.email == "jane.doe@example.com"
    assert cliente.tipo == TipoCliente.NORMAL


def test_cliente_indb_model():
    """Testa o modelo ClienteInDB, que deve incluir a senha."""
    cliente_data = {
        "id": 1,
        "nome": "DB User",
        "email": "db@example.com",
        "senha": "a_real_hashed_password",
        "tipo": TipoCliente.ADMIN,
    }
    cliente = ClienteInDB(**cliente_data)
    assert cliente.senha == "a_real_hashed_password"


def test_cliente_model_invalid_email():
    """Testa que o Pydantic levanta um erro para um e-mail inválido."""
    with pytest.raises(ValidationError):
        ClienteCreate(nome="Invalid", email="not-an-email", senha="password")
