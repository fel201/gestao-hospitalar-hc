# Tasks - Plano de Implementação Completo

Plano de execução de todas as tarefas necessárias para o Sistema de Gestão da Jornada Assistencial do Hospital de Clinicas da UFPE.

---

## FASE 1: Infraestrutura, Banco de Dados e Configuração

### [TASK-001] Validar esquemas de banco de dados conforme `04-modelo-dados.md`
- [x] Criar migrações Alembic para tabelas `PACIENTE`, `CONSULTA`, `EXAME`, `INTERNACAO`
- [ ] Criar tabela `METRICA` com schema de métricas derivadas
- [ ] Criar tabela `AUDIT_LOG` para rastreamento de acessos (LGPD)
- [x] Validar integridade referencial e constraints
- [ ] Testes de validação de esquema contra JSON Schema definido
- **Prioridade**: Essencial
- **Dependências**: Nenhuma
- **Status**: [70%] Em Progresso

### [TASK-002] Configurar ambiente de auditoria de logs
- [ ] Implementar middleware de logging centralizado em FastAPI
- [ ] Criar modelo `AuditLog` para registrar acesso a dados
- [ ] Configurar rotação de logs com timestamp
- [ ] Implementar mascaramento de PII em logs
- [ ] Documentar política de retenção de logs (90 dias?)
- **Prioridade**: Essencial
- **Dependências**: TASK-001
- **Status**: [0%] Não iniciado

### [TASK-003] Configurar variáveis de ambiente e segurança
- [x] Criar arquivo `.env.example` com todas as variáveis necessárias
- [x] Configurar suporte para LDAP/AD via variáveis (AD_URL, AD_USER, AD_PASSWORD)
- [x] Implementar fallback para MockAuthProvider quando AD não disponível
- [ ] Configurar AES-256 para criptografia de dados sensíveis
- [x] Setup de geração de chaves RSA para JWT
- [x] Validar carregamento seguro de secrets do `.env`
- **Prioridade**: Alta
- **Dependências**: Nenhuma
- **Status**: [83%] Em Progresso

---

## FASE 2: Autenticação e Autorização (RF001, RNF002)

### [TASK-004] Implementar módulo de autenticação com JWT
- [x] Criar `auth.py` com implementação de JWT (encode/decode)
- [x] Implementar endpoint `POST /api/auth/login` com suporte a JWT
- [x] Implementar endpoint `POST /api/auth/refresh` para renovação de token
- [x] Criar modelo `RefreshToken` com suporte a groups
- [x] Validar tokens JWT em todas as rotas protegidas
- [x] Retornar `access_token` e `refresh_token` no login
- [x] Implementar expiração configurável de tokens
- **Prioridade**: Essencial
- **Dependências**: TASK-003
- **Status**: [100%] Completo
- **Referência**: `CARE-RF001`

### [TASK-005] Implementar MockAuthProvider para desenvolvimento
- [x] Criar provedor de autenticação mock com usuários pré-configurados
- [x] Suportar credencial `admin/admin` para testes
- [x] Permitir login sem LDAP quando `AD_URL` não está configurado
- [x] Gerar tokens JWT válidos para mock provider
- [x] Documentar como usar em ambiente de desenvolvimento
- **Prioridade**: Alta
- **Dependências**: TASK-004
- **Status**: [100%] Completo

### [TASK-006] Implementar RBAC (Role-Based Access Control)
- [x] Definir roles: `GESTOR`, `MEDICO`, `ENFERMEIRO`, `ADMIN` (via grupos AD)
- [ ] Criar tabelas para roles e permissões
- [ ] Implementar decorator `@require_role()` em FastAPI
- [x] Implementar verificação de permissões em endpoints (em `/api/admin-only-data`)
- [ ] Gerar logs de auditoria para acesso negado
- **Prioridade**: Alta
- **Dependências**: TASK-004
- **Status**: [40%] Em Progresso

