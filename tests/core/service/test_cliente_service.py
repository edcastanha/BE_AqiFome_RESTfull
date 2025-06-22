from unittest.mock import MagicMock, patch
import pytest
from core.domain.cliente import ClienteCreate, TipoCliente
from core.service.cliente_service import ClienteService


@patch('core.service.cliente_service.get_password_hash')
def test_criar_cliente(mock_get_password_hash):
    """
    Testa a criação de um cliente, verificando o hashing da senha
    e a chamada ao repositório.
    """
    # Configuração
    mock_repo = MagicMock()
    mock_repo.get_by_email.return_value = None  # Corrige: simula e-mail não cadastrado
    mock_get_password_hash.return_value = "senha_hasheada_super_segura"
    service = ClienteService(mock_repo)
    cliente_data = ClienteCreate(nome="Teste", email="teste@exemplo.com", senha="senha123", tipo=TipoCliente.USER)

    # Ação
    service.criar_cliente(cliente_data)

    # Verificação
    mock_repo.get_by_email.assert_called_once_with("teste@exemplo.com")
    mock_get_password_hash.assert_called_once_with("senha123")
    mock_repo.create.assert_called_once()

    # Verifica se o repositório foi chamado com a senha hasheada
    args, _ = mock_repo.create.call_args
    assert args[0].nome == cliente_data.nome
    assert args[0].email == cliente_data.email
    assert args[0].tipo == cliente_data.tipo
    assert args[0].senha == "senha_hasheada_super_segura"


def test_criar_cliente_com_email_existente():
    """Testa a falha ao tentar criar um cliente com e-mail que já existe."""
    mock_repo = MagicMock()
    mock_repo.get_by_email.return_value = True  # Simula que o e-mail já existe
    service = ClienteService(mock_repo)
    cliente_data = ClienteCreate(nome="Teste", email="existente@exemplo.com", senha="senha123", tipo=TipoCliente.USER)

    with pytest.raises(ValueError, match="E-mail já cadastrado"):
        service.criar_cliente(cliente_data)
