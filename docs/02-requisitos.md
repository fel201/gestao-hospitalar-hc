# Especificação de Requisitos

## 1. Requisitos Funcionais (RF)
| ID | Título | Descrição | Prioridade |
| :--- | :--- | :--- | :--- |
| RF001 | Autenticação | Autenticação básica com JWT e fallback mock; LDAP/AD opcional quando disponível. | Baixa |
| RF002 | Visualização da linha do tempo de um paciente | Exibição da jornada em formato cronológico | Média |
| RF002 | Visualização de eventos da jornada do paciente | Exibição geral dos eventos por etapa | Essencial |
| RF003 | Criação de indicadores e gráficos de cada etapa | Implementação de estatísticas dos eventos | Essencial |
| RF004 | Armazenamento do Dashboard | Persistir apenas métricas derivadas e metadados. | Alta |

## 2. Requisitos Não Funcionais (RNF)
| ID | Categoria | Descrição |
| :--- | :--- | :--- |
| RNF001 | LGPD | Auditoria de acesso a dados sensíveis. |
| RNF002 | Latência baixa | Resposta em tempo real. |
| RNF003 | Escalabilidade | Dados em JSON. |
| RNF004 | Disponibilidade | Sistema operando 24 horas por dia. |
| RNF005 | Usabilidade | Sistema intuitivo e padronizado. |
| RNF006 | Privacidade | Não persistir PII; armazenar somente métricas derivadas e identificadores pseudonimizados. |

Sim. O detalhamento CARE está desatualizado em relação aos requisitos funcionais e não funcionais do início do documento. Abaixo está uma versão consistente, mantendo um CARE para cada requisito listado.

---

# 3. Detalhamento SDD (CARE)

## [CARE-RF001] Autenticação

* **Context (Contexto):** A aplicação deve permitir acesso apenas a usuários autorizados, funcionando tanto em ambiente de desenvolvimento quanto em produção.
* **Action (Ação):** Implementar autenticação baseada em JWT, utilizando autenticação mock em desenvolvimento e LDAP/Active Directory quando configurado.
* **Result (Resultado):** Usuários autenticados recebem um token JWT válido para acessar os endpoints protegidos.
* **Evaluation (Avaliação):** Validar geração e expiração do token, funcionamento do login mock e autenticação via AD quando configurada.

---

## [CARE-RF002] Visualização da linha do tempo de um paciente

* **Context (Contexto):** Os eventos clínicos do paciente são obtidos a partir dos dados disponibilizados pelo AGHU.
* **Action (Ação):** Disponibilizar um endpoint que reconstrua cronologicamente a jornada de um paciente a partir do seu prontuário.
* **Result (Resultado):** O usuário visualiza toda a linha do tempo do paciente em ordem cronológica.
* **Evaluation (Avaliação):** Validar a ordenação dos eventos, a consistência das informações retornadas e o tratamento de prontuários inexistentes.

---

## [CARE-RF003] Criação de indicadores e gráficos de cada etapa

* **Context (Contexto):** Os eventos da jornada já foram reconstruídos e classificados por etapa assistencial.
* **Action (Ação):** Calcular indicadores estatísticos e gerar os dados necessários para gráficos de desempenho de cada etapa.
* **Result (Resultado):** O dashboard apresenta indicadores, métricas e gráficos atualizados conforme os filtros selecionados.
* **Evaluation (Avaliação):** Comparar os valores calculados com consultas de referência e validar a renderização correta dos gráficos.

---

## [CARE-RF004] Armazenamento do Dashboard

* **Context (Contexto):** Os indicadores são calculados a partir dos dados operacionais do hospital.
* **Action (Ação):** Persistir apenas métricas derivadas, filtros utilizados e metadados necessários para reprocessamento do dashboard, sem armazenar dados pessoais dos pacientes.
* **Result (Resultado):** O dashboard pode ser reconstruído rapidamente utilizando métricas previamente armazenadas.
* **Evaluation (Avaliação):** Verificar que nenhuma informação identificável do paciente é persistida e que os dashboards são recuperados corretamente.

---

## [CARE-RNF001] LGPD

* **Context (Contexto):** O sistema recebe informações provenientes de prontuários hospitalares.
* **Action (Ação):** Implementar mecanismos de auditoria de acesso e garantir que apenas informações estritamente necessárias sejam utilizadas.
* **Result (Resultado):** O tratamento dos dados atende aos princípios da LGPD e permite rastrear acessos realizados.
* **Evaluation (Avaliação):** Executar auditorias de acesso e verificar conformidade com as políticas de privacidade adotadas.

---

## [CARE-RNF002] Latência baixa

* **Context (Contexto):** O dashboard é utilizado durante atividades assistenciais e administrativas.
* **Action (Ação):** Otimizar consultas, processamento e carregamento dos indicadores para minimizar o tempo de resposta.
* **Result (Resultado):** As consultas são respondidas em tempo adequado para uso interativo.
* **Evaluation (Avaliação):** Realizar testes de desempenho garantindo tempos de resposta inferiores ao limite estabelecido.

---

## [CARE-RNF003] Escalabilidade

* **Context (Contexto):** O volume de dados clínicos cresce continuamente conforme novos registros são adicionados.
* **Action (Ação):** Padronizar a comunicação utilizando JSON e estruturar a aplicação para suportar grandes volumes de dados e futuras integrações.
* **Result (Resultado):** O sistema mantém desempenho satisfatório mesmo com aumento significativo da base de dados.
* **Evaluation (Avaliação):** Executar testes de carga e verificar a estabilidade da aplicação em diferentes volumes de dados.

---

## [CARE-RNF004] Disponibilidade

* **Context (Contexto):** O sistema deve estar disponível para utilização contínua pelos profissionais do hospital.
* **Action (Ação):** Implementar mecanismos de monitoramento, tratamento de falhas e recuperação de serviços.
* **Result (Resultado):** A aplicação permanece disponível durante a operação diária do hospital.
* **Evaluation (Avaliação):** Monitorar indicadores de disponibilidade e realizar testes de recuperação após falhas simuladas.

---

## [CARE-RNF005] Usabilidade

* **Context (Contexto):** O sistema será utilizado por profissionais de saúde com diferentes níveis de familiaridade com tecnologia.
* **Action (Ação):** Desenvolver interfaces intuitivas, padronizadas e com navegação simplificada.
* **Result (Resultado):** Os usuários conseguem localizar informações e executar tarefas com facilidade.
* **Evaluation (Avaliação):** Aplicar testes de usabilidade com usuários do Hospital das Clínicas e coletar métricas de satisfação e tempo de execução das tarefas.

---

## [CARE-RNF006] Privacidade

* **Context (Contexto):** Os indicadores do dashboard são produzidos a partir de informações clínicas sensíveis.
* **Action (Ação):** Evitar o armazenamento de informações pessoais identificáveis (PII), persistindo apenas métricas agregadas e identificadores pseudonimizados quando necessários.
* **Result (Resultado):** O armazenamento do sistema reduz o risco de exposição de dados sensíveis.
* **Evaluation (Avaliação):** Auditar a base persistida para confirmar a ausência de PII e validar o uso correto de técnicas de pseudonimização.
