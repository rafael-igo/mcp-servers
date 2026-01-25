# Decisões Técnicas (ADRs)

**Architecture Decision Records**
**Última atualização:** 2026-01-25

---

## Como Usar Este Arquivo

Este arquivo registra todas as decisões técnicas importantes do projeto usando o formato ADR (Architecture Decision Record).

### Template

```markdown
## ADR-NNN: [Título da Decisão]

**Data:** YYYY-MM-DD
**Status:** [Proposto/Aceito/Rejeitado/Depreciado/Superseded]
**Decisores:** [Quem participou da decisão]

### Contexto
[Por que precisamos tomar essa decisão? Qual problema estamos resolvendo?]

### Decisão
[O que foi decidido?]

### Alternativas Consideradas
1. **[Opção A]**
   - Prós: [lista]
   - Contras: [lista]

2. **[Opção B]**
   - Prós: [lista]
   - Contras: [lista]

### Consequências

**Positivas:**
- [Benefício 1]
- [Benefício 2]

**Negativas:**
- [Trade-off 1]
- [Trade-off 2]

**Riscos:**
- [Risco 1 e mitigação]
- [Risco 2 e mitigação]

### Implementação
[Como será implementado? Passos necessários?]

### Notas
[Informações adicionais relevantes]

### Referências
- [Links, documentação, discussões]
```

---

## 2026-01-25

### ADR-001: Sistema de Agentes Especializados

**Data:** 2026-01-25
**Status:** Aceito ✅
**Decisores:** Agente Arquiteto, Equipe de Desenvolvimento

#### Contexto

O projeto I GO Experience é complexo, com múltiplos módulos (Transfer, Rooming, Check-in, Backend) e requer coordenação eficiente entre diferentes áreas de especialização. Precisávamos de uma forma estruturada de organizar o desenvolvimento, capturar conhecimento e tomar decisões técnicas informadas.

#### Decisão

Implementar um **Sistema de Agentes Especializados** com:
- Agentes de coordenação (Insights, Resumo)
- Agentes especializados por módulo (Transfer, Rooming, etc.)
- Sistema de memória persistente
- Orquestrador automático de detecção de intenção
- MCPs para ferramentas especializadas

#### Alternativas Consideradas

1. **Documentação tradicional + Wiki**
   - Prós: Simples, familiar
   - Contras: Estática, desatualiza rápido, difícil de navegar

2. **Sistema de tickets (Jira/Linear)**
   - Prós: Rastreamento de tarefas
   - Contras: Não captura contexto técnico, overhead de gestão

3. **Sistema de agentes IA especializado** ⭐ ESCOLHIDO
   - Prós: Dinâmico, contexto sempre atualizado, captura conhecimento, decisões documentadas
   - Contras: Curva de aprendizado inicial

#### Consequências

**Positivas:**
- Documentação viva e sempre atualizada
- Captura de todas as ideias e insights
- Decisões técnicas bem documentadas
- Onboarding facilitado para novos membros
- Desenvolvimento paralelo sem conflitos
- Memória persistente do projeto

**Negativas:**
- Requer disciplina para manter atualizado
- Estrutura de pastas mais complexa
- Depende de MCPs funcionando

**Riscos:**
- Documentação pode divergir do código real
  - **Mitigação:** Agentes atualizam ao implementar
- Sistema pode ficar complexo demais
  - **Mitigação:** Orquestrador simplifica uso

#### Implementação

1. ✅ Criar estrutura `projeto-claude/01-AGENTES/`
2. ✅ Implementar Agente de Insights
3. ✅ Implementar Agente de Resumo
4. ✅ Criar sistema de memória em `06-MEMORIA-AGENTE/`
5. ✅ Criar orquestrador de detecção de intenção
6. ✅ Integrar com MCPs existentes
7. [ ] Treinar equipe no uso do sistema
8. [ ] Criar automações adicionais

#### Notas

Este ADR é meta - documenta a decisão de usar ADRs! O sistema foi criado em um único dia (2026-01-25), demonstrando a viabilidade da abordagem.

#### Referências

- `projeto-claude/README.md`
- `projeto-claude/01-AGENTES/ORQUESTRADOR.md`
- `api/mcp-servers/README.md`

---

### ADR-002: Criação do Agente de Insights

**Data:** 2026-01-25
**Status:** Aceito ✅
**Decisores:** Agente Arquiteto

#### Contexto

Precisávamos de uma forma estruturada de capturar ideias do usuário, consultar agentes especialistas, e tomar decisões informadas sobre implementação, priorização e arquitetura.

