# Especificação de Requisitos

## 1. Requisitos Funcionais (RF)
| ID | Título | Descrição | Prioridade |
| :--- | :--- | :--- | :--- |
| RF001 | Autenticação | Login via LDAP/AD do hospital. | Essencial |
| RF002 | Cadastro | Registro de pacientes com CNS/CPF. | Essencial |
| RF003 | Reconstrução Cronológica | Registro da linha do tempo do paciente. | Essencial |
| RF004 | Visualização da Jornada | Exibição da jornada em formato cronológico | Essencial |
| RF005 | Visualização de Eventos | Exibição mais detalhada de um certo evento | Essencial |
| RF006 | Identificação de recorrências | Identificação de certos padrões em pacientes | Essencial |
| RF007 | Cálculo do tempo entre eventos | Registro do tempo levado por cada evento | Essencial |
| RF008 | Identificação de Gargalos | Detecção de irregularidades nos eventos | Essencial |

## 2. Requisitos Não Funcionais (RNF)
| ID | Categoria | Descrição |
| :--- | :--- | :--- |
| RNF001 | Segurança | Criptografia AES-256. |
| RNF002 | LGPD | Auditoria de acesso a dados sensíveis. |
| RNF003 | Desempenho | Resposta em tempo real. |
| RNF004 | Modelo de Dados | Dados em JSON. |
| RNF005 | Disponibilidade | Sistema operando 24 horas por dia. |
| RNF006 | Usabilidade | Sistema intuitivo e padronizado. |
| RNF007 | Portabilidade | Sistema portável para as tecnologias usadas no HC. |

## 3. Detalhamento SDD (CARE)
Para cada requisito, a implementação deve seguir o padrão:

### [CARE-RF001] Autenticação LDAP
* **Context (Contexto)**: Servidor LDAP configurado e credenciais de serviço disponíveis.
* **Action (Ação)**: Criar middleware de autenticação que consulte o AD.
* **Result (Resultado)**: Token JWT gerado após sucesso; Código 401 em falha.
* **Evaluation (Avaliação)**: Executar `npm test tests/auth.spec.ts` (deve passar com 100% de sucesso).

### [CARE-RF002] Cadastro de Pacientes
* **Context (Contexto)**: Esquema de banco de dados 'PACIENTE' criado.
* **Action (Ação)**: Criar endpoint POST `/api/pacientes` com validação de CPF e CNS.
* **Result (Resultado)**: Registro persistido no banco; Log de auditoria criado.
* **Evaluation (Avaliação)**: Validar contra JSON Schema definido em `04-modelo-dados.md`.

### [CARE-RF003] Reconstrução Cronológica
* **Context (Contexto)**: Eventos clínicos armazenados com timestamps válidos.
* **Action (Ação)**: Reconstruir automaticamente a jornada do paciente ordenando os eventos cronologicamente.
* **Result (Resultado)**: Linha do tempo organizada desde a entrada até o desfecho clínico.
* **Evaluation (Avaliação)**: Validaar ordenação correta dos eventos utilizando diferentes cenários de jornada.

### [CARE-RF004] Visualização da Jornada
* **Context (Contexto)**: Jornada do paciente previamente reconstruída..
* **Action (Ação)**: Exibir a trajetória do paciente em formato visual cronológico.
* **Result (Resultado)**: Usuário consegue visualizar eventos da jornada em sequência temporal.
* **Evaluation (Avaliação)**: Validação da renderização correta da timeline e carregamento dos eventos.

### [CARE-RF005] Visualização de Eventos
* **Context (Contexto)**: Evento existente dentro da jornada do paciente.
* **Action (Ação)**: Permitir visualização detalhada de um evento selecionado.
* **Result (Resultado)**: Sistema exibe informações complementares como data, horário, unidade, etc do evento.
* **Evaluation (Avaliação)**: Validar exibição completa das informações do evento selecionado.

