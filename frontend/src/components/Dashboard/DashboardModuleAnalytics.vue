<template>
  <section class="mt-10 rounded-2xl border border-slate-700/80 bg-slate-800/70 p-6 shadow-2xl shadow-slate-950/30">
    <div class="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
      <div>
        <p class="text-[11px] uppercase tracking-[0.35em] text-slate-500">Fluxo assistencial</p>
        <h2 class="text-xl font-semibold text-white">Análise por módulo e subprocesso</h2>
        <p class="mt-2 max-w-2xl text-sm text-slate-400">
          Selecione um módulo e um subprocesso para visualizar indicadores que respondem às questões de gestão operacional.
        </p>
      </div>
    </div>

    <div class="mt-6 flex flex-wrap gap-2">
      <button
        v-for="module in modules"
        :key="module.id"
        class="rounded-full border px-3 py-2 text-sm font-medium transition"
        :class="activeModule === module.id
          ? 'border-blue-500 bg-blue-500/20 text-blue-200'
          : 'border-slate-700 bg-slate-900/70 text-slate-300 hover:border-slate-500 hover:text-white'"
        @click="selectModule(module.id)"
      >
        {{ module.label }}
      </button>
    </div>

    <div class="mt-6 grid gap-3 lg:grid-cols-3">
      <button
        v-for="submodule in selectedModule.submodules"
        :key="submodule.id"
        class="rounded-xl border p-4 text-left transition"
        :class="activeSubmodule === submodule.id
          ? 'border-emerald-500 bg-emerald-500/10 shadow-lg shadow-emerald-900/20'
          : 'border-slate-700 bg-slate-900/70 hover:border-slate-500'"
        @click="activeSubmodule = submodule.id"
      >
        <p class="text-sm font-semibold text-white">{{ submodule.title }}</p>
        <p class="mt-2 text-sm text-slate-400">{{ submodule.description }}</p>
      </button>
    </div>

    <div v-if="selectedSubmodule" class="mt-8 rounded-2xl border border-slate-700/70 bg-slate-900/60 p-5">
      <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <p class="text-[11px] uppercase tracking-[0.3em] text-slate-500">Subprocesso ativo</p>
          <h3 class="text-lg font-semibold text-white">{{ selectedSubmodule.title }}</h3>
          <p class="mt-1 text-sm text-slate-400">{{ selectedSubmodule.description }}</p>
        </div>
      </div>

      <div class="mt-6 grid gap-6 xl:grid-cols-2">
        <div
          v-for="chart in selectedSubmodule.charts"
          :key="chart.id"
          class="rounded-xl border border-slate-700/80 bg-slate-800/70 p-4"
        >
          <div class="flex items-start justify-between gap-2">
            <div>
              <h4 class="text-sm font-semibold text-white">{{ chart.title }}</h4>
              <p class="mt-1 text-xs text-slate-400">{{ chart.description }}</p>
            </div>
            <span class="rounded-full bg-slate-700 px-2 py-1 text-[11px] uppercase tracking-[0.25em] text-slate-300">
              {{ chart.typeLabel }}
            </span>
          </div>

          <div class="mt-4 h-56">
            <component :is="chartComponent(chart.type)" :data="buildChartData(chart)" :options="buildChartOptions(chart)" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { Bar, Doughnut, Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Title
} from 'chart.js';

ChartJS.register(BarElement, CategoryScale, LinearScale, ArcElement, PointElement, LineElement, Tooltip, Legend, Title);

type ChartSpec = {
  id: string;
  title: string;
  description: string;
  type: string;
  typeLabel: string;
  labels: string[];
  values: number[];
  backgroundColor?: string[];
  borderColor?: string[];
  unit?: string;
};

type SubmoduleSpec = {
  id: string;
  title: string;
  description: string;
  metric: string;
  insights: string[];
  charts: ChartSpec[];
};

type ModuleSpec = {
  id: string;
  label: string;
  submodules: SubmoduleSpec[];
};