#### Decisão

Criar um **Agente de Insights** responsável por:
- Capturar todas as ideias e sugestões
- Classificar por tipo (feature, bug, improvement, etc.)
- Consultar agentes especialistas automaticamente
- Consolidar feedback técnico
- Tomar decisões baseadas em análise
- Registrar tudo em `INSIGHTS_CAPTURADOS.md`

#### Alternativas Consideradas

1. **Captura manual em notas**
   - Prós: Simples
   - Contras: Ideias se perdem, sem consulta a especialistas

2. **Sistema de issues no GitHub**
   - Prós: Rastreável
   - Contras: Overhead, sem consulta automática a agentes

3. **Agente de Insights especializado** ⭐ ESCOLHIDO
   - Prós: Automático, consulta especialistas, decisões documentadas
   - Contras: Requer estrutura de agentes

#### Consequências

**Positivas:**
- Nenhuma ideia se perde
- Decisões são sempre informadas
- Feedback de múltiplos especialistas
- Histórico completo de insights

**Negativas:**
- Requer disciplina para usar
- Pode gerar muitos insights não implementados

**Riscos:**
- Backlog de insights crescer demais
  - **Mitigação:** Revisão periódica e priorização

#### Implementação

1. ✅ Criar `agente-insights/PROMPT.md`
2. ✅ Criar `agente-insights/RESPONSABILIDADES.md`
3. ✅ Criar `agente-insights/INSIGHTS_CAPTURADOS.md`
4. ✅ Integrar com sistema de memória
5. ✅ Integrar com orquestrador

#### Notas

Primeiro insight capturado: A criação do próprio agente de insights! (INS-0001)

#### Referências

- `projeto-claude/01-AGENTES/agente-insights/`

---

### ADR-003: Criação do Agente de Resumo

**Data:** 2026-01-25
**Status:** Aceito ✅
**Decisores:** Agente Arquiteto, Agente de Insights

#### Contexto

Precisávamos de uma forma rápida de obter status do projeto, progresso por módulo, próximos passos e histórico de ações, sem precisar ler múltiplos arquivos manualmente.

#### Decisão

Criar um **Agente de Resumo** responsável por:
- Gerar status geral do projeto
- Calcular progresso por módulo
- Listar próximos passos priorizados
- Mostrar histórico de ações
- Apresentar decisões técnicas
- Gerar relatórios para diferentes públicos (técnico, executivo, onboarding)

#### Alternativas Consideradas

1. **Scripts de CI/CD gerando relatórios**
   - Prós: Automático
   - Contras: Estático, não interativo, formatação fixa

2. **Dashboard web**
   - Prós: Visual
   - Contras: Requer infraestrutura, manutenção

3. **Agente de Resumo interativo** ⭐ ESCOLHIDO
   - Prós: Dinâmico, adaptável, linguagem natural
   - Contras: Depende da qualidade da memória

#### Consequências

**Positivas:**
- Status sempre disponível em segundos
- Adaptável ao público (técnico vs executivo)
- Nível de detalhe configurável
- Facilita onboarding

**Negativas:**
- Acurácia depende de memória atualizada
- Cálculos de progresso são estimativas

**Riscos:**
- Informações desatualizadas se memória não for atualizada
  - **Mitigação:** Agentes atualizam automaticamente ao implementar

#### Implementação

1. ✅ Criar `agente-resumo/PROMPT.md`
2. ✅ Criar `agente-resumo/RESPONSABILIDADES.md`
3. ✅ Integrar com sistema de memória
4. ✅ Integrar com orquestrador
5. ✅ Definir templates de resumo

#### Notas

Trabalha em conjunto com Agente de Insights - um captura e decide, outro reporta e informa.

#### Referências

- `projeto-claude/01-AGENTES/agente-resumo/`

---

## Índice de ADRs

### Por Status
- **Aceito:** ADR-001, ADR-002, ADR-003
- **Proposto:** (nenhum)
- **Rejeitado:** (nenhum)
- **Depreciado:** (nenhum)

### Por Data
- **2026-01-25:** ADR-001, ADR-002, ADR-003

### Por Categoria
- **Arquitetura:** ADR-001
- **Agentes:** ADR-002, ADR-003
- **Infraestrutura:** (nenhum ainda)
- **Frontend:** (nenhum ainda)
- **Backend:** (nenhum ainda)

---

**Próximo ADR disponível:** ADR-004
