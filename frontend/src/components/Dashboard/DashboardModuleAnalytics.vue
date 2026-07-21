<template>
  <section
    class="mt-10 rounded-2xl border border-slate-700/80 bg-slate-800/70 p-6 shadow-2xl shadow-slate-950/30"
  >
    <div
      class="flex flex-col gap-3 md:flex-row md:items-end md:justify-between"
    >
      <div>
        <p class="text-[11px] uppercase tracking-[0.35em] text-slate-500">
          Fluxo assistencial
        </p>
        <h2 class="text-xl font-semibold text-white">
          Análise por módulo e subprocesso
        </h2>
        <p class="mt-2 max-w-2xl text-sm text-slate-400">
          Selecione um módulo e um subprocesso para visualizar os gráficos
          correspondentes.
        </p>
      </div>
    </div>

    <div class="mt-6 flex flex-wrap gap-2">
      <button
        v-for="modulo in MODULOS"
        :key="modulo.id"
        class="rounded-full border px-3 py-2 text-sm font-medium transition"
        :class="
          activeModulo === modulo.id
            ? 'border-blue-500 bg-blue-500/20 text-blue-200'
            : 'border-slate-700 bg-slate-900/70 text-slate-300 hover:border-slate-500 hover:text-white'
        "
        @click="selecionarModulo(modulo.id)"
      >
        {{ modulo.label }}
      </button>
    </div>

    <div v-if="moduloSelecionado" class="mt-6 grid gap-3 lg:grid-cols-3">
      <button
        v-for="sub in moduloSelecionado.submodulos"
        :key="sub.id"
        class="rounded-xl border p-4 text-left transition"
        :class="
          activeSubmodulo === sub.id
            ? 'border-emerald-500 bg-emerald-500/10 shadow-lg shadow-emerald-900/20'
            : 'border-slate-700 bg-slate-900/70 hover:border-slate-500'
        "
        @click="activeSubmodulo = sub.id"
      >
        <p class="text-sm font-semibold text-white">{{ sub.titulo }}</p>
        <p class="mt-2 text-sm text-slate-400">{{ sub.descricao }}</p>
      </button>
    </div>

    <div
      v-if="submoduloSelecionado"
      class="mt-8 rounded-2xl border border-slate-700/70 bg-slate-900/60 p-5"
    >
      <div
        class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between"
      >
        <div>
          <p class="text-[11px] uppercase tracking-[0.3em] text-slate-500">
            Subprocesso ativo
          </p>
          <h3 class="text-lg font-semibold text-white">
            {{ submoduloSelecionado.titulo }}
          </h3>
          <p class="mt-1 text-sm text-slate-400">
            {{ submoduloSelecionado.descricao }}
          </p>
        </div>
      </div>

      <div class="mt-6 grid gap-6 xl:grid-cols-2">
        <div
          v-for="item in graficosResolvidos"
          :key="item.spec.id"
          class="rounded-xl border border-slate-700/80 bg-slate-800/70 p-4"
          :class="{ 'xl:col-span-2': item.spec.tipo === 'distribuicao' }"
        >
          <div class="flex items-start justify-between gap-2">
            <h4 class="text-sm font-semibold text-white">
              {{ item.spec.titulo }}
            </h4>
            <span
              class="rounded-full bg-slate-700 px-2 py-1 text-[11px] uppercase tracking-[0.25em] text-slate-300"
            >
              {{ rotuloTipo(item.spec.tipo) }}
            </span>
          </div>

          <!-- Gráfico ainda não implementado no backend, ou faltam indicadores -->
          <div
            v-if="item.indisponivel"
            class="mt-4 flex h-40 items-center justify-center rounded-lg border border-dashed border-slate-700 bg-slate-900/40 p-4 text-center"
          >
            <p class="text-xs text-slate-500">
              Ainda não disponível no backend{{
                item.faltando.length ? ": " + item.faltando.join(", ") : ""
              }}.
            </p>
          </div>

          <!-- Comparação de proporções (2-4 categorias em %) -->
          <div
            v-else-if="item.spec.tipo === 'comparacao-proporcao'"
            class="mt-4 h-56"
          >
            <Bar
              :data="buildComparacaoProporcaoData(item)"
              :options="chartOptionsComparacaoProporcao"
              :plugins="[ChartDataLabels]"
            />
          </div>

          <!-- Comparação de valores em dias/horas (mesma unidade) -->
          <div
            v-else-if="item.spec.tipo === 'comparacao-dias'"
            class="mt-4 h-56"
          >
            <Bar
              :data="buildComparacaoValorData(item)"
              :options="chartOptionsComparacaoValor(item.spec.unidade)"
              :plugins="[ChartDataLabels]"
            />
          </div>

          <!-- Comparação mista: unidades diferentes -> dois cards de estatística lado a lado -->
          <div
            v-else-if="item.spec.tipo === 'comparacao-mista'"
            class="mt-4 grid h-40 grid-cols-2 gap-3"
          >
            <div
              v-for="ind in item.indicadores"
              :key="ind.nome"
              class="flex flex-col items-center justify-center rounded-lg bg-slate-900/50 p-3 text-center"
            >
              <span class="text-2xl font-bold text-white">{{
                formatarValor(ind.valor)
              }}</span>
              <span class="mt-1 text-xs text-slate-400">{{
                rotuloIndicador(item.spec, ind.nome)
              }}</span>
            </div>
          </div>

          <!-- Distribuição (dict {categoria: contagem}) -> gráfico de barras horizontal -->
          <div
            v-else-if="item.spec.tipo === 'distribuicao'"
            class="mt-4"
            :style="{
              height: alturaBarraDistribuicao(item.indicadores[0]) + 'px',
            }"
          >
            <Bar
              :data="buildDistribuicaoData(item.indicadores[0])"
              :options="buildDistribuicaoOptions(item.indicadores[0])"
              :plugins="[ChartDataLabels]"
            />
          </div>

          <!-- Valor simples (número, string, dias, horas etc) -->
          <div v-else class="mt-4 flex h-40 items-center justify-center">
            <p class="text-3xl font-bold text-white">
              {{ formatarValor(item.indicadores[0]?.valor) }}
            </p>
          </div>
        </div>

        <div
          v-if="graficosResolvidos.length === 0"
          class="col-span-full text-sm text-slate-400"
        >
          Nenhum gráfico configurado para este subprocesso ainda.
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";
import type { DashboardInterface } from "../../interfaces/dashboard";