### [TASK-007] Implementar suporte LDAP/AD (quando disponível)
- [x] Integrar biblioteca `ldap3`
- [x] Criar `ActiveDirectoryAuthProvider` para autenticação contra AD
- [x] Mapeamento de grupos LDAP para roles da aplicação
- [x] Fallback automático para MockAuthProvider se LDAP falhar
- [ ] Testes com credenciais LDAP mock
- **Prioridade**: Baixa (opcional no desenvolvimento)
- **Dependências**: TASK-004
- **Status**: [80%] Em Progresso
- **Referência**: `CARE-RF001`

---

## FASE 3: Modelo de Dados e Persistência

### [TASK-008] Implementar providers para ingestão de dados
- [x] Criar `PacienteProviderInterface` interface
- [x] Implementar `PacienteCsvProvider` para leitura do CSV
- [x] Implementar `PacientePostgresProvider` para persistência em BD
- [ ] Validar dados contra JSON Schema antes de persistir
- [ ] Implementar validação de duplicatas (CPF/CNS/prontuário)
- **Prioridade**: Essencial
- **Dependências**: TASK-001
- **Status**: [60%] Em Progresso

### [TASK-009] Implementar providers para Consultas
- [x] Criar interface de consultas
- [x] Implementar `ConsultasCsvProvider` para leitura do CSV
- [ ] Implementar persistência em tabela `CONSULTA`
- [ ] Validar timestamps e relacionamento com paciente
- [ ] Registrar em `AUDIT_LOG` cada carga de dados
- **Prioridade**: Essencial
- **Dependências**: TASK-001, TASK-008
- **Status**: [40%] Em Progresso

### [TASK-010] Implementar providers para Exames
- [x] Criar interface de exames
- [x] Implementar `ExameCsvProvider` para leitura do CSV
- [ ] Implementar persistência em tabela `EXAME`
- [ ] Validar IDs de unidade executora e atendimento
- [ ] Registrar em `AUDIT_LOG` cada carga de dados
- **Prioridade**: Essencial
- **Dependências**: TASK-001, TASK-008
- **Status**: [40%] Em Progresso

### [TASK-011] Implementar providers para Internações
- [x] Criar interface de internações
- [x] Implementar `InternacoesCsvProvider` para leitura do CSV
- [ ] Implementar persistência em tabela `INTERNACAO`
- [ ] Calcular `tempo_permanencia_dias` automaticamente
- [ ] Registrar em `AUDIT_LOG` cada carga de dados
- **Prioridade**: Essencial
- **Dependências**: TASK-001, TASK-008
- **Status**: [40%] Em Progresso

### [TASK-012] Implementar modelo de Métricas Derivadas
- [ ] Criar tabela `METRICA` com schema definido
- [ ] Implementar classe modelo `Metrica` em SQLAlchemy
- [ ] Criar queries SQL para cálculo de métricas a partir de eventos
- [ ] Garantir que métricas não persistem PII
- [ ] Implementar índices para performance de queries de métricas
- **Prioridade**: Essencial
- **Dependências**: TASK-001, TASK-009, TASK-010, TASK-011
- **Status**: [0%] Não iniciado
- **Referência**: `CARE-RF008`

---

## FASE 4: Funcionalidades Principais - Jornada Assistencial

### [TASK-013] Implementar reconstrução cronológica da jornada
- [x] Criar função `obter_jornada_paciente()` que agrega eventos (consultas, exames, internações)
- [x] Ordenar eventos por `data_hora` (timestamp)
- [x] Validar sequência cronológica para detecção de anomalias
- [x] Testes com diferentes cenários de jornada
- **Prioridade**: Essencial
- **Dependências**: TASK-008, TASK-009, TASK-010, TASK-011
- **Status**: [100%] 
- **Referência**: `CARE-RF003`

