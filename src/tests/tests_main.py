from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensagem": "API RESTful está funcionando!"}

def test_read_produtos():
    response = client.get("/itens")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Verifica se a resposta é uma lista
    assert len(response.json()) > 0  # Verifica se a lista não está vazia
    for produto in response.json():
        assert "id" in produto
        assert "titulo" in produto
        assert "preco" in produto
        assert "descricao" in produto
        assert "categoria" in produto
        assert "imagem" in produto
        assert "rating" in produto  # Verifica se a chave 'rating' está presente

