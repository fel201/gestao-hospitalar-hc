export interface MetricaDoc {
  titulo: string;
  modulo: string;
  calculo: string;
  observacoes: string;
}

export const METRICAS_DOCS: Record<string, MetricaDoc> = {
  "Tempo médio da data de cadastro até o primeiro evento": {
    titulo: "Tempo médio da data de cadastro até o primeiro evento",
    modulo: "Entrada",
    calculo: "Compara a data de cadastro do paciente com a data do primeiro evento assistencial registrado, como consulta, exame, internação ou cirurgia. Esse cálculo mostra o tempo médio que o paciente aguarda até ser efetivamente atendido ou encaminhado para um fluxo de cuidado.",
    observacoes: "É um indicador de eficiência do acesso inicial. Valores altos podem indicar gargalos na regulação, demora no agendamento ou falhas na transição do cadastro para o atendimento."
  },

  "Taxa de prontuários inertes": {
    titulo: "Taxa de prontuários inertes",
    modulo: "Entrada",
    calculo: "Identifica pacientes cadastrados que nunca tiveram um evento assistencial vinculado ao seu prontuário. O cálculo gera a proporção de cadastros que não evoluíram para uma ação clínica, administrativa ou de acompanhamento.",
    observacoes: "Esse indicador ajuda a avaliar a qualidade do cadastro e o uso efetivo do sistema. Uma taxa alta pode indicar cadastros feitos apenas para registro administrativo ou pacientes que não chegaram a iniciar a jornada assistencial."
  },

  "Intervalo médio entre consultas": {
    titulo: "Intervalo médio entre consultas",
    modulo: "Consultas",
    calculo: "Mede o tempo entre a consulta regulada e o primeiro retorno, ou entre retornos sucessivos quando houver continuidade do acompanhamento. O cálculo apresenta o ritmo com que o cuidado é mantido ao longo da jornada do paciente.",
    observacoes: "Valores maiores do que o esperado podem sinalizar perda de continuidade assistencial, dificuldades de agendamento de retorno ou interrupção do tratamento. Esse indicador é importante para avaliar a manutenção do cuidado e a adesão ao plano terapêutico."
  },

  "Porcentagem global dos tipos de consultas": {
    titulo: "Gráfico comparativo das porcentagens globais dos tipos de consultas",
    modulo: "Consultas",
    calculo: "Agrupa todas as consultas registradas por tipo — como regulada, retorno, interconsulta, sessão ou pronto-atendimento — e calcula a participação de cada categoria no total. O cálculo aponta o perfil predominante do atendimento ambulatorial.",
    observacoes: "Permite visualizar se o serviço está mais focado em entrada de novos casos ou na continuidade de tratamentos já em curso. Também ajuda a identificar mudanças na natureza da demanda e a necessidade de ajustar recursos ou rotinas."
  },

  "Tempo medio global entre a criação de prontuário e o primeiro agendamento": {
    titulo: "Tempo médio entre a criação do prontuário e o primeiro agendamento",
    modulo: "Consultas",
    calculo: "Calcula o intervalo entre o cadastro do paciente e a primeira consulta registrada. O resultado reflete o tempo que o paciente demora para obter o primeiro acesso ambulatorial após o cadastro.",
    observacoes: "Esse indicador aponta a eficiência do fluxo inicial de atendimento. Um aumento pode indicar lentidão no agendamento, falta de vagas ou atraso na regulação, o que impacta negativamente a experiência do paciente e a agilidade do serviço."
  },

  "Tempo médio de agendamento até realização (horas)": {
    titulo: "Tempo médio entre o agendamento e a realização da consulta",
    modulo: "Consultas",
    calculo: "Mede, em horas, o tempo entre o momento em que a consulta regulada foi agendada e o momento em que ela foi efetivamente realizada. O cálculo explica quanto tempo o paciente espera entre a marcação e a execução do atendimento.",
    observacoes: "É um indicador direto da fila de espera e da capacidade de atendimento. A elevação desse tempo aponta para excesso de demanda, agendas comprometidas ou dificuldade em manter a data agendada."
  },

  "Porcentagem global de faltas": {
    titulo: "Gráfico comparativo das porcentagens globais de faltas",
    modulo: "Consultas",
    calculo: "Calcula a proporção de consultas que terminaram em falta do paciente e a proporção de consultas em que o profissional faltou, em relação ao total de consultas registradas. O cálculo separa os dois perfis para facilitar a interpretação.",
    observacoes: "Ajuda a identificar se o absenteísmo está mais associado à demanda do paciente ou à oferta do serviço. Essa distinção orienta ações diferentes de comunicação, gerenciamento de agenda e alocação de profissionais."
  },

  "Encaminhamento global frequente por consulta regulada": {
    titulo: "Gráfico dos encaminhamentos globais após consulta regulada",
    modulo: "Consultas",
    calculo: "Analisa para onde o paciente segue após uma consulta regulada, considerando se o próximo evento é um retorno, uma interconsulta ou se não há continuidade registrada. O cálculo revela os principais desdobramentos do atendimento inicial.",
    observacoes: "O indicador mostra se a consulta regulada está gerando continuidade do cuidado ou se o paciente tende a se perder no fluxo. Muitos casos sem seguimento podem indicar fragilidade na transição entre etapas do atendimento."
  },

  "Porcentagem de exames concluídos": {
    titulo: "Porcentagem de exames concluídos",
    modulo: "Exames",
    calculo: "Divide o número de exames liberados pelo total de exames registrados na especialidade. O cálculo mostra a proporção de exames que chegaram a um desfecho efetivo dentro do fluxo de exames.",
    observacoes: "Reflete a efetividade da execução dos exames solicitados. Percentuais baixos podem indicar atrasos, cancelamentos ou falhas na operacionalização do serviço de diagnóstico."
  },

  "Porcentagem de exames regulados": {
    titulo: "Porcentagem de exames regulados",
    modulo: "Exames",
    calculo: "Calcula a parcela de exames que passou pelo processo de regulação antes de ser realizada. O cálculo destaca o peso da etapa de priorização e avaliação na especialidade.",
    observacoes: "Esse indicador revela a complexidade do fluxo de exames. Uma alta proporção de exames regulados pode demandar mais atenção de gestão na regulação e priorização dos casos."
  },

  "Porcentagem de exames marcados como pendentes": {
    titulo: "Porcentagem de exames pendentes",
    modulo: "Exames",
    calculo: "Calcula a proporção de exames que foram marcados como pendentes em relação ao total da especialidade. O cálculo identifica a parcela da demanda que não foi concluída.",
    observacoes: "Valores elevados podem indicar perda de oportunidade de cuidado, falha no agendamento, indisponibilidade de recursos ou dificuldade de acompanhamento do paciente."
  },

  "Distribuição de exames por grupo de executor": {
    titulo: "Gráfico comparativo da distribuição dos tipos de exames",
    modulo: "Exames",
    calculo: "Classifica cada exame por grupo de unidade executora, como imagem, análises clínicas, procedimento ou internação, e calcula a participação de cada grupo no total. O cálculo mostra a composição do volume de exames dentro da especialidade.",
    observacoes: "Ajuda a identificar quais tipos de setor estão mais demandados pela especialidade e a orientar a alocação de recursos entre as unidades executoras."
  },

  "Tempo médio de solicitação até a realização do exame por mês": {
    titulo: "Tempo médio entre solicitação e realização do exame",
    modulo: "Exames",
    calculo: "Agrupa os exames por mês de realização e calcula o tempo médio entre a solicitação e a realização de cada exame. O cálculo permite acompanhar a evolução do tempo de espera por mês.",
    observacoes: "Esse indicador é útil para identificar períodos com maior atraso e para monitorar se o tempo de resposta do serviço de exames está melhorando ou piorando."
  },

  "Distribuição de exames por grupo de executor (global)": {
    titulo: "Gráfico comparativo global da distribuição dos tipos de exames",
    modulo: "Exames",
    calculo: "Classifica todos os exames do hospital por grupo de unidade executora, independentemente da especialidade, e calcula a participação de cada grupo no total. O cálculo oferece uma visão institucional do fluxo de exames.",
    observacoes: "Permite comparar a demanda entre diferentes grupos executores e apoiar decisões sobre priorização de recursos e melhoria de capacidade estrutural."
  },

  "Porcentagem global de exames marcados como pendentes": {
    titulo: "Porcentagem global de exames pendentes",
    modulo: "Exames",
    calculo: "Calcula a proporção de exames não concluídos em todo o hospital em relação ao total de exames registrados. O cálculo mostra o peso dos exames pendentes no volume institucional.",
    observacoes: "Serve como alerta para problemas sistêmicos de agenda, capacidade ou adesão do paciente que afetam diferentes especialidades ao mesmo tempo."
  },

  "Porcentagem global de exames concluídos": {
    titulo: "Porcentagem global de exames concluídos",
    modulo: "Exames",
    calculo: "Divide o número de exames liberados pelo total de exames do hospital, sem filtro por especialidade. O cálculo fornece uma visão geral da efetividade do fluxo de exames institucional.",
    observacoes: "Ajuda a comparar a performance do hospital como um todo e a identificar tendências gerais de conclusão dos exames solicitados."
  },

  "Porcentagem de sumários de alta informatizados": {
    titulo: "Porcentagem de sumários de alta informatizados",
    modulo: "Internação",
    calculo: "Calcula a proporção de altas hospitalares documentadas de forma informatizada em relação ao total de altas da especialidade. O cálculo mostra o nível de adoção do registro eletrônico de alta.",
    observacoes: "Esse indicador ajuda a monitorar a digitalização do processo de alta, a rastreabilidade do cuidado e a qualidade da continuidade da informação após a internação."
  },

  "Porcentagem dos desfechos mais comuns": {
    titulo: "Gráfico comparativo dos desfechos das internações",
    modulo: "Internação",
    calculo: "Agrupa as internações concluídas por desfecho — alta, óbito, transferência ou evasão — e calcula a participação relativa de cada categoria no total. O cálculo revela o perfil dos resultados assistenciais.",
    observacoes: "Esse gráfico ajuda a identificar padrões de desfecho e a orientar ações clínicas ou administrativas em especialidades com resultados inesperados."
  },

  "Tempo médio de permanência de internação nos últimos 5 meses": {
    titulo: "Tempo médio de permanência das internações",
    modulo: "Internação",
    calculo: "Agrupa as internações concluídas por mês e calcula a permanência média em dias para cada mês. O cálculo mostra a evolução do tempo de internação ao longo de cinco meses.",
    observacoes: "Ajuda a detectar tendências de aumento ou redução no tempo de internação e a avaliar se mudanças operacionais estão impactando a duração dos internamentos."
  },

  "Tempo médio de permanência por especialidade": {
    titulo: "Tempo médio de permanência por especialidade",
    modulo: "Internação",
    calculo: "Compara o tempo médio de permanência das internações concluídas entre as diferentes especialidades. O cálculo destaca as áreas com maior uso de leitos por paciente.",
    observacoes: "Esse indicador é útil para identificar especialidades que demandam maior tempo de internação e para planejar a alocação de leitos e de equipe."
  },

  "Porcentagem de registros de pacientes internados por especialidade clínica": {
    titulo: "Gráfico comparativo das internações por especialidade",
    modulo: "Internação",
    calculo: "Calcula a participação de cada especialidade no total de pacientes internados distintos, evitando contar um mesmo paciente mais de uma vez. O cálculo mostra a demanda real por paciente único em cada área.",
    observacoes: "Importante para entender onde está concentrada a demanda de pacientes internados e para comparar a carga assistencial entre especialidades de forma mais fiel."
  },

  "Especialidades com maior percentual de internações": {
    titulo: "Gráfico das especialidades com maior percentual de internações",
    modulo: "Internação",
    calculo: "Ordena as especialidades pelo volume de internações e calcula a participação de cada uma no total. O cálculo evidencia as áreas com maior concentração de leitos ocupados.",
    observacoes: "Permite identificar quais especialidades estão responsável pela maior parte das internações e orientar decisões sobre distribuição de leitos e recursos."
  },

  "Porcentagem geral dos desfechos mais comuns": {
    titulo: "Gráfico comparativo global dos desfechos das internações",
    modulo: "Internação",
    calculo: "Aplica a mesma classificação de desfecho usada por especialidade, mas considerando todas as internações do hospital. O cálculo oferece uma visão institucional dos resultados assistenciais.",
    observacoes: "Ajuda a ter uma referência geral do perfil de desfechos e a comparar o desempenho assistencial entre diferentes áreas e níveis do hospital."
  },

  "Tempo médio global de permanência de internação nos últimos 5 meses": {
    titulo: "Tempo médio global de permanência das internações",
    modulo: "Internação",
    calculo: "Calcula a permanência média hospitalar ao longo dos últimos cinco meses, considerando todas as especialidades. O cálculo gera uma referência global de duração de internação.",
    observacoes: "Ajuda a avaliar o nível de ocupação e a evolução do tempo médio de internação em escala institucional, servindo como parâmetro para gestão de capacidade."
  },

  "Tempo médio de cirurgia": {
    titulo: "Tempo médio de cirurgia",
    modulo: "Cirurgia",
    calculo: "Calcula a média da duração das cirurgias realizadas na especialidade, excluindo procedimentos cancelados. O cálculo mostra o tempo típico de uso da sala cirúrgica por procedimento.",
    observacoes: "Ajuda a avaliar a complexidade da atividade cirúrgica e a planejar melhor a ocupação do centro cirúrgico, a alocação de turnos e a previsão de tempo por caso."
  },

  "Porcentagem de cirurgias concluídas": {
    titulo: "Porcentagem de cirurgias concluídas",
    modulo: "Cirurgia",
    calculo: "Calcula a proporção de cirurgias efetivamente realizadas em relação ao total de cirurgias registradas na especialidade. O cálculo permite avaliar o sucesso do agendamento e da execução cirúrgica.",
    observacoes: "Esse indicador é útil para monitorar cancelamentos, reprogramações e o grau de execução do plano cirúrgico. Valores baixos podem indicar problemas de disponibilidade, insumos ou preparo pré-operatório."
  },

  "Porcentagem global de cirurgias concluidas": {
    titulo: "Porcentagem global de cirurgias concluídas",
    modulo: "Cirurgia",
    calculo: "Aplica o mesmo cálculo de conclusão, mas considerando todos os procedimentos cirúrgicos do hospital. O resultado oferece uma visão institucional da taxa de execução cirúrgica.",
    observacoes: "Permite comparar o desempenho cirúrgico do hospital como um todo e identificar áreas de melhoria relacionadas à programação e à capacidade operacional."
  },

  "Tempo médio de cirurgia por especialidade": {
    titulo: "Tempo médio de cirurgia por especialidade",
    modulo: "Cirurgia",
    calculo: "Compara o tempo médio de duração das cirurgias entre especialidades. O cálculo destaca onde os procedimentos tendem a ser mais longos e, possivelmente, mais complexos.",
    observacoes: "Esse indicador ajuda a orientar a gestão do centro cirúrgico, a alocação de equipes e a previsão de capacidade, especialmente em especialidades com maior tempo médio de procedimento."
  },

  "Cirurgias por especialidade": {
    titulo: "Gráfico comparativo das cirurgias por especialidade",
    modulo: "Cirurgia",
    calculo: "Mostra o volume de cirurgias realizadas por especialidade e calcula a participação relativa no total. O cálculo evidencia as áreas de maior atividade cirúrgica.",
    observacoes: "Permite identificar quais especialidades concentram o maior volume de procedimentos e apoiar decisões sobre distribuição de salas, equipe e recursos."
  },

  "Porcentagem global de cirurgias por origem": {
    titulo: "Gráfico comparativo global das origens das cirurgias",
    modulo: "Cirurgia",
    calculo: "Classifica as cirurgias por origem — internação ou ambulatório — e calcula a participação de cada categoria no total. O cálculo mostra de onde vêm os casos cirúrgicos.",
    observacoes: "Ajuda a entender o perfil do fluxo cirúrgico e a integração entre serviços de internação e ambulatório, o que é importante para planejamento de leitos e prioridades."
  },
};