### [TASK-014] Implementar identificação de recorrências (reinternações)
- [ ] Criar função `identify_recurrences()` para detectar padrões
- [ ] Definir intervalo configurável para considerar reinternação (ex.: 30 dias)
- [ ] Calcular número de reinternações por paciente
- [ ] Testes com jornadas simuladas com reinternações conhecidas
- [ ] Gerar flags de alerta para reinternações frequentes
- **Prioridade**: Essencial
- **Dependências**: TASK-013
- **Status**: [0%] Não iniciado
- **Referência**: `CARE-RF005`, `CARE-UC003`

### [TASK-015] Implementar cálculo de tempo entre eventos
- [x] Criar função `calculate_time_intervals()` para calcular tempo entre eventos
- [ ] Métrica: tempo de espera (agendamento até consulta)
- [ ] Métrica: tempo de permanência (entrada até saída)
- [ ] Métrica: duração de internação (admissão até alta)
- [x] Gerar campo `tempo_intervalo_horas` entre eventos
- [ ] Testes com intervalos conhecidos para validar cálculos
- **Prioridade**: Essencial
- **Dependências**: TASK-013
- **Status**: [33%]
- **Referência**: `CARE-RF007`, `CARE-UC005`

### [TASK-016] Implementar identificação de gargalos operacionais
- [ ] Criar função `identify_bottlenecks()` para análise de atrasos
- [ ] Calcular tempo médio entre eventos por tipo
- [ ] Identificar etapas com atraso acima do percentil 75
- [ ] Agregar dados por unidade funcional e especialidade
- [ ] Gerar alertas para gargalos críticos
- [ ] Testes com dados históricos simulados
- **Prioridade**: Essencial
- **Dependências**: TASK-015, TASK-012
- **Status**: Não iniciado
- **Referência**: `CARE-RF007`, `CARE-UC004`

### [TASK-016-2] Dashboard da Jornada Assistencial Principal

- [ ] Exibir fluxo da jornada assistencial
- [ ] Organizar eventos em etapas
- [ ] Mostrar KPIs por etapa
- [ ] Mostrar quantidade de eventos por etapa
- [ ] Permitir filtro por especialidade
- [ ] Permitir filtro por período
- **Prioridade**: Essencial
- **Status**: Não iniciado


## FASE 5: API Endpoints - Backend

### [TASK-017] Implementar endpoint `GET /api/pacientes/:id_paciente`
- [ ] Retornar apenas dados não-sensíveis (nome reduzido, idade, sexo)
- [ ] Validar permissões RBAC antes de retornar
- [ ] Registrar acesso em `AUDIT_LOG`
- [ ] Responder com JSON conforme schema definido
- [ ] Tratamento de erro 404 para paciente inexistente
- [ ] Testes unitários com coverage
- **Prioridade**: Baixa
- **Dependências**: TASK-004, TASK-008
- **Status**: Em Progresso
- **Referência**: SPEC.md Section 7

### [TASK-018] Implementar endpoint `GET /api/pacientes` (lista paginada)
- [x] Retornar primeiros 50 pacientes por padrão
- [ ] Suportar paginação via query params (`page`, `limit`)
- [x] Retornar apenas metadados e identificadores não-sensíveis
- [ ] Filtros opcionais: `especialidade`, `unidade`, `data_inicio`, `data_fim`
- [ ] Ordenação por nome ou data de criação
- [ ] Testes de paginação e filtros
- **Prioridade**: Essencial
- **Dependências**: TASK-004, TASK-008
- **Status**: Em Progresso
- **Referência**: SPEC.md Section 7

### [TASK-019] Implementar endpoint `GET /api/paciente/jornada`
- [x] Retornar timeline completa do paciente
- [x] Agregar consultas, exames e internações em ordem cronológica
- [ ] Incluir cálculos de intervalo e tempo entre eventos
- [ ] Incluir flags de recorrência e gargalos identificados
- [x] Responder com JSON conforme schema definido
- [ ] Registrar acesso em `AUDIT_LOG`
- [ ] Testes de performance com jornadas grandes
- **Prioridade**: Baixa
- **Dependências**: TASK-004, TASK-013, TASK-014, TASK-015
- **Status**: Em Progresso
- **Referência**: `CARE-UC001`, SPEC.md Section 7

