# SPEC.md - Contrato de Desenvolvimento (SDD)

## 1. Visão Geral e Resultados Esperados
Este documento é a ÚNICA fonte de verdade para a orquestração do desenvolvimento. O objetivo é construir um sistema hospitalar seguro e em conformidade com a LGPD.

### Objetivos de Alto Nível
- [ ] Implementar autenticação via LDAP/AD.
- [ ] Gerenciar cadastro de pacientes (CNS/CPF).
- [ ] Garantir trilhas de auditoria imutáveis.

## 2. Contexto do Projeto (Documentação Imutável)
As definições detalhadas estão distribuídas nos seguintes documentos:
- [Visão](01-visao.md)
- [Requisitos](02-requisitos.md)
- [Casos de Uso](03-casos-uso.md)
- [Modelo de Dados](04-modelo-dados.md)
- [Interfaces](05-interfaces.md)
- [Arquitetura](06-arquitetura.md)
- [Glossário](07-glossario.md)

## 3. Limites de Escopo e Guardrails (Anti-Patterns)
**A IA DEVE:**
- Seguir rigorosamente o Modelo de Dados definido em `04-modelo-dados.md`.
- Implementar testes unitários para cada funcionalidade nova.
- Utilizar criptografia AES-256 para dados sensíveis.
- Tratar como contrato de ingestão apenas as colunas explícitas de `Paciente`, `Consulta`, `Exame` e `Internacao` descritas em `04-modelo-dados.md`.

**A IA NÃO DEVE:**
- Criar dependências externas não documentadas em `06-arquitetura.md`.
- Implementar exclusão física de registros (usar Soft Delete).
- Burlar o sistema de RBAC (Role-Based Access Control).
- Exigir LDAP/AD para que a aplicação seja executada em ambiente de desenvolvimento.

## 4. Task Breakdown (Plano de Implementação)
### Fase 1: Infraestrutura e Dados
- [ ] [TASK-001] Validar esquemas de banco de dados conforme `04-modelo-dados.md`.
- [ ] [TASK-002] Configurar ambiente de auditoria de logs.

### Fase 2: Funcionalidades Essenciais
- [ ] [TASK-003] Implementar Módulo de Autenticação (RF001).
- [ ] [TASK-004] Implementar Cadastro de Pacientes (RF002).

## 5. Critérios de Verificação Global
- [ ] 100% de cobertura em rotas de autenticação.
- [ ] Zero vulnerabilidades críticas no lint de segurança.
- [ ] Conformidade total com os esquemas JSON/OpenAPI.

## 6. Política de Armazenamento (Metrics-First)

Este projeto NÃO armazenará os dados clínicos brutos ou PII dos pacientes como fonte primária.
Em vez disso armazenaremos apenas métricas derivadas e metadados necessários para alimentar dashboards e análises.

- Dados sensíveis (e.g., CPF, CNS, descrições textuais clínicas) não devem ser persistidos pela plataforma.
- O identificador usado internamente para associação é `pac_codigo` (não CPF). Quando necessário, armazene apenas um `pac_codigo` pseudonimizado.

## 7. API Endpoints Principais

Os endpoints atualmente disponíveis e pretendidos são:

- `GET /api/pacientes/:id_paciente/jornada` — Retorna a linha do tempo do paciente (eventos agregados e métricas derivadas) para exibição no dashboard. `:id_paciente` refere-se a `pac_codigo` do AGHU.
- `GET /api/pacientes/:id_paciente` — Retorna dados triviais não sensíveis de um paciente para uso contextual no UI (ex.: `nome` reduzido, `idade`, `sexo`), quando estritamente necessário.
- `GET /api/pacientes` — Lista paginada de pacientes (por padrão primeiros 50), apenas metadados e identificadores não sensíveis.
- `GET /api/metricas` — Retorna métricas armazenadas e agregadas para relatórios e KPIs.

Todos os endpoints devem seguir os guardrails de privacidade definidos em `06-arquitetura.md` e validar schemas JSON descritos em `04-modelo-dados.md`.
