# API RESTfull - AQIFome

Requisitos de execucão do projeto localmente

- Docker
- Docker Compose

[Guia de Execução do Ambiente Local (Desenvolvimento)](INSTALL.md)

**Após a inicialização, a aplicação estará disponível no endereço:**

   - [ReDoc](http://localhost:8000/redoc) para documentação da API

   - [Swagger UI](http://localhost:8000/docs) para documentação da API

========================
## Contexto

O aiqfome está expandindo seus canais de integração e precisa de uma API robusta para gerenciar os "produtos favoritos" de usuários na plataforma.
Essa funcionalidade será usada por apps e interfaces web para armazenar e consultar produtos marcados como favoritos pelos clientes. A API terá alto volume de uso e integrará com outros sistemas internos e externos.


### 🔧 Desafio:
Desenvolva uma API RESTful que permita:

**Clientes**
Criar, visualizar, editar e remover clientes(ADMIN).
Dados obrigatórios: nome e e-mail.
Um mesmo e-mail não pode se repetir no cadastro.

**Favoritos**
Um cliente deve ter uma lista de produtos favoritos.
Os produtos devem ser validados via API externa (link fornecido abaixo).
Um produto não pode ser duplicado na lista de um cliente.
Produtos favoritos devem exibir: ID, título, imagem, preço e review (se houver).

**Requisitos de Integração**
 Sugerimos o uso de uma API genérica para buscar produtos. Porém, para facilitar a execução e deixar tudo mais direto ao ponto,recomendamos o uso da seguinte API pública:

🔗 https://fakestoreapi.com/docs

Você pode utilizar especificamente estes dois endpoints:

Listar todos os produtos:
🔗 GET https://fakestoreapi.com/products

Buscar produto por ID:
🔗 GET https://fakestoreapi.com/products/{id}



### ⚖️ Regras Gerais
A API deve ser pública, mas conter autenticação e autorização.
Evite duplicidade de dados.
Estruture bem o código, seguindo boas práticas REST.
Pense em performance e escalabilidade(nesta abordagem optei por um design orientado a replicar os dados de Produto ).
Documente sua API (Swagger padrao do FASTAPI).
Não use IA ou cópias. Será passível de eliminação.

### 💡 Requisitos Técnicos
Você pode escolher uma das seguintes linguagens:

* Python
* Framework FASTAPI  


### 🗄️ Banco de Dados sugerido:
PostgreSQL

### 📊 O que esperamos:
**Critério**	                            **Peso**
* Correção e funcionamento da API	        🔥🔥🔥🔥
* Modelagem de dados (clientes/produtos)	🔥🔥🔥
* Validação e controle de dados	            🔥🔥🔥
* Documentação ou instrução de uso	        🔥🔥
* Segurança básica (auth, validação)	    🔥🔥