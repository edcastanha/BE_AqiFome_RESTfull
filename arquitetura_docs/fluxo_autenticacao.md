# Diagrama de Sequência: Autenticação de Usuário (Login)

Este diagrama ilustra o fluxo de autenticação de um usuário para obter um token de acesso JWT.

```mermaid
sequenceDiagram
    participant User
    participant API as FastAPI
    participant ClienteService
    participant Security
    participant Database

    User->>+API: POST /auth/login (com email e senha)
    API->>+ClienteService: authenticate_user(email, password)
    ClienteService->>+Database: find_by_email(email)
    alt Usuário não encontrado
        Database-->>-ClienteService: Retorna None
        ClienteService-->>-API: Lança exceção (HTTP 404)
        API-->>-User: 404 Not Found
    else Usuário encontrado
        Database-->>-ClienteService: Retorna dados do Cliente
        ClienteService->>+Security: verify_password(plain_password, hashed_password)
        alt Senha incorreta
            Security-->>-ClienteService: Retorna False
            ClienteService-->>-API: Lança exceção (HTTP 401)
            API-->>-User: 401 Unauthorized
        else Senha correta
            Security-->>-ClienteService: Retorna True
            ClienteService->>+Security: create_access_token(data={ "sub": user.email })
            Security-->>-ClienteService: Retorna JWT Token
            ClienteService-->>-API: Retorna o token
            API-->>-User: 200 OK (com access_token)
        end
    end
```