### [TASK-020] Implementar endpoint `GET /api/metricas`
- [ ] Suportar filtro obrigatório por especialidade
- [ ] Retornar quantidade de consultas, exames, procedimentos e prontuários
- [ ] Retornar KPIs referentes a uma determinada especialidade.
- [ ] Retornar distribuição dos eventos por etapa da jornada
- **Prioridade**: Essencial
- **Status**: Não iniciado

### [TASK-021] Implementar endpoint `GET /api/metricas/indicadores`
- [ ] Retornar indicadores principais:
  - Tempo médio de permanência
  - Tempo médio de espera
  - Taxa de reinternação
  - Fluxo predominante
  - Ocupação por unidade
- [ ] Suportar filtros por período, unidade e especialidade
- [ ] Responder em tempo real (< 10 segundos)
- [ ] Testes de performance e precisão de cálculos
- **Prioridade**: Essencial
- **Dependências**: TASK-012, TASK-016
- **Status**: Não iniciado
- **Referência**: `CARE-UC005`

### [TASK-023] Implementar endpoint `POST /api/token/refresh`
- [x] Aceitar `refresh_token` em JSON
- [x] Validar token e gerar novo `access_token`
- [x] Manter `refresh_token` anterior (não rotacionar por padrão)
- [ ] Registrar renovação de token em `AUDIT_LOG`
- [ ] Testes de renovação com tokens expirados e válidos
- **Prioridade**: Alta
- **Dependências**: TASK-004
- **Status**: Em Progresso

### [TASK-024] Implementar middleware de autenticação e autorização
- [x] Validar JWT em todas as rotas protegidas
- [x] Injetar contexto de usuário em requests
- [ ] Validar RBAC com decorators `@require_role()`
- [ ] Registrar acesso não autorizado em `AUDIT_LOG`
- [x] Tratamento de erro 401 (não autenticado) e 403 (sem permissão)
- [ ] Testes de middleware com tokens válidos e inválidos
- **Prioridade**: Essencial
- **Dependências**: TASK-004, TASK-006
- **Status**: Em Progresso

### [TASK-025] Implementar tratamento de erros centralizado
- [ ] Criar classe `AppException` e subclasses específicas
- [ ] Middleware para capturar e formatar erros em JSON
- [ ] Logs estruturados para erros com contexto
- [ ] Máscara de PII em mensagens de erro
- [ ] HTTP status codes apropriados para cada tipo de erro
- [ ] Testes de tratamento de erros
- **Prioridade**: Alta
- **Dependências**: TASK-002
- **Status**: Não iniciado

---

## FASE 6: Frontend - Vue/TypeScript


### [TASK-028] Implementar página de Lista de Pacientes
- [x] Exibir tabela com paginação
- [x] Chamada para `GET /api/pacientes`
- [ ] Filtros: nome, especialidade, unidade, data
- [x] Busca rápida (search box)
- [x] Link para detalhe do paciente
- [ ] Indicadores de status (reinternação, gargalo)
- [ ] Testes de paginação e filtros
- **Prioridade**: Baixa
- **Dependências**: TASK-018, TASK-026
- **Status**: Em Progresso

### [TASK-029] Implementar página de Detalhe do Paciente
- [x] Exibir informações básicas do paciente
- [ ] Componente timeline visual da jornada
- [x] Chamada para `GET /api/paciente/jornada`
- [x] Exibir eventos em ordem cronológica
- [ ] Modal ou painel lateral para detalhes de cada evento
- [ ] Indicadores de recorrência e gargalos
- [x] Responsividade e performance
- **Prioridade**: Baixa
- **Dependências**: TASK-019, TASK-026
- **Status**: [71%] Em Progresso
- **Referência**: `CARE-UC001`, `CARE-UC002`

