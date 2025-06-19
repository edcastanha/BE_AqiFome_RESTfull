# PROMPT.md

## Diretrizes para o Agent

### 1. Princípios Gerais

- Sempre explique as decisões de implementação, justificando escolhas técnicas e arquiteturais.
- Priorize a aplicação dos princípios SOLID, Clean Code e DDD em todas as tarefas, independentemente do framework ou biblioteca utilizada.
- Mantenha o CORE do sistema (entidades, regras de negócio e casos de uso) isolado de frameworks e infraestrutura, facilitando testes e futuras migrações.

### 2. Organização do Projeto

- Separe claramente as camadas de domínio, aplicação, infraestrutura e interfaces.
- O domínio deve conter apenas entidades, value objects, agregados, repositórios (interfaces) e regras de negócio.
- Frameworks e bibliotecas devem ser utilizados apenas nas camadas externas (infraestrutura e interfaces).

### 3. Boas Práticas

- Utilize nomes claros e descritivos para classes, métodos e variáveis.
- Escreva métodos curtos, com responsabilidade única.
- Evite duplicidade de código e comentários desnecessários.
- Documente todas as decisões relevantes no código e, se necessário, em ADRs (docs/adr/).

### 4. Testes e Qualidade

- Sempre que um novo commit for solicitado:
  - Execute a verificação de cobertura de testes de unidade (diretório `tests/`).
  - Realize conferência automática de boas práticas (SOLID, Clean Code e documentação).
  - Não aprove commits que reduzam a cobertura de testes ou violem as boas práticas estabelecidas.

### 5. Documentação

- Explique no PR ou commit as decisões tomadas, principalmente quando envolverem arquitetura, design ou trade-offs.
- Atualize a documentação e ADRs sempre que houver mudanças relevantes.

---

**Resumo:**  
O Agent deve garantir que o código entregue seja limpo, testável, desacoplado de frameworks, bem documentado e coberto por testes, explicando sempre as decisões e mantendo o CORE do como namespace para os import validos. Assegure que as práticas de SOLID, Clean Code e DDD sejam seguidas rigorosamente, priorizando a qualidade e a manutenibilidade do sistema. A documentação deve ser clara e atualizada, refletindo as decisões de design e arquitetura tomadas durante o desenvolvimento.

### 6. Estrutura de Pastas
- `core/`: Contém o núcleo do sistema, incluindo entidades, regras de negócio e casos de uso.
