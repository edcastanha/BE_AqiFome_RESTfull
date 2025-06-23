from unittest.mock import MagicMock, patch
import pytest
from core.domain.cliente import ClienteCreate, ClienteUpdate, TipoCliente
from core.service.cliente_service import ClienteService
from pydantic import SecretStr


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


@patch('core.service.cliente_service.get_password_hash')
def test_atualizar_cliente_com_senha(mock_get_password_hash):
    """
    Testa a atualização de um cliente, incluindo a senha,
    verificando se a senha é hasheada corretamente.
    """
    # Configuração
    mock_repo = MagicMock()
    # O serviço primeiro busca o cliente para garantir que ele existe.
    mock_repo.get_by_id.return_value = MagicMock()
    mock_get_password_hash.return_value = "nova_senha_hasheada"
    service = ClienteService(mock_repo)
    cliente_id = 1
    update_data = ClienteUpdate(
        nome="Novo Nome",
        senha=SecretStr("nova_senha_123")
    )

    # Ação
    service.atualizar_cliente(cliente_id, update_data)

    # Verificação
    mock_repo.get_by_id.assert_called_once_with(cliente_id)
    mock_get_password_hash.assert_called_once_with("nova_senha_123")
    mock_repo.update.assert_called_once()

    # Verifica se o repositório foi chamado com os dados corretos
    args, _ = mock_repo.update.call_args
    assert args[0] == cliente_id
    # O segundo argumento é o objeto Pydantic ClienteUpdate, não um dicionário
    update_payload_obj = args[1]
    assert isinstance(update_payload_obj, ClienteUpdate)
    assert update_payload_obj.nome == "Novo Nome"
    # O serviço deve ter trocado a senha original pela hasheada
    assert update_payload_obj.senha.get_secret_value() == "nova_senha_hasheada"


def test_atualizar_cliente_sem_senha():
    """
    Testa a atualização de um cliente sem modificar a senha.
    """
    # Configuração
    mock_repo = MagicMock()
    # O serviço primeiro busca o cliente para garantir que ele existe.
    mock_repo.get_by_id.return_value = MagicMock()
    service = ClienteService(mock_repo)
    cliente_id = 1
    update_data = ClienteUpdate(nome="Outro Nome")

    # Ação
    service.atualizar_cliente(cliente_id, update_data)

    # Verificação
    mock_repo.get_by_id.assert_called_once_with(cliente_id)
    mock_repo.update.assert_called_once()
    args, _ = mock_repo.update.call_args
    assert args[0] == cliente_id
    # O segundo argumento é o objeto Pydantic ClienteUpdate
    update_payload_obj = args[1]
    assert isinstance(update_payload_obj, ClienteUpdate)
    assert update_payload_obj.nome == "Outro Nome"
    # A senha não foi fornecida, então deve ser None no objeto de atualização
    assert update_payload_obj.senha is None