### [TASK-030] Implementar componente Timeline visual
- [ ] Renderizar eventos em formato visual cronológico
- [ ] Cores diferenciadas por tipo de evento (consulta, exame, internação)
- [ ] Exibir timestamps e duração entre eventos
- [ ] Interatividade: clicar para expandir detalhes
- [ ] Scroll horizontal/vertical conforme necessário
- [ ] Testes de renderização com diferentes números de eventos
- **Prioridade**: Baixa
- **Dependências**: TASK-019
- **Status**: [ ] Não iniciado

### [TASK-031] Implementar componente de Indicadores/KPIs
- [ ] Cards exibindo tempo médio, taxa de reinternação, etc.
- [ ] Gráficos com Chart.js ou equivalente
- [ ] Indicadores de tendência (seta para cima/baixo)
- [ ] Responsividade mobile
- [ ] Testes de renderização
- **Prioridade**: Alta
- **Dependências**: TASK-020, TASK-021
- **Status**: [ ] Não iniciado

### [TASK-032] Implementar navegação baseada em roles
- [ ] Menu diferenciado por role (GESTOR, MEDICO, ENFERMEIRO)
- [ ] Visibilidade condicional de páginas/componentes
- [ ] Tratamento de acesso não autorizado
- [ ] Testes de navegação por role
- **Prioridade**: Alta
- **Dependências**: TASK-006, TASK-026
- **Status**: [ ] Não iniciado

---

## FASE 7: Segurança, Criptografia e LGPD

### [TASK-034] Implementar criptografia AES-256 para dados sensíveis
- [ ] Usar biblioteca `cryptography` do Python
- [ ] Criptografar campos sensíveis no banco de dados (se aplicável)
- [ ] Implementar funções `encrypt()` e `decrypt()`
- [ ] Gerenciar chaves de criptografia via `.env`
- [ ] Testes de criptografia/descriptografia
- **Prioridade**: Essencial
- **Dependências**: TASK-003
- **Status**: [0%] Não iniciado
- **Referência**: `CARE-RNF001`

### [TASK-035] Implementar auditoria de acesso a dados sensíveis (LGPD)
- [ ] Registrar toda visualização de dados do paciente em `AUDIT_LOG`
- [ ] Incluir: usuário, timestamp, IP, ação realizada
- [ ] Alertas para acessos não esperados ou suspeitos
- [ ] Retenção configurável de logs (sugerido: 90 dias)
- [ ] Testes de auditoria com diferentes cenários de acesso
- **Prioridade**: Essencial
- **Dependências**: TASK-002, TASK-004
- **Status**: [0%] Não iniciado
- **Referência**: `CARE-RNF002`

### [TASK-036] Implementar conformidade com LGPD
- [ ] Documentar política de privacidade
- [ ] Implementar direito ao esquecimento (Soft Delete com `deleted_at`)
- [ ] Consentimento explícito para armazenamento de dados (TCLE)
- [ ] Mascaramento de PII em logs e backups
- [ ] Testes de conformidade com regras LGPD
- **Prioridade**: Essencial
- **Dependências**: TASK-002, TASK-035
- **Status**: [ ] Não iniciado
- **Referência**: `CARE-RNF002`

### [TASK-037] Implementar proteção contra SQL Injection
- [ ] Usar SQLAlchemy ORM (protegido por padrão)
- [ ] Auditar queries SQL geradas manualmente
- [ ] Validar inputs antes de queries
- [ ] Testes de segurança com payloads de SQL injection
- **Prioridade**: Essencial
- **Dependências**: TASK-008
- **Status**: [ ] Não iniciado

### [TASK-038] Implementar proteção contra XSS/CSRF
- [ ] Validar e sanitizar inputs em frontend
- [ ] Implementar CSRF token se necessário
- [ ] Headers de segurança: X-Content-Type-Options, X-Frame-Options, etc.
- [ ] Testes de XSS com payloads maliciosos
- **Prioridade**: Alta
- **Dependências**: TASK-026
- **Status**: [ ] Não iniciado

