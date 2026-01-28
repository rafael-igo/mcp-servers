# Decisões Técnicas - ADRs - igo-journey/main

Registro de decisões arquiteturais importantes.

---

## Normalização do esquema de banco de dados

**Data:** 2026-01-26
**Projeto/Branch:** igo-journey/main

### Contexto
Migração do esquema SQL Server legado (tabelas largas com ~160 campos) para PostgreSQL normalizado

### Alternativas Consideradas
1) Manter estrutura flat do legado; 2) Normalização parcial; 3) Normalização completa com JSONB para flexibilidade

### Decisão
Normalização completa com JSONB para flexibilidade

### Razão
**Escalabilidade**: Tabelas normalizadas permitem N trechos de voo, N documentos, N hospedagens por convidado.
**Flexibilidade**: JSONB em raw_data, settings e metadata permite armazenar campos variáveis sem alterar schema.
**Performance**: Índices específicos por domínio, evitando tabelas com 160+ colunas.
**Manutenibilidade**: Domínios separados (Aéreo, Hospedagem, Transfer) com responsabilidades claras.
**IA-Ready**: Tabelas para embeddings (pgvector), conversas e sugestões já preparadas.

---
