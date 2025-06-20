# Plano de Tarefas – API RESTful Favoritos de Produtos

## 1. Planejamento e Arquitetura

- [x] **Análise de requisitos**  
    Revisar e detalhar todos os requisitos funcionais e não funcionais dos documentos fornecidos.
- [x] **Definição da arquitetura**  
    Escolhida um arquitetura proxima ao DDD (Domain-Driven Design), separando camadas: Domain, Repository, Application, Infrastructure, Presentation.
- [x] **Escolha de tecnologias**  
    Definida a linguagem PYTHON, frameworks FastAPI, banco de dados POSTGRES, ORM SQLAlchemy, biblioteca de autenticação (preferencialmente OAuth2) ????? .

- [ ] **Modelagem inicial**  
    Criar diagramas de entidades (ERD) e fluxos de uso.

## 2. Modelagem de Domínio

- [x] **Definir entidades e agregados**  
    - Cliente (com nome, e-mail)
    - ProdutoFavorito (referência ao cliente e ao produto externo)
- [x] **Criar Value Objects**  
    - E-mail (validação de formato e unicidade)
- [x] **Definir repositórios e interfaces**  
    - ClienteRepository
    - ProdutoFavoritoRepository

## 3. Implementação da Camada de Domínio

- [x] **Implementar entidades e regras de negócio**  
    - Respeitar princípios SOLID e Clean Code
    - Garantir unicidade de e-mail e não duplicidade de favoritos
- [x] **Implementar serviços de domínio**  
    - Adicionar/remover favoritos com validação via API externa

## 4. Infraestrutura e Integração

- [x] **Configurar banco de dados**  
    - Criar migrations e scripts de inicialização
- [x] **Implementar repositórios concretos**  
    - Usar ORM para persistência
- [ ] **Implementar integração com Fake Store API**  
    - Serviços para buscar e validar produtos externos

## 5. Camada de Aplicação

- [x] **Implementar casos de uso (Use Cases/Application Services)**  
    - Cadastro, edição, remoção e listagem de clientes
    - Adição, remoção e listagem de favoritos
- [ ] **Implementar DTOs e mapeamentos**

## 6. Camada de Apresentação (API)

- [ ] **Implementar controladores RESTful**  
    - Endpoints para clientes e favoritos, seguindo boas práticas REST
- [ ] **Validação de entrada e tratamento de erros**  
    - Utilizar middlewares/handlers para validação e respostas padronizadas

## 7. Segurança

- [ ] **Implementar autenticação e autorização**  
    - JWT ou OAuth para proteger endpoints sensíveis
- [ ] **Garantir segurança básica (validação, CORS, rate limiting)**

## 8. Testes

- [ ] **Testes unitários**  
    - Cobrir entidades, serviços de domínio e casos de uso
- [ ] **Testes de integração**  
    - Testar endpoints e integração com banco/API externa

## 9. Documentação

- [ ] **Documentar a API (OpenAPI/Swagger)**  
    - Gerar documentação automática e exemplos de uso
- [ ] **Escrever instruções de instalação e uso**

## 10. Revisão e Refino

- [ ] **Revisão de código (Code Review)**  
    - Garantir aderência a SOLID, Clean Code e DDD
- [ ] **Ajustes finais e deploy**

---

> **Observações:**  
- Priorizar clareza, modularidade e separação de responsabilidades.  
- Evitar duplicidade de dados e garantir integridade referencial.  
- Manter documentação e código sempre atualizados.
```