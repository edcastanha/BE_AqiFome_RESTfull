from core.domain.favorito import Favorito

def test_favorito_model():
    favorito = Favorito(id=1, cliente_id=1, produto_id=123, titulo="Produto Exemplo", imagem="url", preco=10.0, review="Ótimo!")
    assert favorito.id == 1
    assert favorito.cliente_id == 1
    assert favorito.produto_id == 123
    assert favorito.titulo == "Produto Exemplo"
    assert favorito.imagem == "url"
    assert favorito.preco == 10.0
    assert favorito.review == "Ótimo!"
    # Testa representação
    assert str(favorito) == str(favorito)
