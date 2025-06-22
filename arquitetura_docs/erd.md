```mermaid
erDiagram
    CLIENTE ||--o{ FAVORITO : "possui"
    PRODUTO ||--o{ FAVORITO : "é"

    CLIENTE {
        int id (PK)
        string nome
        string email
        string password_hash
    }

    PRODUTO {
        int id (PK)
        string title
        float price
        string description
        string category
        string image
        float rate
        int count
    }

    FAVORITO {
        UUID id (PK)
        int cliente_id (FK)
        int produto_id (FK)
    }
```
