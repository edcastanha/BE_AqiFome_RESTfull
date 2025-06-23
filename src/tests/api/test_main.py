import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api.main import app

client = TestClient(app)

# --- Testes básicos ---
def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "API Online"}

def test_login_invalido():
    resp = client.post("/token", data={"username": "fake", "password": "fake"})
    assert resp.status_code == 401

# --- Testes de fluxo completo ---
@patch("core.service.favorito_service.FakeStoreProduct")
@patch("core.service.favorito_service.RedisConfig")
def test_crud_cliente_e_favoritos(mock_redis_config, mock_fake_store):
    # Mock Redis
    mock_redis = MagicMock()
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    mock_redis_config.return_value.get_client.return_value = mock_redis
    mock_redis_config.return_value.get_expires.return_value = 3600

    # Mock FakeStoreProduct
    mock_fake_store.return_value.get_product.return_value = {
        "id": 1, "titulo": "Produto Teste", "imagem": "img.png", "preco": 10.0
    }
    mock_fake_store.return_value.get_product_sync.return_value = {
        "id": 1, "titulo": "Produto Teste", "imagem": "img.png", "preco": 10.0
    }

    # Criar cliente
    cliente_data = {
        "nome": "Test User",
        "email": "testuser_crud@example.com",  # E-mail único para este teste
        "senha": "senha123",
        "tipo": 0  # Tipo USER normal
    }

    # 1. Criar o cliente primeiro (sem token, pois é um endpoint público ou de admin)
    # Para este teste, vamos assumir que a criação de cliente não exige token.
    # Se exigisse, precisaríamos de um token de admin.
    resp = client.post("/clientes", json=cliente_data)
    assert resp.status_code == 201, f"Erro ao criar cliente: {resp.text}"
    cliente = resp.json()
    cliente_id = cliente["id"]


    # 2. Login com o novo cliente
    resp = client.post("/token", data={"username": cliente_data["email"], "password": cliente_data["senha"]})
    assert resp.status_code == 200, f"Erro no login: {resp.text}"

    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Listar clientes (deve falhar, pois o usuário não é admin)
    resp = client.get("/clientes", headers=headers)
    assert resp.status_code == 403

    # 4. Buscar o próprio cliente (deve funcionar)
    resp = client.get(f"/clientes/{cliente_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == cliente_data["email"]

    # 5. Atualizar o próprio cliente
    update_data = {"nome": "Novo Nome"}
    resp = client.put(f"/clientes/{cliente_id}", json=update_data, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["nome"] == "Novo Nome"

    # 6. Adicionar favorito
    fav_data = {"produto_ids": [1]}
    resp = client.post(f"/clientes/{cliente_id}/favoritos", json=fav_data, headers=headers)
    assert resp.status_code == 201
    favoritos = resp.json()
    assert isinstance(favoritos, list)
    assert favoritos[0]["produto"]["id"] == 1

    # Listar favoritos
    resp = client.get(f"/clientes/{cliente_id}/favoritos", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    # Remover favorito
    resp = client.delete(f"/clientes/{cliente_id}/favoritos/1", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["ok"] is True

    # Deletar cliente
    resp = client.delete(f"/clientes/{cliente_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["ok"] is True

# --- Testes de erro e permissão ---
def test_operacoes_sem_token():
    # Tenta acessar endpoints protegidos sem token
    resp = client.get("/clientes")
    assert resp.status_code in (401, 403)
    resp = client.get("/clientes/1/favoritos")
    assert resp.status_code in (401, 403)
    resp = client.post("/clientes/1/favoritos", json={"produto_ids": [1]})
    assert resp.status_code in (401, 403)