// Registrado globalmente para que Tooltip/Legend continuem funcionando,
// mas cada <Bar> também recebe o plugin explicitamente via :plugins="[ChartDataLabels]"
// (necessário no vue-chartjs para habilitar os rótulos por gráfico).
ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

// -------------------------------------------------------------------------
// Tipos
// -------------------------------------------------------------------------

// Formato real de distribuição vindo do backend: dict ordenado por contagem
// desc, ex.: encaminhamentos_por_consulta_regulada -> {"RETORNO": 12, "SEM SEGUIMENTO": 5, ...}
type IndicadorDistribuicao = Record<string, number>;

type Indicador = {
  nome: string;
  valor: number | string | IndicadorDistribuicao;
};

type TipoGrafico =
  | "comparacao-proporcao" // N indicadores em % lado a lado (0-100), pode incluir "Outros" residual
  | "comparacao-dias" // N indicadores numéricos na mesma unidade (dias/horas)
  | "comparacao-mista" // 2 indicadores com unidades diferentes -> cards lado a lado
  | "distribuicao" // 1 indicador cujo valor é um dict {categoria: contagem}
  | "valor-simples"; // 1 indicador numérico/textual isolado

type GraficoSpec = {
  id: string;
  titulo: string;
  tipo: TipoGrafico;
  indicadorNomes: string[];
  incluirOutros?: boolean;
  unidade?: string;
  // NOVO: mapa opcional "nome real do indicador" -> "rótulo exibido no gráfico"
  rotulos?: Record<string, string>;
};

type SubmoduloSpec = {
  id: string;
  titulo: string;
  descricao: string;
  graficos: GraficoSpec[];
};

type ModuloSpec = {
  id: string;
  label: string;
  dataKey: keyof Pick<
    DashboardInterface,
    "entrada" | "consultas" | "exames" | "internacao" | "cirurgias"
  >;
  submodulos: SubmoduloSpec[];
};

// -------------------------------------------------------------------------
// Props
// -------------------------------------------------------------------------

const props = defineProps<{
  dashboard: DashboardInterface;
}>();