### [TASK-039] Implementar rate limiting
- [ ] Limitar tentativas de login (ex.: 5 tentativas/15 min)
- [ ] Limitar requisições por IP/usuário
- [ ] Usar biblioteca como `slowapi` para FastAPI
- [ ] Testes de rate limiting
- **Prioridade**: Alta
- **Dependências**: TASK-022
- **Status**: [ ] Não iniciado

---

## FASE 8: Testes e Garantia de Qualidade

### [TASK-040] Criar testes unitários para autenticação
- [ ] Testes de login com credenciais válidas/inválidas
- [ ] Testes de token JWT (encode/decode, expiração)
- [ ] Testes de refresh token
- [ ] Testes de RBAC e permissões
- [ ] Coverage mínimo: 90%
- **Prioridade**: Essencial
- **Dependências**: TASK-004, TASK-005, TASK-022
- **Status**: [ ] Não iniciado

### [TASK-041] Criar testes unitários para funcionalidades de jornada
- [ ] Testes de reconstrução cronológica com dados simulados
- [ ] Testes de identificação de recorrências
- [ ] Testes de cálculo de intervalos de tempo
- [ ] Testes de identificação de gargalos
- [ ] Coverage mínimo: 90%
- **Prioridade**: Essencial
- **Dependências**: TASK-013, TASK-014, TASK-015, TASK-016
- **Status**: [ ] Não iniciado

### [TASK-042] Criar testes de integração para endpoints
- [ ] Testes de todos os endpoints `GET /api/pacientes*`
- [ ] Testes de autenticação requerida
- [ ] Testes de RBAC (diferentes roles)
- [ ] Testes de validação de input/output contra schemas
- [ ] Testes de paginação e filtros
- [ ] Coverage mínimo: 80%
- **Prioridade**: Essencial
- **Dependências**: TASK-017, TASK-018, TASK-019, TASK-020
- **Status**: [ ] Não iniciado

### [TASK-043] Criar testes de performance
- [ ] Teste de resposta em tempo real (< 10 segundos por requisição)
- [ ] Teste de carga: 100 requisições simultâneas
- [ ] Análise de queries lentas (use EXPLAIN PLAN)
- [ ] Otimização de índices se necessário
- **Prioridade**: Alta
- **Dependências**: TASK-017, TASK-018, TASK-019, TASK-020
- **Status**: [ ] Não iniciado
- **Referência**: `CARE-RNF003`

### [TASK-044] Criar testes de segurança
- [ ] Testes de SQL injection
- [ ] Testes de XSS/CSRF
- [ ] Testes de autenticação bypass
- [ ] Testes de acesso não autorizado
- [ ] Validação de headers de segurança
- [ ] Linting de segurança (bandit, safety)
- **Prioridade**: Essencial
- **Dependências**: TASK-037, TASK-038, TASK-039
- **Status**: [ ] Não iniciado

### [TASK-045] Criar testes de conformidade LGPD
- [ ] Verificar ausência de PII em logs
- [ ] Verificar ausência de PII em respostas de API
- [ ] Testes de auditoria de acesso
- [ ] Testes de soft delete
- **Prioridade**: Essencial
- **Dependências**: TASK-035, TASK-036
- **Status**: [ ] Não iniciado

### [TASK-046] Gerar relatório de cobertura de testes
- [ ] Usar `pytest-cov` para Python
- [ ] Usar `vitest` ou `jest` para TypeScript/Vue
- [ ] Meta: 85% de cobertura no backend, 80% no frontend
- [ ] Documentar áreas com baixa cobertura
- **Prioridade**: Alta
- **Dependências**: TASK-040, TASK-041, TASK-042, TASK-043, TASK-044
- **Status**: [ ] Não iniciado

---

## FASE 9: Ingestão de Dados e ETL