const modules: ModuleSpec[] = [
  {
    id: 'entrada',
    label: 'Entrada',
    submodules: [
      {
        id: 'entrada-criar-prontuario',
        title: 'Criação de prontuário',
        description: 'Indicadores de abertura e cuidado inicial.',
        metric: 'Tempo médio até o primeiro evento: 32 min',
        insights: [
          'Em média, quanto tempo os pacientes aguardam entre o cadastro e o primeiro evento assistencial?',
          'Qual a taxa de prontuários inertes sem evento subsequente?'
        ],
        charts: [
          {
            id: 'tempo-entrada',
            title: 'Tempo até o primeiro evento',
            description: 'Distribuição do intervalo entre cadastro e primeiro contato assistencial.',
            type: 'bar',
            typeLabel: 'Barra',
            labels: ['< 15 min', '15–30 min', '30–60 min', '> 60 min'],
            values: [24, 36, 22, 18],
            backgroundColor: ['rgba(59, 130, 246, 0.7)', 'rgba(16, 185, 129, 0.7)', 'rgba(245, 158, 11, 0.7)', 'rgba(239, 68, 68, 0.7)']
          },
          {
            id: 'inercia-entrada',
            title: 'Prontuários inertes',
            description: 'Percentual de prontuários sem evento assistencial subsequente.',
            type: 'doughnut',
            typeLabel: 'Rosca',
            labels: ['Com evolução', 'Inertes'],
            values: [82, 18],
            backgroundColor: ['rgba(16, 185, 129, 0.8)', 'rgba(239, 68, 68, 0.8)']
          }
        ]
      }
    ]
  },
  {
    id: 'consultas',
    label: 'Consultas',
    submodules: [
      {
        id: 'consultas-reguladas',
        title: 'Realização de consulta regulada',
        description: 'Visão da demanda regulada e seus desfechos.',
        metric: 'Proporção regulada: 42%',
        insights: [
          'Qual a proporção de consultas reguladas em relação ao total?',
          'Quais encaminhamentos são mais frequentes após a consulta regulada?'
        ],
        charts: [
          {
            id: 'proporcao-consultas',
            title: 'Distribuição de consultas',
            description: 'Comparativo entre consultas reguladas e não reguladas.',
            type: 'doughnut',
            typeLabel: 'Rosca',
            labels: ['Reguladas', 'Não reguladas'],
            values: [42, 58],
            backgroundColor: ['rgba(59, 130, 246, 0.8)', 'rgba(100, 116, 139, 0.8)']
          },
          {
            id: 'desfechos-consultas',
            title: 'Desfechos subsequentes',
            description: 'Probabilidade de exame, retorno, internação e cirurgia após consulta regulada.',
            type: 'bar',
            typeLabel: 'Barra',
            labels: ['Exame', 'Retorno', 'Internação', 'Cirurgia'],
            values: [32, 27, 11, 4],
            backgroundColor: ['rgba(59, 130, 246, 0.7)', 'rgba(16, 185, 129, 0.7)', 'rgba(245, 158, 11, 0.7)', 'rgba(236, 72, 153, 0.7)']
          }
        ]
      },
      {
        id: 'consultas-retorno',
        title: 'Realização de consulta de retorno',
        description: 'Perfil de retornos e intervalo entre consultas.',
        metric: 'Retornos por paciente: 1,8',
        insights: [
          'Quantas consultas de retorno, em média, são geradas por paciente?',
          'Qual o intervalo médio entre retorno e retorno?'
        ],
        charts: [
          {
            id: 'retornos-por-paciente',
            title: 'Retornos por paciente',
            description: 'Média de consultas de retorno por paciente no período.',
            type: 'bar',
            typeLabel: 'Barra',
            labels: ['1', '2', '3+'],
            values: [44, 31, 25],
            backgroundColor: ['rgba(16, 185, 129, 0.7)', 'rgba(59, 130, 246, 0.7)', 'rgba(245, 158, 11, 0.7)']
          },
          {
            id: 'intervalo-retornos',
            title: 'Intervalo entre consultas',
            description: 'Tempo médio entre a primeira consulta regulada e o primeiro retorno.',
            type: 'line',
            typeLabel: 'Linha',
            labels: ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4'],
            values: [12, 10, 14, 11],
            backgroundColor: ['rgba(59, 130, 246, 0.3)']
          }
        ]
      },
      {
        id: 'consultas-triagem',
        title: 'Realização de triagem de interconsulta',
        description: 'Fluxo de triagem e geração de interconsultas.',
        metric: 'Triagem efetiva: 61%',
        insights: [
          'Qual a proporção de pacientes que passam por triagem de interconsulta?',
          'Qual a proporção das triagens que geram interconsulta?'
        ],
        charts: [
          {
            id: 'triagem-pacientes',
            title: 'Pacientes com triagem',
            description: 'Participação de pacientes que passaram pela triagem de interconsulta.',
            type: 'doughnut',
            typeLabel: 'Rosca',
            labels: ['Com triagem', 'Sem triagem'],
            values: [61, 39],
            backgroundColor: ['rgba(59, 130, 246, 0.8)', 'rgba(100, 116, 139, 0.8)']
          },
          {
            id: 'triagem-conversao',
            title: 'Conversão em interconsulta',
            description: 'Percentual das triagens que efetivamente geraram interconsulta.',
            type: 'bar',
            typeLabel: 'Barra',
            labels: ['Sim', 'Não'],
            values: [61, 39],
            backgroundColor: ['rgba(16, 185, 129, 0.7)', 'rgba(239, 68, 68, 0.7)']
          }
        ]
      },
      {
        id: 'consultas-interconsulta',
        title: 'Realização de interconsulta',
        description: 'Participação de interconsultas na jornada.',
        metric: 'Interconsultas: 18% do total',
        insights: [
          'Qual a proporção de interconsultas em relação ao total?',
          'Qual a proporção dos pacientes que passam por interconsultas?'
        ],
        charts: [
          {
            id: 'participacao-interconsulta',
            title: 'Participação das interconsultas',
            description: 'Peso das interconsultas no total de consultas.',
            type: 'doughnut',
            typeLabel: 'Rosca',
            labels: ['Interconsulta', 'Outras'],
            values: [18, 82],
            backgroundColor: ['rgba(236, 72, 153, 0.8)', 'rgba(100, 116, 139, 0.8)']
          },
          {
            id: 'pacientes-interconsulta',
            title: 'Pacientes com interconsulta',
            description: 'Proporção de pacientes que tiveram pelo menos uma interconsulta.',
            type: 'bar',
            typeLabel: 'Barra',
            labels: ['Sim', 'Não'],
            values: [27, 73],
            backgroundColor: ['rgba(59, 130, 246, 0.7)', 'rgba(148, 163, 184, 0.7)']
          }
        ]
      }
    ]
  },
  {
    id: 'exames',
    label: 'Exames',
    submodules: [
      {
        id: 'exames-regulados',
        title: 'Realização de exames regulados',
        description: 'Perfil dos exames regulados.',
        metric: 'Exames regulados: 31% do total',
        insights: [
          'Qual a proporção de exames regulados em relação ao total de exames?',
          'Quais tipos de exames mais predominam dentro dos regulados?'
        ],
        charts: [
          {
            id: 'proporcao-exames-regulados',
            title: 'Participação dos exames regulados',
            description: 'Comparativo entre exames regulados e demais exames.',
            type: 'doughnut',
            typeLabel: 'Rosca',
            labels: ['Regulados', 'Outros'],
            values: [31, 69],
            backgroundColor: ['rgba(16, 185, 129, 0.8)', 'rgba(100, 116, 139, 0.8)']
          },
          {
            id: 'tipos-exames-regulados',
            title: 'Tipos mais frequentes',
            description: 'Tipos de exame mais comuns no fluxo regulado.',
            type: 'bar',
            typeLabel: 'Barra',
            labels: ['Tomografia', 'Hemograma', 'Ultrassom', 'Ecocardiograma'],
            values: [18, 24, 15, 12],
            backgroundColor: ['rgba(59, 130, 246, 0.7)', 'rgba(16, 185, 129, 0.7)', 'rgba(245, 158, 11, 0.7)', 'rgba(236, 72, 153, 0.7)']
          }
        ]
      },
      {
        id: 'exames-ambulatorial',
        title: 'Solicitação ambulatorial de exames',
        description: 'Análise de exames ambulatoriais e gargalos.',
        metric: 'Média por paciente: 2,4 exames',
        insights: [
          'Qual o volume médio de exames ambulatoriais por paciente?',
          'Quais exames são gargalos recorrentes?'
        ],
        charts: [
          {
            id: 'volume-ambulatorial',
            title: 'Volume por paciente',
            description: 'Média de exames ambulatoriais por paciente.',
            type: 'bar',
            typeLabel: 'Barra',
            labels: ['1', '2', '3+'],
            values: [33, 41, 26],
            backgroundColor: ['rgba(59, 130, 246, 0.7)', 'rgba(16, 185, 129, 0.7)', 'rgba(245, 158, 11, 0.7)']
          },
          {
            id: 'gargalos-ambulatorial',
            title: 'Gargalos recorrentes',
            description: 'Exames com maior tempo de espera e atraso.',
            type: 'line',
            typeLabel: 'Linha',
            labels: ['MRI', 'Tomografia', 'Lab', 'Ecocardiograma'],
            values: [14, 11, 9, 7],
            backgroundColor: ['rgba(239, 68, 68, 0.3)']
          }
        ]
      }
    ]
  },
  {
    id: 'internacao',
    label: 'Internação',
    submodules: [
      {
        id: 'internacao-regular',
        title: 'Realização de internação',
        description: 'Métricas de internação clínica e regulada.',
        metric: 'Tempo médio de internação: 5,4 dias',
        insights: [
          'Qual a proporção de pacientes internados por especialidade clínica?',
          'Qual o tempo médio entre solicitação e internação?'
        ],
        charts: [
          {
            id: 'internacao-especialidades',
            title: 'Internações por especialidade',
            description: 'Participação das principais especialidades clínicas.',
            type: 'bar',
            typeLabel: 'Barra',
            labels: ['Cardiologia', 'Oncologia', 'Pneumologia', 'Neurologia'],
            values: [28, 24, 19, 15],
            backgroundColor: ['rgba(59, 130, 246, 0.7)', 'rgba(16, 185, 129, 0.7)', 'rgba(245, 158, 11, 0.7)', 'rgba(236, 72, 153, 0.7)']
          },
          {
            id: 'internacao-tipo',
            title: 'Tipo de internação',
            description: 'Comparativo entre internações ambulatoriais e reguladas.',
            type: 'doughnut',
            typeLabel: 'Rosca',
            labels: ['Regulada', 'Ambulatorial'],
            values: [63, 37],
            backgroundColor: ['rgba(59, 130, 246, 0.8)', 'rgba(100, 116, 139, 0.8)']
          }
        ]
      },
      {
        id: 'internacao-pre-operatoria',
        title: 'Realização de internação pré-operatória',
        description: 'Participação da internação pré-operatória.',
        metric: 'Pré-operatória: 19% das internações',
        insights: [
          'Qual a proporção de pacientes internados para pré-operatório?',
          'Quais as proporções de internações cirúrgicas em relação ao todo?'
        ],
        charts: [
          {
            id: 'pre-op-participacao',
            title: 'Participação pré-operatória',
            description: 'Peso das internações pré-operatórias no conjunto.',
            type: 'doughnut',
            typeLabel: 'Rosca',
            labels: ['Pré-operatória', 'Outros'],
            values: [19, 81],
            backgroundColor: ['rgba(245, 158, 11, 0.8)', 'rgba(100, 116, 139, 0.8)']
          },
          {
            id: 'pre-op-cirurgicas',
            title: 'Internações cirúrgicas',
            description: 'Comparativo entre internações cirúrgicas e clínicas.',
            type: 'bar',
            typeLabel: 'Barra',
            labels: ['Cirúrgica', 'Clínica'],
            values: [19, 81],
            backgroundColor: ['rgba(236, 72, 153, 0.7)', 'rgba(59, 130, 246, 0.7)']
          }
        ]
      }
    ]
  },
  {
    id: 'cirurgia',
    label: 'Cirurgia',
    submodules: [
      {
        id: 'cirurgia-lec',
        title: 'Inserção de paciente na LEC',
        description: 'Volume e permanência na lista de espera cirúrgica.',
        metric: 'Pacientes na LEC: 184',
        insights: [
          'Quantos pacientes são inseridos na LEC em um determinado período?',
          'Qual o tempo médio de permanência do paciente na LEC?'
        ],
        charts: [
          {
            id: 'lec-especialidades',
            title: 'Pacientes por especialidade',
            description: 'Distribuição de pacientes na LEC por especialidade cirúrgica.',
            type: 'bar',
            typeLabel: 'Barra',
            labels: ['Ortopedia', 'Ginecologia', 'Urologia', 'Cirurgia Geral'],
            values: [42, 29, 21, 18],
            backgroundColor: ['rgba(59, 130, 246, 0.7)', 'rgba(16, 185, 129, 0.7)', 'rgba(245, 158, 11, 0.7)', 'rgba(236, 72, 153, 0.7)']
          },
          {
            id: 'lec-permanencia',
            title: 'Permanência na LEC',
            description: 'Tempo médio de permanência do paciente na lista.',
            type: 'line',
            typeLabel: 'Linha',
            labels: ['Jan', 'Fev', 'Mar', 'Abr'],
            values: [34, 31, 29, 27],
            backgroundColor: ['rgba(59, 130, 246, 0.3)']
          }
        ]
      },
      {
        id: 'cirurgia-realizada',
        title: 'Realização de cirurgia',
        description: 'Proporção de pacientes operados por especialidade.',
        metric: 'Cirurgias realizadas: 67%',
        insights: [
          'Qual a proporção de pacientes que passam por cirurgia?',
          'Qual o tempo médio de cirurgia por especialidade cirúrgica?'
        ],
        charts: [
          {
            id: 'cirurgias-especialidades',
            title: 'Proporção por especialidade',
            description: 'Participação das cirurgias nas principais especialidades.',
            type: 'doughnut',
            typeLabel: 'Rosca',
            labels: ['Ortopedia', 'Ginecologia', 'Urologia', 'Cirurgia Geral'],
            values: [31, 24, 21, 24],
            backgroundColor: ['rgba(59, 130, 246, 0.8)', 'rgba(16, 185, 129, 0.8)', 'rgba(245, 158, 11, 0.8)', 'rgba(236, 72, 153, 0.8)']
          },
          {
            id: 'tempo-cirurgia',
            title: 'Tempo médio de cirurgia',
            description: 'Tempo médio por procedimento cirúrgico.',
            type: 'bar',
            typeLabel: 'Barra',
            labels: ['Ortopedia', 'Ginecologia', 'Urologia', 'Cirurgia Geral'],
            values: [95, 72, 58, 84],
            backgroundColor: ['rgba(59, 130, 246, 0.7)', 'rgba(16, 185, 129, 0.7)', 'rgba(245, 158, 11, 0.7)', 'rgba(236, 72, 153, 0.7)']
          }
        ]
      }
    ]
  }
];

