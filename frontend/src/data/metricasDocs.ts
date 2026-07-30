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
      calculo: "- O programa percorre todas as tabelas de eventos (consultas, exames, internações e cirurgias)\n-  Identifica, para cada prontuário, o evento com a menor data de realização, correspondente ao primeiro evento registrado para aquele paciente.\n- Em seguida, percorre a tabela de pacientes e, para cada paciente que possui um primeiro evento identificado, calcula a diferença entre a data de cadastro (utilizando o campo data_cadastro da tabela pacientes) e a data de realização desse primeiro evento.\n- A soma dessas diferenças é então dividida pela quantidade de pacientes que possuem ao menos um evento registrado, obtendo-se o tempo médio entre o cadastro do paciente e seu primeiro evento.",
      observacoes: ""
    },
    "Taxa de prontuários inertes": {
      titulo: "Taxa de prontuários inertes",
      modulo: "Entrada",
      calculo: "São identificados todos os prontuários que possuem pelo menos um evento registrado nas tabelas de consultas, exames, internações ou cirurgias. Em seguida, cada paciente é comparado com esse conjunto de prontuários. Os pacientes cujo prontuário não possui nenhum evento registrado são classificados como inertes. Por fim, a quantidade de prontuários inertes é dividida pelo total de pacientes cadastrados, obtendo-se a taxa de prontuários inertes.",
      observacoes: "Se caso os eventos e a lista de prontuários forem carregados pelos CSVs, haverá uma porcentagem muito alta desse indicador pois não há uma grande quantidade de eventos armazenados nos CSVs em comparação com a lista de pacientes, devido a limitações de espaço."
    },
    "Porcentagem dos tipos de consultas": {
      titulo: "Gráfico comparativo das porcentagens dos tipos de consultas",
      modulo: "Consultas",
      calculo: "Na tabela de consultas tem o campo \"Condição de Atendimento\", que podem ter campos como \"CONSULTA REGULADA\", \"INTERCONSULTA\". Depois é só contabilizar cada um desses tipos de consultas e fazer uma proporção com o total de consultas.",
      observacoes: "O propósito desse gráfico consiste em avaliar o perfil da demanda da especialidade. "
    },
    "Porcentagem de faltas": {
      titulo: "Gráfico comparativo das porcentagens de faltas por parte do paciente e do profissional",
      modulo: "Consultas",
      calculo: "No campo Retorno da tabela de consultas tem dois campos importantes \"PROFISSIONAL FALTOU\" e \"PACIENTE FALTOU\". O programa simplesmente contabiliza os registros de consulta de cada situação e divide pelo total de consultas.",
      observacoes: "Esse gráfico diz muita coisa sobre a experiência do usuário no hospital. Por instância, em um caso de proporção alta de faltas por parte do paciente, o gestor assistencial pode levantar diversas perguntas como: \n- há alguma falha de comunicação no agendamento das consultas? \n- há alguma demora excessiva entre o data de agendamento e a data da consulta, que faz com que o usuário esqueça dela?"
    },
    "Encaminhamento frequente por consulta regulada": {
      titulo: "Gráfico dos encaminhamentos frequentes por consulta regulada",
      modulo: "Consultas",
      calculo: "Utilizando os campos da \"Condição do Atendimento\", a cada consulta regulada o programa procura um evento de consulta subsequente a ela fazendo uma comparação com a coluna \"Data/Hora da Consulta\".",
      observacoes: "O gráfico demonstra como os pacientes interagem com a especialidade após uma consulta regulada, permitindo uma visualização mais ampla do fluxo assistencial dos pacientes."
    },
    "Média de consultas de cada tipo por paciente": {
      titulo: "Gráfico de comparação de médias de consultas de cada tipo por paciente",
      modulo: "Consultas",
      calculo: "Divide o numero de consultas de um determinado tipo pelo total de pessoas que tiveram AO MENOS uma consulta daquele tipo, repetindo o processo para todos os tipos de consultas (reguladas, retorno e interconsultas).",
      observacoes: "Esse gráfico mostra a média de consultas de cada tipo por paciente, considerando apenas os pacientes que realizaram pelo menos uma consulta daquele tipo."
    },

};