### [TASK-047] Implementar pipeline ETL para Pacientes
- [ ] Ler `data/pacientes.csv`
- [ ] Validar contra JSON Schema
- [ ] Transformar em entidades `Paciente`
- [ ] Detectar duplicatas (CPF, CNS)
- [ ] Persistir em BD via `PacientePostgresProvider`
- [ ] Gerar relatório de ingestão (sucesso/erro/duplicatas)
- [ ] Testes com CSV de exemplo
- **Prioridade**: Essencial
- **Dependências**: TASK-008, TASK-037
- **Status**: [ ] Não iniciado

### [TASK-048] Implementar pipeline ETL para Consultas
- [ ] Ler `data/consultas.csv`
- [ ] Validar contra JSON Schema
- [ ] Relacionar com paciente via CPF/CNS
- [ ] Validar timestamps (data_hora_consulta < data_hora_fim)
- [ ] Persistir em BD
- [ ] Gerar relatório de ingestão
- [ ] Testes com CSV de exemplo
- **Prioridade**: Essencial
- **Dependências**: TASK-009, TASK-047
- **Status**: [ ] Não iniciado

### [TASK-049] Implementar pipeline ETL para Exames
- [ ] Ler `data/exames.csv`
- [ ] Validar contra JSON Schema
- [ ] Relacionar com paciente e atendimento
- [ ] Validar sequência temporal (solicitação <= realização <= liberação)
- [ ] Persistir em BD
- [ ] Gerar relatório de ingestão
- [ ] Testes com CSV de exemplo
- **Prioridade**: Essencial
- **Dependências**: TASK-010, TASK-047
- **Status**: [ ] Não iniciado

### [TASK-050] Implementar pipeline ETL para Internações
- [ ] Ler `data/internacoes.csv`
- [ ] Validar contra JSON Schema
- [ ] Relacionar com paciente e atendimento
- [ ] Calcular `tempo_permanencia_dias`
- [ ] Validar sequência temporal (dthr_inicio < dthr_fim)
- [ ] Persistir em BD
- [ ] Gerar relatório de ingestão
- [ ] Testes com CSV de exemplo
- **Prioridade**: Essencial
- **Dependências**: TASK-011, TASK-047
- **Status**: [ ] Não iniciado

### [TASK-051] Criar script de migração de dados inicial
- [ ] Script `load_initial_data.py` que executa TASK-047 a 050
- [ ] Transações atômicas (rollback em caso de erro)
- [ ] Log detalhado de cada etapa
- [ ] Documentação de como executar
- **Prioridade**: Alta
- **Dependências**: TASK-047, TASK-048, TASK-049, TASK-050
- **Status**: [ ] Não iniciado

---

## FASE 10: Integração, Documentação e Deployment

### [TASK-052] Criar documentação de API (OpenAPI/Swagger)
- [ ] Documentar todos os endpoints em OpenAPI 3.0
- [ ] Incluir schemas JSON
- [ ] Exemplos de request/response
- [ ] Documentar erros e status codes
- [ ] Gerar Swagger UI automático em `/docs`
- **Prioridade**: Alta
- **Dependências**: TASK-017, TASK-018, TASK-019, TASK-020, TASK-022
- **Status**: [ ] Não iniciado

### [TASK-053] Criar documentação de desenvolvimento
- [ ] Guia de setup local
- [ ] Instruções de como rodar testes
- [ ] Documentação de arquitetura
- [ ] Padrões de codificação
- [ ] Troubleshooting comum
- **Prioridade**: Alta
- **Dependências**: Nenhuma
- **Status**: [ ] Não iniciado

### [TASK-054] Criar Dockerfile e docker-compose.yml
- [ ] Dockerfile para backend (Python/FastAPI)
- [ ] Dockerfile para frontend (Vue)
- [ ] docker-compose.yml com postgres, backend, frontend
- [ ] Variáveis de ambiente para containers
- [ ] Documentação de como build e run
- **Prioridade**: Alta
- **Dependências**: Nenhuma
- **Status**: [ ] Não iniciado