const activeModule = ref('entrada');
const activeSubmodule = ref('entrada-criar-prontuario');

const selectedModule = computed(() => modules.find((module) => module.id === activeModule.value) ?? modules[0]);
const selectedSubmodule = computed(() => selectedModule.value.submodules.find((submodule) => submodule.id === activeSubmodule.value) ?? selectedModule.value.submodules[0]);

const selectModule = (moduleId: string) => {
  activeModule.value = moduleId;
  const nextModule = modules.find((module) => module.id === moduleId) ?? modules[0];
  activeSubmodule.value = nextModule.submodules[0]?.id ?? '';
};

const chartComponent = (type: string) => {
  if (type === 'doughnut') return Doughnut;
  if (type === 'line') return Line;
  return Bar;
};

const buildChartData = (chart: ChartSpec) => {
  const common = {
    labels: chart.labels,
    datasets: [
      {
        label: chart.title,
        data: chart.values,
        backgroundColor: chart.backgroundColor ?? ['rgba(59, 130, 246, 0.7)'],
        borderColor: chart.borderColor ?? ['rgba(255, 255, 255, 0.8)'],
        borderWidth: 1
      }
    ]
  };

  if (chart.type === 'doughnut') {
    return {
      labels: chart.labels,
      datasets: [
        {
          data: chart.values,
          backgroundColor: chart.backgroundColor ?? ['rgba(59, 130, 246, 0.8)', 'rgba(100, 116, 139, 0.8)'],
          borderColor: '#0f172a',
          borderWidth: 2
        }
      ]
    };
  }

  if (chart.type === 'line') {
    return {
      labels: chart.labels,
      datasets: [
        {
          label: chart.title,
          data: chart.values,
          fill: true,
          borderColor: '#38bdf8',
          backgroundColor: 'rgba(56, 189, 248, 0.16)',
          tension: 0.35,
          pointRadius: 4,
          pointHoverRadius: 5
        }
      ]
    };
  }

  return common;
};

const buildChartOptions = (chart: ChartSpec) => {
  const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#cbd5e1'
        }
      },
      tooltip: {
        enabled: true
      }
    },
    scales: {
      x: {
        ticks: {
          color: '#94a3b8'
        },
        grid: {
          color: 'rgba(148, 163, 184, 0.15)'
        }
      },
      y: {
        beginAtZero: true,
        ticks: {
          color: '#94a3b8'
        },
        grid: {
          color: 'rgba(148, 163, 184, 0.15)'
        }
      }
    }
  };

  if (chart.type === 'doughnut') {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom' as const,
          labels: {
            color: '#cbd5e1'
          }
        }
      }
    };
  }

  return baseOptions;
};
</script>
