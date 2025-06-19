from src.core.domain.favorito import Favorito
from src.core.service.favorito_service import FavoritoService
from src.core.repository.favorito_repository import FavoritoRepository
import pytest
from typing import List

class FakeFavoritoRepository(FavoritoRepository):
    def __init__(self):
        self._favoritos: List[Favorito] = []
    def exists(self, cliente_id, produto_id):
        return any(f.cliente_id == cliente_id and f.produto_id == produto_id for f in self._favoritos)
    def create(self, favorito):
        self._favoritos.append(favorito)
        return favorito
    def list_by_cliente(self, cliente_id):
        return [f for f in self._favoritos if f.cliente_id == cliente_id]
    def delete(self, cliente_id, produto_id):
        for f in self._favoritos:
            if f.cliente_id == cliente_id and f.produto_id == produto_id:
                self._favoritos.remove(f)
                return True
        return False

def test_adicionar_favorito():
    repo = FakeFavoritoRepository()
    service = FavoritoService(repo)
    fav = Favorito(id=None, cliente_id=1, produto_id=10, titulo="Produto", imagem="img", preco=1.0, review=None)
    criado = service.adicionar_favorito(fav)
    assert criado.produto_id == 10
    # Testa duplicidade
    with pytest.raises(ValueError):
        service.adicionar_favorito(fav)

def test_listar_remover_favorito():
    repo = FakeFavoritoRepository()
    service = FavoritoService(repo)
    fav = Favorito(id=None, cliente_id=1, produto_id=10, titulo="Produto", imagem="img", preco=1.0, review=None)
    service.adicionar_favorito(fav)
    assert len(service.listar_favoritos(1)) == 1
    assert service.remover_favorito(1, 10)
    assert len(service.listar_favoritos(1)) == 0