// -------------------------------------------------------------------------
// Estrutura de módulos/subprocessos/gráficos, seguindo o documento de
// especificação e o mapeamento confirmado indicador-a-indicador.
// -------------------------------------------------------------------------
const rotuloIndicador = (spec: GraficoSpec, nomeReal: string): string =>
  spec.rotulos?.[nomeReal] ?? nomeReal;

const MODULOS: ModuloSpec[] = [
  {
    id: "entrada",
    label: "Entrada",
    dataKey: "entrada",
    submodulos: [
      {
        id: "entrada-prontuario",
        titulo: "Criação de prontuário",
        descricao:
          "Tempo até o primeiro evento assistencial e prontuários inertes.",
        graficos: [
          {
            id: "entrada-tempo-primeiro-evento",
            titulo:
              "Tempo médio entre cadastro e o primeiro evento assistencial",
            tipo: "valor-simples",
            indicadorNomes: [
              "Tempo médio da data de cadastro até o primeiro evento",
            ],
          },
          {
            id: "entrada-prontuarios-inertes",
            titulo: "Taxa de prontuários inertes (sem evento subsequente)",
            tipo: "valor-simples",
            indicadorNomes: ["Taxa de prontuários inertes"],
          },
        ],
      },
    ],
  },
  {
    id: "consultas",
    label: "Consultas",
    dataKey: "consultas",
    submodulos: [
      {
        id: "consultas-realizacao",
        titulo: "Realização de consultas",
        descricao:
          "Reguladas, retornos e interconsultas: proporções, encaminhamentos, faltas e intervalos.",
        graficos: [
          {
            id: "consultas-proporcao-tipos",
            titulo:
              "Proporção de consultas reguladas, de retorno e interconsultas",
            tipo: "comparacao-proporcao",
            indicadorNomes: [
              "Porcentagem de consultas reguladas",
              "Porcentagem de consultas de retorno",
              "Porcentagem de interconsultas",
            ],
            incluirOutros: true,
            rotulos: {
              "Porcentagem de consultas reguladas": "Reguladas",
              "Porcentagem de consultas de retorno": "Retornos",
              "Porcentagem de interconsultas": "Interconsultas",
            },
          },
          {
            id: "consultas-encaminhamentos",
            titulo: "Encaminhamentos mais frequentes após consulta regulada",
            tipo: "distribuicao",
            indicadorNomes: ["Encaminhamento frequente por consulta regulada"],
          },
          {
            id: "consultas-faltas",
            titulo: "Faltas: pacientes x profissionais",
            tipo: "comparacao-proporcao",
            indicadorNomes: [
              "Porcentagem de faltas por parte do profissional",
              "Porcentagem de faltas por parte do paciente",
            ],
          },
          {
            id: "consultas-tempo-prontuario-agendamento",
            titulo:
              "Tempo médio entre a criação do prontuário e o agendamento da consulta",
            tipo: "valor-simples",
            indicadorNomes: [
              "Tempo medio entre a criação de prontuário e o primeiro agendamento",
            ], // ainda não existe no backend
            unidade: "horas",
          },
          {
            id: "consultas-tempo-agendamento-realizacao",
            titulo: "Tempo médio entre agendamento e realização da consulta",
            tipo: "valor-simples",
            indicadorNomes: [
              "Tempo médio de agendamento até realização (horas)",
            ],
          },
          {
            id: "consultas-retorno-interconsulta-paciente",
            titulo: "Comparação de consultas por pacientes",
            tipo: "comparacao-dias",
            indicadorNomes: [
              "Consultas reguladas por paciente",
              "Consultas retorno por paciente",
              "Interconsultas por paciente",
            ],
          },
          {
            id: "consultas-intervalo-retornos",
            titulo: "Intervalo: REGULADA → 1º RETORNO X RETORNO → RETORNO",
            tipo: "comparacao-dias",
            indicadorNomes: [
              "Intervalo médio da consulta regulada ao primeiro retorno",
              "Intervalo médio de retornos consecutivos",
            ],
            unidade: "dias",
          },
        ],
      },
    ],
  },
  {
    id: "exames",
    label: "Exames",
    dataKey: "exames",
    submodulos: [
      {
        id: "exames-ambulatoriais",
        titulo: "Exames Ambulatoriais",
        descricao:
          "Proporção, volume por paciente, tempos e gargalos dos exames ambulatoriais.",
        graficos: [
          {
            id: "exames-amb-proporcao",
            titulo: "Proporção de exames ambulatoriais em relação ao total",
            tipo: "valor-simples",
            indicadorNomes: ["Porcentagem de exames ambulatoriais"],
          },
          {
            id: "exames-amb-volume",
            titulo: "Concentração de Exames Ambulatoriais por paciente ativo",
            tipo: "valor-simples",
            indicadorNomes: ["Concentração de Exames Ambulatoriais por paciente ativo"],
          },
          {
            id: "exames-amb-tempo-agendamento",
            titulo: "Tempo médio entre solicitação e agendamento",
            tipo: "valor-simples",
            indicadorNomes: [],
          },
          {
            id: "exames-amb-tempo-realizacao",
            titulo: "Tempo médio entre agendamento e realização",
            tipo: "valor-simples",
            indicadorNomes: [],
          },
          {
            id: "exames-amb-gargalos",
            titulo: "Exames que são gargalos recorrentes",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
        ],
      },
      {
        id: "exames-hospitalares",
        titulo: "Exames Hospitalares",
        descricao:
          "Proporção, tipos predominantes, tempos e gargalos dos exames na internação.",
        graficos: [
          {
            id: "exames-hosp-proporcao",
            titulo: "Proporção de exames de internação em relação ao total",
            tipo: "valor-simples",
            indicadorNomes: [],
          },
          {
            id: "exames-hosp-tipos",
            titulo: "Tipos de exame mais predominantes na internação",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
          {
            id: "exames-hosp-volume",
            titulo: "Volume médio de exames por paciente internado",
            tipo: "valor-simples",
            indicadorNomes: [],
          },
          {
            id: "exames-hosp-tempo-agendamento",
            titulo: "Tempo médio entre solicitação e agendamento",
            tipo: "valor-simples",
            indicadorNomes: [],
          },
          {
            id: "exames-hosp-tempo-realizacao",
            titulo: "Tempo médio entre agendamento e realização",
            tipo: "valor-simples",
            indicadorNomes: [],
          },
          {
            id: "exames-hosp-gargalos",
            titulo: "Exames que são gargalos recorrentes",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
        ],
      },
      {
        id: "exames-pre-operatorios",
        titulo: "Exames Pré-operatórios",
        descricao:
          "Proporção, tipos predominantes, tempos e gargalos dos exames pré-operatórios.",
        graficos: [
          {
            id: "exames-pre-proporcao",
            titulo: "Proporção de exames pré-operatórios em relação ao total",
            tipo: "valor-simples",
            indicadorNomes: [],
          },
          {
            id: "exames-pre-tipos",
            titulo: "Tipos de exame mais predominantes no pré-operatório",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
          {
            id: "exames-pre-tempo-agendamento",
            titulo: "Tempo médio entre solicitação e agendamento",
            tipo: "valor-simples",
            indicadorNomes: [],
          },
          {
            id: "exames-pre-tempo-realizacao",
            titulo: "Tempo médio entre agendamento e realização",
            tipo: "valor-simples",
            indicadorNomes: [],
          },
          {
            id: "exames-pre-gargalos",
            titulo: "Exames que são gargalos recorrentes",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
        ],
      },
      {
        id: "exames-comparacao",
        titulo: "Comparação entre os três",
        descricao:
          "Ambulatoriais x Hospitalares x Pré-operatórios lado a lado.",
        graficos: [
          {
            id: "exames-cmp-proporcao",
            titulo: "Comparação de proporção por natureza de exame",
            tipo: "comparacao-proporcao",
            indicadorNomes: [],
          },
          {
            id: "exames-cmp-tipos",
            titulo: "Comparação de tipos mais predominantes",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
          {
            id: "exames-cmp-tempo-agendamento",
            titulo: "Comparação de tempo até agendamento",
            tipo: "comparacao-dias",
            indicadorNomes: [],
            unidade: "horas",
          },
          {
            id: "exames-cmp-tempo-realizacao",
            titulo: "Comparação de tempo até realização",
            tipo: "comparacao-dias",
            indicadorNomes: [],
            unidade: "horas",
          },
          {
            id: "exames-cmp-gargalos",
            titulo: "Comparação de gargalos recorrentes",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
        ],
      },
    ],
  },
  {
    id: "internacao",
    label: "Internação",
    dataKey: "internacao",
    submodulos: [
      {
        id: "internacao-realizacao",
        titulo: "Realização de Internação",
        descricao:
          "Por especialidade clínica, tempo médio e proporção ambulatorial x regulada.",
        graficos: [
          {
            id: "internacao-especialidade",
            titulo:
              "Proporção de pacientes internados por especialidade clínica",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
          {
            id: "internacao-tempo-especialidade",
            titulo: "Tempo médio de internação por especialidade clínica",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
          {
            id: "internacao-tipo-solicitacao",
            titulo: "Ambulatorial x regulada em relação ao total",
            tipo: "comparacao-proporcao",
            indicadorNomes: [],
          },
          {
            id: "internacao-tempo-solicitacao",
            titulo: "Tempo médio entre solicitação e internação",
            tipo: "valor-simples",
            indicadorNomes: ["Tempo médio de permanência (dias)"],
          },
        ],
      },
      {
        id: "internacao-pre-operatoria",
        titulo: "Internação Pré-operatória",
        descricao:
          "Proporção por especialidade cirúrgica e participação no total de internações.",
        graficos: [
          {
            id: "internacao-pre-especialidade",
            titulo:
              "Proporção de internados para pré-operatório por especialidade cirúrgica",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
          {
            id: "internacao-pre-participacao",
            titulo: "Participação da pré-operatória no total de internações",
            tipo: "comparacao-proporcao",
            indicadorNomes: [],
            incluirOutros: true,
          },
        ],
      },
      {
        id: "internacao-pos-operatoria",
        titulo: "Internação Pós-operatória",
        descricao:
          "Proporção em UTI por especialidade e tempo médio de internação pós-operatória.",
        graficos: [
          {
            id: "internacao-pos-uti",
            titulo:
              "Proporção internada em UTI no pós-operatório por especialidade",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
          {
            id: "internacao-pos-tempo",
            titulo:
              "Tempo médio de internação pós-operatória por especialidade",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
        ],
      },
      {
        id: "internacao-comparacao",
        titulo: "Comparação entre os três tipos",
        descricao: "Regular x pré-operatória x pós-operatória lado a lado.",
        graficos: [
          {
            id: "internacao-cmp-proporcao",
            titulo: "Comparação da proporção de internados em cada tipo",
            tipo: "comparacao-proporcao",
            indicadorNomes: [],
          },
          {
            id: "internacao-cmp-tempo",
            titulo: "Comparação do tempo médio de internação de cada tipo",
            tipo: "comparacao-dias",
            indicadorNomes: [],
            unidade: "dias",
          },
          {
            id: "internacao-cmp-participacao",
            titulo: "Comparação da proporção de internações de cada tipo",
            tipo: "comparacao-proporcao",
            indicadorNomes: [],
          },
        ],
      },
    ],
  },
  {
    id: "cirurgia",
    label: "Cirurgia",
    dataKey: "cirurgias",
    submodulos: [
      {
        id: "cirurgia-realizacao",
        titulo: "Realização de cirurgia",
        descricao:
          "Proporção de pacientes operados e tempo médio de cirurgia por especialidade.",
        graficos: [
          {
            id: "cirurgia-proporcao-especialidade",
            titulo:
              "Proporção de pacientes que passam por cirurgia, por especialidade",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
          {
            id: "cirurgia-tempo-especialidade",
            titulo: "Tempo médio de cirurgia por especialidade",
            tipo: "distribuicao",
            indicadorNomes: [],
          },
        ],
      },
    ],
  },
];

// -------------------------------------------------------------------------
// Seleção de módulo/subprocesso
// -------------------------------------------------------------------------

const activeModulo = ref(MODULOS[0].id);
const activeSubmodulo = ref(MODULOS[0].submodulos[0].id);

const moduloSelecionado = computed(
  () => MODULOS.find((m) => m.id === activeModulo.value) ?? MODULOS[0],
);

const submoduloSelecionado = computed(
  () =>
    moduloSelecionado.value.submodulos.find(
      (s) => s.id === activeSubmodulo.value,
    ) ?? moduloSelecionado.value.submodulos[0],
);

const selecionarModulo = (moduloId: string) => {
  activeModulo.value = moduloId;
  const novoModulo = MODULOS.find((m) => m.id === moduloId) ?? MODULOS[0];
  activeSubmodulo.value = novoModulo.submodulos[0]?.id ?? "";
};

// -------------------------------------------------------------------------
// Normalização dos indicadores do bloco do backend correspondente ao módulo
// -------------------------------------------------------------------------

const indicadoresDoBloco = computed<Indicador[]>(() => {
  const modulo = moduloSelecionado.value;
  const bloco = props.dashboard?.[modulo.dataKey];
  const brutos = (bloco?.indicadores ?? []) as unknown[];

  const normalizados: Indicador[] = [];
  for (const item of brutos) {
    if (
      item &&
      typeof item === "object" &&
      "nome" in (item as any) &&
      "valor" in (item as any)
    ) {
      normalizados.push(item as Indicador);
    } else {
      console.warn(
        "Indicador fora do formato {nome, valor} recebido do backend:",
        item,
      );
    }
  }
  return normalizados;
});

// -------------------------------------------------------------------------
// Resolução: cada gráfico da spec busca seus indicadores pelo "nome" exato
// -------------------------------------------------------------------------

type GraficoResolvido = {
  spec: GraficoSpec;
  indicadores: Indicador[];
  faltando: string[];
  indisponivel: boolean;
};

const graficosResolvidos = computed<GraficoResolvido[]>(() => {
  const lista = indicadoresDoBloco.value;
  const sub = submoduloSelecionado.value;
  if (!sub) return [];

  return sub.graficos.map((spec) => {
    const indicadores: Indicador[] = [];
    const faltando: string[] = [];
    for (const nome of spec.indicadorNomes) {
      const encontrado = lista.find((i) => i.nome === nome);
      if (encontrado) indicadores.push(encontrado);
      else faltando.push(nome);
    }
    const indisponivel =
      spec.indicadorNomes.length === 0 || faltando.length > 0;
    return { spec, indicadores, faltando, indisponivel };
  });
});

// -------------------------------------------------------------------------
// Helpers de formatação/render
// -------------------------------------------------------------------------

const PALETA = [
  "rgba(59, 130, 246, 0.85)",
  "rgba(16, 185, 129, 0.85)",
  "rgba(245, 158, 11, 0.85)",
  "rgba(236, 72, 153, 0.85)",
  "rgba(139, 92, 246, 0.85)",
  "rgba(148, 163, 184, 0.6)", // "Outros" costuma vir por último -> cinza neutro
];

const rotuloTipo = (tipo: TipoGrafico) => {
  switch (tipo) {
    case "comparacao-proporcao":
      return "Comparação";
    case "comparacao-dias":
      return "Comparação";
    case "comparacao-mista":
      return "Comparação";
    case "distribuicao":
      return "Distribuição";
    default:
      return "Valor";
  }
};

const numeroDoValor = (valor: number | string): number => {
  if (typeof valor === "number") return valor;
  const limpo = valor.replace("%", "").replace(",", ".").trim();
  const n = parseFloat(limpo);
  return Number.isNaN(n) ? 0 : n;
};

const formatarValor = (valor: Indicador["valor"] | undefined): string => {
  if (valor === undefined) return "—";
  if (typeof valor === "object") return "";
  return String(valor);
};

// Configuração base do datalabels, reaproveitada em todos os gráficos de barra.
// Texto sempre visível, sem precisar passar o mouse por cima.
const DATALABELS_BASE = {
  color: "#f8fafc",
  font: { weight: "bold" as const, size: 12 },
  textStrokeColor: "rgba(15, 23, 42, 0.55)",
  textStrokeWidth: 3,
};

// --- comparação de proporções (0-100%), com "Outros" residual opcional ---

const buildComparacaoProporcaoData = (item: GraficoResolvido) => {
  const labels = item.indicadores.map((i) =>
    rotuloIndicador(item.spec, i.nome),
  );
  const valores = item.indicadores.map((i) =>
    numeroDoValor(i.valor as number | string),
  );

  if (item.spec.incluirOutros) {
    const soma = valores.reduce((a, b) => a + b, 0);
    labels.push("Outros");
    valores.push(Math.max(0, 100 - soma));
  }

  return {
    labels,
    datasets: [
      {
        data: valores,
        backgroundColor: labels.map((_, i) => PALETA[i % PALETA.length]),
        borderColor: "#0f172a",
        borderWidth: 1,
        borderRadius: 6,
        maxBarThickness: 64,
      },
    ],
  };
};

const chartOptionsComparacaoProporcao = {
  responsive: true,
  maintainAspectRatio: false,
  layout: { padding: { top: 24 } },
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: { label: (ctx: any) => `${ctx.raw}%` },
    },
    datalabels: {
      ...DATALABELS_BASE,
      anchor: "end" as const,
      align: "end" as const,
      formatter: (value: number) => `${value}%`,
    },
  },
  scales: {
    x: { ticks: { color: "#cbd5e1" }, grid: { display: false } },
    y: {
      beginAtZero: true,
      max: 100,
      ticks: { color: "#94a3b8", callback: (v: string | number) => `${v}%` },
      grid: { color: "rgba(148, 163, 184, 0.15)" },
    },
  },
};

// --- comparação de valores na mesma unidade (dias/horas) ---

const buildComparacaoValorData = (item: GraficoResolvido) => ({
  labels: item.indicadores.map((i) => rotuloIndicador(item.spec, i.nome)),
  datasets: [
    {
      data: item.indicadores.map((i) =>
        numeroDoValor(i.valor as number | string),
      ),
      backgroundColor: item.indicadores.map(
        (_, i) => PALETA[i % PALETA.length],
      ),
      borderColor: "#0f172a",
      borderWidth: 1,
      borderRadius: 6,
      maxBarThickness: 64,
    },
  ],
});

const chartOptionsComparacaoValor = (unidade?: string) => ({
  responsive: true,
  maintainAspectRatio: false,
  layout: { padding: { top: 24 } },
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx: any) => `${ctx.raw}${unidade ? " " + unidade : ""}`,
      },
    },
    datalabels: {
      ...DATALABELS_BASE,
      anchor: "end" as const,
      align: "end" as const,
      formatter: (value: number) => `${value}${unidade ? " " + unidade : ""}`,
    },
  },
  scales: {
    x: { ticks: { color: "#cbd5e1" }, grid: { display: false } },
    y: {
      beginAtZero: true,
      ticks: { color: "#94a3b8" },
      grid: { color: "rgba(148, 163, 184, 0.15)" },
    },
  },
});

// --- distribuição (dict {categoria: contagem}) -> barra horizontal ---

const MAX_CATEGORIAS = 5;

const categoriasAgrupadas = (
  dist: IndicadorDistribuicao,
): [string, number][] => {
  const entradas = Object.entries(dist);
  if (entradas.length <= MAX_CATEGORIAS + 1) return entradas;
  const principais = entradas.slice(0, MAX_CATEGORIAS);
  const restante = entradas
    .slice(MAX_CATEGORIAS)
    .reduce((soma, [, v]) => soma + v, 0);
  return [...principais, ["Outros", restante]];
};

const alturaBarraDistribuicao = (indicador?: Indicador): number => {
  if (!indicador) return 180;
  const dist = indicador.valor as IndicadorDistribuicao;
  const qtd = categoriasAgrupadas(dist).length;
  return Math.max(180, qtd * 48);
};

const buildDistribuicaoData = (indicador: Indicador) => {
  const dist = indicador.valor as IndicadorDistribuicao;
  const entradas = categoriasAgrupadas(dist);
  return {
    labels: entradas.map(([nome]) => nome),
    datasets: [
      {
        label: indicador.nome,
        data: entradas.map(([, valor]) => valor),
        backgroundColor: entradas.map((_, i) => PALETA[i % PALETA.length]),
        borderColor: "#0f172a",
        borderWidth: 1,
        borderRadius: 6,
      },
    ],
  };
};

const buildDistribuicaoOptions = (indicador: Indicador) => {
  const dist = indicador.valor as IndicadorDistribuicao;
  const total = Object.values(dist).reduce((a, b) => a + b, 0);
  return {
    indexAxis: "y" as const,
    responsive: true,
    maintainAspectRatio: false,
    layout: { padding: { right: 56 } },
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (ctx: any) => {
            const valor = ctx.raw as number;
            const pct = total > 0 ? Math.round((valor / total) * 100) : 0;
            return `${valor} (${pct}%)`;
          },
        },
      },
      datalabels: {
        ...DATALABELS_BASE,
        anchor: "end" as const,
        align: "end" as const,
        formatter: (value: number) => {
          const pct = total > 0 ? Math.round((value / total) * 100) : 0;
          return `${value} (${pct}%)`;
        },
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        ticks: { color: "#94a3b8", precision: 0 },
        grid: { color: "rgba(148, 163, 184, 0.15)" },
      },
      y: {
        ticks: { color: "#cbd5e1" },
        grid: { display: false },
      },
    },
  };
};
</script>