### [TASK-055] Configurar CI/CD pipeline
- [ ] GitHub Actions para testes automatizados
- [ ] Linting (pylint, eslint)
- [ ] Cobertura de testes
- [ ] Build de images Docker
- [ ] Deploy automático (se houver ambiente)
- **Prioridade**: Alta
- **Dependências**: TASK-040, TASK-041, TASK-042
- **Status**: [ ] Não iniciado

### [TASK-056] Validar conformidade com Checklist de Guardrails
- [ ] ✓ Seguir rigorosamente o Modelo de Dados (TASK-001)
- [ ] ✓ Implementar testes unitários (TASK-040, 041, 042)
- [ ] ✓ Utilizar criptografia AES-256 (TASK-034)
- [ ] ✓ Colunas explícitas de ingestão respeitadas (TASK-047-050)
- [ ] ✓ Sem dependências externas não documentadas (TASK-052)
- [ ] ✓ Usar Soft Delete (TASK-036)
- [ ] ✓ RBAC não burlarável (TASK-006)
- [ ] ✓ LDAP/AD opcional para dev (TASK-005)
- [ ] ✓ Cobertura 100% em rotas de autenticação
- [ ] ✓ Zero vulnerabilidades críticas (TASK-044)
- **Prioridade**: Essencial
- **Dependências**: Todas as tasks anteriores
- **Status**: [ ] Não iniciado

### [TASK-057] Deployment em ambiente de staging
- [ ] Setup de servidor staging (ou VM local)
- [ ] Deploy de backend + frontend + BD
- [ ] Testes de integração completa em staging
- [ ] Validação de performance em staging
- [ ] Documentação de processo de deployment
- **Prioridade**: Alta
- **Dependências**: TASK-054, TASK-055
- **Status**: [ ] Não iniciado

### [TASK-058] Deployment em ambiente de produção (HC)
- [ ] Plano de migração de dados
- [ ] Backup estratégia
- [ ] Monitoramento e alertas
- [ ] Documentação de operations
- [ ] Plano de rollback
- **Prioridade**: Baixa (pós-MVP)
- **Dependências**: TASK-057
- **Status**: [ ] Não iniciado

---

## RESUMO E MÉTRICAS

### Estatísticas
- **Total de Tasks**: 58
- **Fases**: 10
- **Prioridades**: Essencial (32), Alta (20), Baixa (6)

### Dependências Críticas (Path Crítico)
```
TASK-001 (BD) 
  ↓
TASK-002 (Auditoria)
  ↓
TASK-003 (Env/Segurança)
  ↓
TASK-004 (JWT)
  ↓
TASK-022 (Login API)
  ↓
TASK-026 (Login Frontend)
  ↓
TASK-008 (Providers Pacientes)
  ↓
TASK-009, 010, 011 (Providers Consulta/Exame/Internação)
  ↓
TASK-013 (Reconstrução Jornada)
  ↓
TASK-019 (Jornada API)
  ↓
TASK-029 (Detalhe Paciente Frontend)
```

### Critérios de Conclusão do Projeto
- [ ] Todas as 58 tasks marcadas como concluídas
- [ ] Testes com coverage mínimo de 85% (backend), 80% (frontend)
- [ ] Zero vulnerabilidades críticas de segurança
- [ ] Conformidade 100% com SPEC.md e SDD
- [ ] Documentação completa
- [ ] Deployment bem-sucedido em staging
- [ ] Validação com usuários finais (HC)

---

## Notas Importantes

1. **Sequência de Execução**: Seguir a ordem das fases garante que dependências sejam respeitadas.
2. **Guardrails**: Consultar `06-arquitetura.md` para anti-patterns proibidos.
3. **Validação de Schemas**: Todo dado deve ser validado contra JSON Schema antes de persistência.
4. **PII Protection**: Nunca persistir dados sensíveis brutos; armazenar apenas métricas derivadas.
5. **Soft Delete**: Usar `deleted_at` em vez de DELETE SQL.
6. **Logs Detalhados**: Registrar todas as operações críticas em `AUDIT_LOG`.
7. **Performance**: Alvo: respostas < 10 segundos; otimizar índices conforme necessário.

