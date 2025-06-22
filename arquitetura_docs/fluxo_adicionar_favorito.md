# Diagrama de Sequência: Adicionar Produto Favorito

Este diagrama ilustra o fluxo de adicionar um novo produto à lista de favoritos de um cliente.

```mermaid
sequenceDiagram
    participant User
    participant API as FastAPI
    participant FavoritoService
    participant ProdutoRepository
    participant FakeStoreAPI as "Fake Store API"
    participant Database

    User->>+API: POST /clientes/1/favoritos (com [1, 2, 3])
    API->>+FavoritoService: adicionar_favoritos(cliente_id=1, produto_ids=[1, 2, 3])

    loop Para cada produto_id na lista
        FavoritoService->>FavoritoService: O produto já é favorito? (Não)
        FavoritoService->>+ProdutoRepository: get_by_id(produto_id)
        alt Produto não está no cache (DB local)
            ProdutoRepository-->>-FavoritoService: Retorna None
            FavoritoService->>+FakeStoreAPI: GET /products/{produto_id}
            FakeStoreAPI-->>-FavoritoService: Retorna dados do Produto (JSON)
            Note over FavoritoService: Mapeia JSON para o modelo Produto (com a correção)
            FavoritoService->>+ProdutoRepository: create(produto)
            ProdutoRepository-->>-FavoritoService: Retorna Produto salvo
        else Produto já está no cache
            ProdutoRepository-->>-FavoritoService: Retorna Produto do DB
        end
    end

    Note over FavoritoService: Agrupa todos os favoritos para criar
    FavoritoService->>+Database: Insere todos os favoritos em lote (create_many)
    Database-->>-FavoritoService: Confirma a criação

    Note over FavoritoService: Monta a resposta com os detalhes dos produtos
    FavoritoService-->>-API: Retorna a lista de FavoritosResponse
    API-->>-User: 200 OK (com a lista de favoritos criados)
```
