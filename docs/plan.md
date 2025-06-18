Fase 1: Configuração e Base do Projeto
Tarefa: Configurar Ambiente de Desenvolvimento

Descrição: Instalar a linguagem de programação escolhida, o banco de dados (PostgreSQL preferencialmente) e as ferramentas necessárias.
Dependências: Nenhuma.
Estimativa: 2 horas.
Entregável: Ambiente configurado e testado.

Tarefa: Inicializar o Projeto

Descrição: Criar a estrutura básica do projeto, incluindo pastas para modelos, controladores, serviços, etc. Configurar o gerenciador de dependências.
Dependências: Tarefa 1.
Estimativa: 1 hora.
Entregável: Estrutura de diretórios inicial e arquivo de configuração de projeto.
Tarefa: Configurar Conexão com o Banco de Dados

Descrição: Adicionar as dependências do driver do banco de dados e configurar a conexão.
Dependências: Tarefa 2.
Estimativa: 1 hora.
Entregável: Função/módulo de conexão com o DB e migração inicial.
Fase 2: Módulo de Clientes
Tarefa: Modelagem da Entidade Cliente no Banco de Dados

Descrição: Criar a tabela clientes com os campos id, nome, email e restrição UNIQUE para email.
Dependências: Tarefa 3.
Estimativa: 1 hora.
Entregável: Script SQL ou migração para criar a tabela clientes.
Tarefa: Implementar Repositório de Clientes

Descrição: Criar a camada de acesso a dados (CRUD) para a entidade Cliente (funções para criar, buscar por ID/email, listar, atualizar, deletar).
Dependências: Tarefa 4.
Estimativa: 3 horas.
Entregável: Módulo de repositório de clientes com métodos CRUD.
Tarefa: Implementar Serviço de Clientes

Descrição: Criar a lógica de negócio para clientes, incluindo validação de campos obrigatórios (nome, email) e validação de unicidade do e-mail antes de criar/atualizar.
Dependências: Tarefa 5.
Estimativa: 3 horas.
Entregável: Módulo de serviço de clientes.
Tarefa: Criar Endpoints REST para Clientes

Descrição: Implementar os controladores/handlers para os endpoints de clientes (POST /clientes, GET /clientes, GET /clientes/{id}, PUT /clientes/{id}, DELETE /clientes/{id}).
Dependências: Tarefa 6.
Estimativa: 4 horas.
Entregável: Endpoints de clientes funcionando com validação básica.
Fase 3: Autenticação e Autorização
Tarefa: Implementar Geração e Validação de JWT

Descrição: Criar funções para gerar JWTs após autenticação bem-sucedida e para validar JWTs em requisições protegidas.
Dependências: Tarefa 7.
Estimativa: 4 horas.
Entregável: Módulo de segurança com funções JWT.
Tarefa: Criar Endpoint de Autenticação (Login)

Descrição: Implementar um endpoint /login que receba credenciais (ex: e-mail e senha - ou simplificado para o desafio) e retorne um JWT.
Dependências: Tarefa 8, Módulo de Clientes (para buscar usuário).
Estimativa: 2 horas.
Entregável: Endpoint de login funcionando.
Tarefa: Aplicar Middleware de Autenticação nos Endpoints

Descrição: Proteger os endpoints relevantes (todos, exceto o de login e possivelmente o de criação de cliente) com o middleware de validação de JWT.
Dependências: Tarefa 8, Tarefa 9.
Estimativa: 3 horas.
Entregável: Endpoints protegidos por autenticação.
Fase 4: Módulo de Favoritos e Integração Externa
Tarefa: Modelagem da Entidade Favorito no Banco de Dados

Descrição: Criar a tabela favoritos com id, cliente_id (chave estrangeira para clientes), produto_id (da API externa), titulo, imagem, preco, review. Adicionar uma restrição UNIQUE composta em (cliente_id, produto_id).
Dependências: Tarefa 7 (Módulo de Clientes).
Estimativa: 2 horas.
Entregável: Script SQL ou migração para criar a tabela favoritos.
Tarefa: Implementar Cliente HTTP para Fake Store API

Descrição: Criar um módulo para fazer requisições GET para https://fakestoreapi.com/products e https://fakestoreapi.com/products/{id}. Tratar possíveis erros de rede/resposta.
Dependências: Nenhuma.
Estimativa: 3 horas.
Entregável: Módulo de integração com Fake Store API.
Tarefa: Implementar Repositório de Favoritos

Descrição: Criar a camada de acesso a dados (CRUD) para a entidade Favorito (funções para criar, buscar por cliente, deletar, verificar duplicidade).
Dependências: Tarefa 11.
Estimativa: 3 horas.
Entregável: Módulo de repositório de favoritos.
Tarefa: Implementar Serviço de Favoritos

Descrição: Criar a lógica de negócio para favoritos:
Ao adicionar um favorito: chamar a Fake Store API para validar o produto_id, extrair titulo, imagem, preco, review. Verificar se o produto já não está na lista do cliente.
Ao listar favoritos: buscar no DB e retornar.
Ao remover: remover do DB.
Dependências: Tarefa 12, Tarefa 13.
Estimativa: 6 horas.
Entregável: Módulo de serviço de favoritos.
Tarefa: Criar Endpoints REST para Favoritos

Descrição: Implementar os controladores/handlers para os endpoints de favoritos (POST /clientes/{id}/favoritos, GET /clientes/{id}/favoritos, DELETE /clientes/{id}/favoritos/{produto_id}).
Dependências: Tarefa 10 (autenticação), Tarefa 14.
Estimativa: 4 horas.
Entregável: Endpoints de favoritos funcionando e protegidos.
Fase 5: Finalização e Documentação
Tarefa: Implementar Tratamento de Erros Global

Descrição: Criar um middleware/handler global para capturar e formatar erros de forma consistente (ex: 404 Not Found, 400 Bad Request, 500 Internal Server Error).
Dependências: Todas as tarefas de endpoints.
Estimativa: 2 horas.
Entregável: API com tratamento de erros padronizado.
Tarefa: Escrever Documentação Básica da API (Opcional, mas recomendado)

Descrição: Criar um arquivo README.md com instruções de como rodar a API, endpoints disponíveis, exemplos de requisição e resposta. (Se optar por OpenAPI/Swagger, esta tarefa se expande).
Dependências: Todas as tarefas de endpoints.
Estimativa: 4 horas.
Entregável: Documentação básica no README.
Tarefa: Testes Manuais e Refatoração

Descrição: Realizar testes manuais de todos os endpoints para garantir que tudo funciona conforme o esperado. Refatorar o código conforme necessário para melhor clareza e performance.
Dependências: Todas as tarefas concluídas.
Estimativa: 5 horas.
Entregável: API testada e refatorada.