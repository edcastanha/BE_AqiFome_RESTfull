ADR 001: Escolha da Arquitetura da Aplicação
Título: Escolha de Arquitetura da Aplicação: API RESTful em Camadas
Status: Proposta
Contexto: A API precisa ser robusta, escalável, de fácil manutenção e seguir boas práticas. Uma arquitetura em camadas separa as responsabilidades, facilitando o desenvolvimento e a testabilidade.
Decisão: Adotar uma arquitetura de aplicação em camadas (Apresentação, Negócio, Integração, Dados).
Consequências:
Positivas: Maior separação de responsabilidades, melhor testabilidade de unidades e integração, facilidade de manutenção e escalabilidade, conformidade com princípios REST.
Negativas: Aumento inicial na complexidade do código devido à separação, mas que se paga a longo prazo.

ADR 002: Estratégia de Autenticação e Autorização
Título: Estratégia de Autenticação e Autorização via JWT (JSON Web Tokens)
Status: Proposta
Contexto: A API deve ser pública, mas requer autenticação e autorização para proteger seus endpoints. JWTs são amplamente utilizados em APIs RESTful por serem stateless, escaláveis e seguros.
Decisão: Implementar autenticação baseada em JWTs para verificar a identidade do usuário e autorização baseada em papéis/escopos para controlar o acesso aos recursos.
Consequências:
Positivas: Escalabilidade (stateless), segurança (assinatura digital), interoperabilidade, redução de carga no servidor (não exige sessão).
Negativas: Gerenciamento de revogação de tokens em caso de comprometimento pode ser mais complexo (embora para este desafio inicial possa ser simplificado).

ADR 003: Modelagem de Dados para Clientes e Favoritos
Título: Modelagem de Dados Relacional para Clientes e Favoritos
Status: Proposta
Contexto: Precisamos armazenar clientes e seus produtos favoritos, garantindo a unicidade do e-mail do cliente e a não duplicação de produtos na lista de favoritos de um cliente. O PostgreSQL é o banco de dados sugerido e é relacional.
Decisão: Utilizar um modelo relacional com tabelas clientes e favoritos, com um relacionamento de um para muitos entre clientes e favoritos, e uma chave composta para garantir a unicidade do produto por cliente.
Consequências:
Positivas: Integridade de dados garantida por restrições de banco de dados (unique, foreign key), consultas eficientes para relacionamentos, compatibilidade com PostgreSQL.
Negativas: Pode exigir joins para recuperar dados completos de favoritos, o que é padrão em DBs relacionais.

ADR 004: Tratamento de Integração com API Externa
Título: Estratégia de Integração com Fake Store API
Status: Proposta
Contexto: A validação de produtos deve ocorrer via integração com a Fake Store API. É crucial que essa integração seja robusta e trate cenários de falha.
Decisão: Criar um módulo/cliente HTTP dedicado para interagir com a Fake Store API. Implementar mecanismos de tratamento de erros (timeouts, retries controlados se aplicável) e encapsular a lógica de busca e validação de produtos.
Consequências:
Positivas: Separação clara da lógica de integração, facilidade de testar a camada de integração isoladamente, resiliência a falhas da API externa (até certo ponto).
Negativas: Adiciona uma camada de abstração, que é um custo razoável para os benefícios.