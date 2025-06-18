# Instruções de Inicialização do Projeto via Docker

Este projeto utiliza Docker e Docker Compose para facilitar a configuração e execução do ambiente.

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado

## Passos para Inicialização

1. **Clone o repositório:**

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <nome_da_pasta_do_projeto>
   ```

2. **Construa e inicie os containers:**

   ```bash
   docker-compose up --build
   ```

   Isso irá construir as imagens (caso necessário) e iniciar os serviços definidos no arquivo `docker-compose.yml`.

3. **Acesse a aplicação:**

   Após a inicialização, a aplicação estará disponível no endereço:

   - http://localhost:8000

   (Verifique a porta configurada no `docker-compose.yml` ou no `Dockerfile` caso seja diferente)

4. **Parar os containers:**

   Para parar os containers, utilize:

   ```bash
   docker-compose down
   ```

---

Se tiver dúvidas ou problemas, consulte a documentação oficial do Docker ou entre em contato com o responsável pelo projeto.
