from src.core.domain.cliente import Cliente

def test_cliente_model():
    cliente = Cliente(id=1, nome="João", email="joao@email.com")
    assert cliente.id == 1
    assert cliente.nome == "João"
    assert cliente.email == "joao@email.com"
    # Testa representação
    assert str(cliente) == str(cliente)
