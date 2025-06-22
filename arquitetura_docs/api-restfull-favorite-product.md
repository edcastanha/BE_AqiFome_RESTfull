# Documento de requisitos do Projeto API Restful de Favoritos de Produtos do Cliente

Usarei Python com FastAPI para desenvolver uma API RESTful que permita aos clientes gerenciar seus produtos favoritos. A seguir estão os requisitos e especificações do projeto. 

#### 1. Cadastro e Gerenciamento de Clientes
- Permitir criar, visualizar, editar e remover clientes.
- Cada cliente deve possuir name, e-mail e password obrigatórios.
- Não permitir cadastro de e-mails duplicados.

#### 2. Gerenciamento de Produtos Favoritos
- Permitir que cada cliente mantenha uma lista de produtos favoritos.
- Não permitir produtos duplicados na lista de favoritos de um mesmo cliente.
- Os produtos devem ser validados e obtidos via API externa: [Fake Store API](https://fakestoreapi.com/docs).
- Exibir para cada produto favorito: ID, título, imagem, preço e review (se houver).

#### 3. Integração com API Externa
- Buscar produtos válidos utilizando os endpoints:
    - `GET https://fakestoreapi.com/products`
    - `GET https://fakestoreapi.com/products/{id}`

#### 4. Autenticação e Autorização
- A API deve ser pública, mas exigir autenticação e autorização para operações sensíveis.
- Implementar mecanismos de segurança básica (ex: JWT, OAuth ou similar).

#### 5. Modelagem e Validação de Dados
- Estruturar o banco de dados para evitar duplicidade de informações.
- Garantir integridade referencial entre clientes e produtos favoritos.
- Validar dados de entrada (ex: formato de e-mail, existência do produto).

#### 6. Performance e Escalabilidade
- Projetar a API para suportar alto volume de requisições.
- Utilizar práticas RESTful e otimizar consultas ao banco de dados.

#### 7. Documentação
- Documentar a API, preferencialmente utilizando OpenAPI/Swagger.
- Fornecer instruções claras de uso e exemplos de requisições.

#### 8. Banco de Dados
- Utilizaremos preferencialmente PostgreSQL