### [CARE-RF006] Identificação de Recorrências
* **Context (Contexto)**: Histórico clínico do paciente disponível no sistema.
* **Action (Ação)**: Analisar jornadas em busca de padrões recorrentes.
* **Result (Resultado)**: Sistema identifica esses padrões e os exibe para avaliação.
* **Evaluation (Avaliação)**: Executar consultas de pacientes recorrentes e validar padrões identificados.

### [CARE-RF007] Cálculo do Tempo entre Eventos
* **Context (Contexto)**: Eventos registrados com timestamps consistentes.
* **Action (Ação)**: Calcular automaticamente o tempo entre eventos consecutivos da jornada.
* **Result (Resultado)**: Sistema apresenta métricas de: tempo de espera, permanência, duração de internação.
* **Evaluation (Avaliação)**: Validar cálculos utilizando jornadas com intervalos conhecidos.

### [CARE-RF008] Identificação de Gargalos
* **Context (Contexto)**: Dados históricos de jornadas disponíveis para análise.
* **Action (Ação)**: Analisar fluxos assistenciais em busca de gargalos operacionais.
* **Result (Resultado)**: Sistema identifica etapas com maior atraso.
* **Evaluation (Avaliação)**: Validar identificação correta dos gargalos em cenários simulados e históricos reais.

### [CARE-RNF001] Segurança
* **Context (Contexto)**: Criptografia dos dados trafegados.
* **Action (Ação)**: Aplicar a AES-256.
* **Result (Resultado)**: Dado é codificado entre os endpoints.
* **Evaluation (Avaliação)**: Verificar se os dados estão corretamente criptogrados.

### [CARE-RNF002] LGPD
* **Context (Contexto)**: Proteção e bom uso dos dados de pacientes.
* **Action (Ação)**: Garantir que todo uso de dados seja conforme a LGPD.
* **Result (Resultado)**: Restrição do uso de dados essenciais apenas pelo sistema.
* **Evaluation (Avaliação)**: Aplicar testes de verificação de formato e uso de dados.

### [CARE-RNF003] Desempenho
* **Context (Contexto)**: Resposta em tempo hábil do sistema.
* **Action (Ação)**: Garantir respostas em 10 segundos ou menos.
* **Result (Resultado)**: Sistema ágil e viável para uso no contexto hospitalar.
* **Evaluation (Avaliação)**: Testes de estresse.

### [CARE-RNF004] Modelo de Dados 
* **Context (Contexto)**: Dados são trocados entre endpoints pelo padrão JSON.
* **Action (Ação)**: Garantir uso padronizado de JSON em toda aplicação.
* **Result (Resultado)**: Ausência de falhas de integração de dados.
* **Evaluation (Avaliação)**: Testes de formato de dados.

### [CARE-RNF005] Disponibilidade
* **Context (Contexto)**: Sistema deve estar disponível 24 horas por dia.
* **Action (Ação)**: Garantir que o sistema sempre rode sem interrupções.
* **Result (Resultado)**: Disponibilidade ideal.
* **Evaluation (Avaliação)**: Testes de estresse (simulação de picos) e monitoramento de disponibilidade.

### [CARE-RNF006] Usabilidade
* **Context (Contexto)**: Aplicação deve ser intuitiva.
* **Action (Ação)**: Tornar UI/UX simples e significativas.
* **Result (Resultado)**: Uso mais facilitado para profissionais de saúde.
* **Evaluation (Avaliação)**: Testes In loco por profissionais do HC.

### [CARE-RNF007] Portabilidade
* **Context (Contexto)**: Sistema deve rodar nos equipamentos do HC.
* **Action (Ação)**: Tornar sistema compatível com a tecnologia do AGHU, assim como dos computadores do HC.
* **Result (Resultado)**: Sistema compatível integralmente no HC.
* **Evaluation (Avaliação)**: Testes In loco e remotos.



