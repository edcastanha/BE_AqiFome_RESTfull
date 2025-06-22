# Instruções de Inicialização do Projeto via Docker

Este projeto utiliza Docker e Docker Compose para facilitar a configuração e execução do ambiente.

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado

## Passos para Inicialização

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/edcastanha/BE_AqiFome_RESTfull.git
   cd BE_AqiFome_RESTfull/
   ```

2. **Construa e inicie os containers:**

   ```bash
   docker-compose up --build -d
   ```

   Isso irá construir as imagens (caso necessário) e iniciar os serviços definidos no arquivo `docker-compose.yml`.


3. **Acesse a aplicação:**

   Para ambiente de teste, você pode usar o comando para criar o primeiro cliente e popular o banco de dados:

   ```bash
   docker exec rest_api python src/scripts/seed.py
   ```

   Isso irá criar um cliente padrão e popular o banco de dados com alguns produtos favoritos.

   Após a inicialização, a aplicação estará disponível no endereço:

   - http://localhost:8000/redoc (ReDoc para documentação da API)

   - http://localhost:8000/docs (Swagger UI para documentação da API)

   (Verifique a porta configurada no `docker-compose.yml` ou no `Dockerfile` caso seja diferente)

4. **Parar os containers:**

   Para parar os containers e excluir volume Postgres, utilize:

   ```bash
   docker-compose down -v
   ```

   
---

Se tiver dúvidas ou problemas, consulte a documentação oficial do Docker ou entre em contato com o responsável pelo projeto.
