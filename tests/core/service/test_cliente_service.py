import pytest
from src.core.domain.cliente import Cliente
from src.core.repository.cliente_repository import ClienteRepository
from src.core.service.cliente_service import ClienteService
from typing import List

class FakeClienteRepository(ClienteRepository):
    def __init__(self):
        self._clientes: List[Cliente] = []
    def get_by_email(self, email):
        for c in self._clientes:
            if c.email == email:
                return c
        return None
    def create(self, cliente):
        self._clientes.append(cliente)
        return cliente
    def list(self):
        return self._clientes

def test_criar_cliente():
    repo = FakeClienteRepository()
    service = ClienteService(repo)
    cliente = Cliente(id=None, nome="Maria", email="maria@email.com")
    criado = service.criar_cliente(cliente)
    assert criado.nome == "Maria"
    assert criado.email == "maria@email.com"
    # Testa duplicidade
    with pytest.raises(ValueError):
        service.criar_cliente(cliente)
