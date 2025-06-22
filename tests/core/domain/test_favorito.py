import pytest
from pydantic import ValidationError

from core.domain.favorito import (
    Favorito,
    FavoritoBase,
    FavoritoCreate,
    FavoritoCreateRequest,
    FavoritoResponse,
)
from core.domain.produto import Produto


def test_favorito_create_request():
    """Testa a criação de uma requisição para adicionar favoritos."""
    request_data = {"produto_ids": [1, 5, 10]}
    request_model = FavoritoCreateRequest(**request_data)
    assert request_model.produto_ids == [1, 5, 10]


def test_favorito_base_model():
    """Testa o modelo base de Favorito."""
    favorito = FavoritoBase(cliente_id=1, produto_id=2)
    assert favorito.cliente_id == 1
    assert favorito.produto_id == 2


def test_favorito_create_model():
    """Testa o DTO interno de criação de Favorito."""
    favorito = FavoritoCreate(cliente_id=1, produto_id=3)
    assert favorito.cliente_id == 1
    assert favorito.produto_id == 3


def test_favorito_domain_model():
    """Testa o modelo de domínio Favorito, que pode conter um objeto Produto."""
    produto = Produto(
        id=1, titulo="Teste", preco=10.0, imagem="https://example.com/image.jpg"
    )
    favorito = Favorito(id=10, cliente_id=1, produto_id=1, produto=produto)
    assert favorito.id == 10
    assert favorito.produto is not None
    assert favorito.produto.titulo == "Teste"


def test_favorito_response_model():
    """Testa o modelo de resposta da API para um favorito."""
    produto = Produto(
        id=1, titulo="Teste", preco=10.0, imagem="https://example.com/image.jpg"
    )
    response = FavoritoResponse(id=20, cliente_id=1, produto=produto)
    assert response.id == 20
    assert response.cliente_id == 1
    assert response.produto.id == 1


def test_favorito_response_model_validation():
    """Testa que o modelo de resposta exige um produto."""
    with pytest.raises(ValidationError):
        FavoritoResponse(id=1, cliente_id=1, produto=None)
