from src.core.domain.favorito import Favorito
from src.core.repository.favorito_repository import FavoritoRepository
from typing import List

class FavoritoService:
    def __init__(self, repository: FavoritoRepository):
        self.repository = repository

    def adicionar_favorito(self, favorito: Favorito) -> Favorito:
        if self.repository.exists(favorito.cliente_id, favorito.produto_id):
            raise ValueError("Produto já está nos favoritos do cliente")
        return self.repository.create(favorito)

    def listar_favoritos(self, cliente_id: int) -> List[Favorito]:
        return self.repository.list_by_cliente(cliente_id)

    def remover_favorito(self, cliente_id: int, produto_id: int) -> bool:
        return self.repository.delete(cliente_id, produto_id)
