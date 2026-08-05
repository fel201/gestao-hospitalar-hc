<template>
  <section
    class="mt-10 rounded-lg border border-[#2c3140] bg-[#181c25] p-6"
  >
    <div
      class="flex flex-col gap-3 border-b border-[#2c3140] pb-5 md:flex-row md:items-end md:justify-between"
    >
      <div>
        <p class="font-mono text-[11px] uppercase tracking-[0.16em] text-[#8b8f9c]">
          Fluxo assistencial
        </p>
        <h2 class="mt-1 font-serif text-2xl font-medium text-[#ece8df]">
          Análise por módulo e subprocesso
        </h2>
        <p class="mt-2 max-w-2xl text-sm leading-relaxed text-[#9096a3]">
          Selecione um módulo e um subprocesso para visualizar os indicadores
          correspondentes.
        </p>
      </div>
    </div>

    <!-- Abas de módulo, no estilo de divisórias de prontuário: cada módulo
         carrega sua própria cor de identidade, usada depois nos gráficos. -->
    <div class="mt-6 flex flex-wrap gap-1">
      <button
        v-for="modulo in MODULOS"
        :key="modulo.id"
        class="rounded-t-md border border-b-0 px-4 py-2.5 text-sm font-medium transition-colors"
        :style="tabStyle(modulo.id)"
        @click="selecionarModulo(modulo.id)"
      >
        <span
          class="mr-2 inline-block h-1.5 w-1.5 rounded-full align-middle"
          :style="{ backgroundColor: MODULO_COLORS[modulo.id]?.base ?? '#6b7280' }"
        />
        {{ modulo.label }}
      </button>
    </div>

    <div
      class="rounded-b-md rounded-tr-md border border-[#2c3140] bg-[#15181f] p-5"
    >
      <div v-if="moduloSelecionado" class="grid gap-3 lg:grid-cols-3">
        <button
          v-for="sub in moduloSelecionado.submodulos"
          :key="sub.id"
          class="rounded-md border p-4 text-left transition-colors"
          :style="submoduloCardStyle(sub.id)"
          @click="activeSubmodulo = sub.id"
        >
          <p class="font-serif text-[15px] font-medium text-[#ece8df]">
            {{ sub.titulo }}
          </p>
          <p class="mt-1.5 text-sm leading-relaxed text-[#8b8f9c]">
            {{ sub.descricao }}
          </p>
        </button>
      </div>

      <div
        v-if="submoduloSelecionado"
        class="mt-6 border-t border-[#252a35] pt-6"
      >
        <div
          class="flex flex-col gap-1 border-l-2 pl-3 md:flex-row md:items-baseline md:justify-between md:gap-3"
          :style="{ borderColor: corAtiva }"
        >
          <div>
            <p class="font-mono text-[10px] uppercase tracking-[0.14em] text-[#767c8a]">
              Subprocesso ativo
            </p>
            <h3 class="font-serif text-lg font-medium text-[#ece8df]">
              {{ submoduloSelecionado.titulo }}
            </h3>
          </div>
          <p class="text-sm text-[#8b8f9c] md:max-w-sm md:text-right">
            {{ submoduloSelecionado.descricao }}
          </p>
        </div>

        <div class="mt-6 grid gap-5 xl:grid-cols-2">
          <div
            v-for="item in graficosResolvidos"
            :key="item.spec.id"
            class="rounded-md border border-[#252a35] bg-[#1b1f29] p-4"
            :class="{ 'xl:col-span-2': item.spec.tipo === 'distribuicao' }"
          >
          <div class="flex items-start justify-between gap-3">
            <h4 class="font-serif text-[15px] font-medium leading-snug text-[#ece8df]">
              {{ item.spec.titulo }}
            </h4>
            <div class="flex shrink-0 items-center gap-2">
              <button
                v-if="!item.indisponivel"
                @click="abrirDocumentacao(item)"
                title="Como essa métrica é calculada"
                class="text-[#767c8a] transition-colors hover:text-[#ece8df]"
              >
                <InformationCircleIcon class="h-4 w-4" />
              </button>
              <span
                class="rounded-sm border px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-widest text-[#8b8f9c]"
                style="border-color: #313847"
              >
                {{ rotuloTipo(item.spec.tipo) }}
              </span>
            </div>
          </div>

            <!-- Gráfico ainda não implementado no backend, ou faltam indicadores -->
            <div
              v-if="item.indisponivel"
              class="mt-6 flex h-40 items-center justify-center rounded-md border border-dashed border-[#2c3140] bg-[#151820] p-4 text-center"
            >
              <p class="font-mono text-xs text-[#666c79]">
                Ainda não disponível no backend{{
                  item.faltando.length ? ": " + item.faltando.join(", ") : ""
                }}.
              </p>
            </div>

            <!-- Comparação de proporções (2-4 categorias em %) -->
            <div
              v-else-if="item.spec.tipo === 'comparacao-proporcao'"
              class="mt-6"
              :style="{ height: alturaComparacao(item) + 'px' }"
            >
              <Bar
                :data="buildComparacaoProporcaoData(item)"
                :options="chartOptionsComparacaoProporcao(item)"
                :plugins="[ChartDataLabels]"
              />
            </div>

            <!-- Comparação de valores em dias/horas (mesma unidade) -->
            <div
              v-else-if="item.spec.tipo === 'comparacao-dias'"
              class="mt-6"
              :style="{ height: alturaComparacao(item) + 'px' }"
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
              class="mt-6 grid h-40 grid-cols-2 gap-3"
            >
              <div
                v-for="ind in item.indicadores"
                :key="ind.nome"
                class="flex flex-col items-center justify-center rounded-md border border-[#252a35] bg-[#15181f] p-3 text-center"
              >
                <span class="font-mono text-2xl font-semibold text-[#ece8df]">{{
                  formatarValor(ind.valor)
                }}</span>
                <span class="mt-1 text-xs text-[#8b8f9c]">{{
                  rotuloIndicador(item.spec, ind.nome)
                }}</span>
              </div>
            </div>

            <!-- Distribuição (dict {categoria: contagem}) -> gráfico de barras horizontal -->
            <div
              v-else-if="item.spec.tipo === 'distribuicao'"
              class="mt-6"
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

            <!-- Serie temporal (horas) -->
            <div
              v-else-if="item.spec.tipo === 'serie-temporal'"
              class="mt-6"
              :style="{ height: alturaSerieTemporal(item.indicadores[0]) + 'px' }"
            >
              <Bar
                :data="buildSerieTemporalData(item.indicadores[0])"
                :options="buildSerieTemporalOptions(item.spec.unidade)"
                :plugins="[ChartDataLabels]"
              />
            </div>

            <!-- Serie temporal percentual (0-100%) -->
            <div
              v-else-if="item.spec.tipo === 'serie-temporal-percentual'"
              class="mt-6"
              :style="{ height: alturaSerieTemporal(item.indicadores[0]) + 'px' }"
            >
              <Bar
                :data="buildSerieTemporalPercentualData(item.indicadores[0])"
                :options="buildSerieTemporalPercentualOptions()"
                :plugins="[ChartDataLabels]"
              />
            </div>
            <!-- Valor simples (número, string, dias, horas etc) -->
            <div v-else class="mt-6 flex h-40 flex-col items-center justify-center gap-1">
              <p class="font-mono text-3xl font-semibold" :style="{ color: corAtiva }">
                {{ formatarValorSimples(item) }}
              </p>
            </div>
          </div>

          <div
            v-if="graficosResolvidos.length === 0"
            class="col-span-full text-sm text-[#8b8f9c]"
          >
            Nenhum gráfico configurado para este subprocesso ainda.
          </div>
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
import { useRouter } from "vue-router";
import { InformationCircleIcon } from "@heroicons/vue/24/outline";

const router = useRouter();

const abrirDocumentacao = (item: GraficoResolvido) => {
  const nomeIndicador = item.spec.indicadorNomes[0];
  if (!nomeIndicador) return;
  router.push({ path: "/docs", query: { indicador: nomeIndicador } });
};
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

// Dicionário de categorias fixas que somam 100% (ex.: Ambulatoriais / Pré-operatórios
// e Emergenciais), com valores já formatados como string ("45.2%") ou numéricos.
// Difere de IndicadorDistribuicao (contagens abertas): aqui as chaves são fixas
// e o conjunto é tratado como uma comparação de proporções, não uma distribuição.
type IndicadorProporcaoDict = Record<string, number | string>;

type Indicador = {
  nome: string;
  valor: number | string | IndicadorDistribuicao | IndicadorProporcaoDict;
};

type TipoGrafico =
  | "comparacao-proporcao"
  | "comparacao-dias"
  | "comparacao-mista"
  | "distribuicao"
  | "serie-temporal"
  | "serie-temporal-percentual"
  | "valor-simples";

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
// Identidade visual por módulo. Cada etapa do fluxo assistencial recebe uma
// cor própria e discreta, usada de forma consistente na aba, no card de
// subprocesso e nos gráficos daquele módulo — a cor passa a significar algo
// (a etapa do fluxo), em vez de ser decoração aleatória.
// -------------------------------------------------------------------------

const MODULO_COLORS: Record<string, { base: string }> = {
  entrada: { base: "#4f8a8b" }, // recepção / triagem — teal contido
  consultas: { base: "#c99a3e" }, // consultas / retornos — ocre
  exames: { base: "#b1615b" }, // exames — terracota apagado
  internacao: { base: "#5a7599" }, // internação — azul-ardósia
  cirurgia: { base: "#8a5a86" }, // cirurgia — ameixa
};

const NEUTRO_OUTROS = "#5c6270";

const corAtiva = computed(
  () => MODULO_COLORS[activeModulo.value]?.base ?? "#5c6270",
);

// Mistura um hex com branco na proporção `ratio` (0 = cor original, 1 = branco).
const misturarComBranco = (hex: string, ratio: number): string => {
  const n = parseInt(hex.replace("#", ""), 16);
  const r = (n >> 16) & 255;
  const g = (n >> 8) & 255;
  const b = n & 255;
  const mix = (c: number) => Math.round(c + (255 - c) * ratio);
  return `rgb(${mix(r)}, ${mix(g)}, ${mix(b)})`;
};

// Paleta derivada da cor do módulo ativo: tons do mesmo matiz, do mais
// saturado ao mais claro, com um cinza neutro reservado para "Outros".
const paletaDoModulo = (moduloId: string): string[] => {
  const base = MODULO_COLORS[moduloId]?.base ?? NEUTRO_OUTROS;
  return [0, 0.2, 0.4, 0.58, 0.74].map((r) => misturarComBranco(base, r)).concat(NEUTRO_OUTROS);
};

const tabStyle = (moduloId: string) => {
  const cor = MODULO_COLORS[moduloId]?.base ?? NEUTRO_OUTROS;
  const ativo = activeModulo.value === moduloId;
  return {
    borderColor: ativo ? "#2c3140" : "#22262f",
    borderTopWidth: "3px",
    borderTopColor: ativo ? cor : "transparent",
    backgroundColor: ativo ? "#15181f" : "#181b22",
    color: ativo ? "#ece8df" : "#8b8f9c",
  };
};

const submoduloCardStyle = (subId: string) => {
  const ativo = activeSubmodulo.value === subId;
  return {
    borderColor: ativo ? corAtiva.value : "#252a35",
    backgroundColor: ativo ? misturarComBrancoBg(corAtiva.value) : "#181b22",
  };
};

// Fundo bem sutil (quase imperceptível) na cor do módulo, só para o card ativo.
const misturarComBrancoBg = (hex: string): string => {
  const n = parseInt(hex.replace("#", ""), 16);
  const r = (n >> 16) & 255;
  const g = (n >> 8) & 255;
  const b = n & 255;
  return `rgba(${r}, ${g}, ${b}, 0.08)`;
};

// -------------------------------------------------------------------------
// Estrutura de módulos/subprocessos/gráficos, seguindo o documento de
// especificação e o mapeamento confirmado indicador-a-indicador.
// -------------------------------------------------------------------------
const rotuloIndicador = (spec: GraficoSpec, nomeReal: string): string =>
  spec.rotulos?.[nomeReal] ?? nomeReal;

const buildSerieTemporalData = (indicador: Indicador) => {
  const dados = indicador.valor as Record<string, number>;

  return {
    labels: Object.keys(dados),
    datasets: [
      {
        label: indicador.nome,
        data: Object.values(dados).map(numeroDoValor),
        backgroundColor: corAtiva.value,
        borderRadius: 3,
        maxBarThickness: 52,
      },
    ],
  };
};

// NOTA sobre o fix de clipping: quando uma barra chega perto do topo da área
// do gráfico, o datalabel (anchor "end" / align "top") é desenhado acima da
// própria barra — e se não houver espaço reservado ali, ele fica cortado
// pela borda do canvas, só aparecendo no hover do tooltip. Duas mudanças
// resolvem isso:
//  1. `layout.padding.top` reserva uma faixa fixa acima da área do gráfico
//     para os labels "estourarem" sem serem cortados.
//  2. `grace` na escala Y adiciona uma folga percentual acima do maior valor
//     dos dados, então a barra mais alta nunca encosta no teto da área
//     plotada (isso também ajuda mesmo com o padding, pois evita que a barra
//     e o label disputem o mesmo pixel).
const buildSerieTemporalOptions = (unidade?: string) => {
  // Para indicadores em minutos, o tooltip (mais espaço, um de cada vez)
  // mostra o par completo "120 min / 2 horas". Já o rótulo fixo acima da
  // barra usa uma versão compacta ("120min/2h") — o texto completo em cada
  // uma das barras lado a lado não cabia e ficava sobrepondo a barra
  // vizinha. O eixo Y continua só em minutos, para não duplicar a mesma
  // informação em dois formatos ao lado um do outro.
  const formatarTooltip = (value: number): string =>
    unidade === "min"
      ? formatarMinutosComHoras(value)
      : `${value}${unidade ? " " + unidade : ""}`;

  const formatarRotulo = (value: number): string =>
    unidade === "min"
      ? formatarMinutosCompacto(value)
      : `${value}${unidade ? " " + unidade : ""}`;

  const formatarEixo = (value: number): string =>
    unidade === "min" ? `${value} min` : `${value}${unidade ? " " + unidade : ""}`;

  return {
    responsive: true,
    maintainAspectRatio: false,
    layout: { padding: { top: 28 } },

    plugins: {
      legend: {
        display: false,
      },

      tooltip: {
        callbacks: {
          label: (ctx: any) => formatarTooltip(ctx.raw),
        },
      },

      datalabels: {
        ...DATALABELS_BASE,

        anchor: "end" as const,
        align: "top" as const,
        offset: 4,
        clamp: true,

        formatter: (value: number) =>
          value === 0 ? "0" : formatarRotulo(value),
      },
    },

    scales: {
      x: {
        ticks: {
          color: "#8b8f9c",
          font: { family: "'IBM Plex Mono', monospace", size: 11 },
          autoSkip: false,
          maxRotation: 0,
          minRotation: 0,
          callback: function (this: any, value: string | number) {
            return quebrarLabel(this.getLabelForValue(value as number));
          },
        },
        grid: {
          display: false,
        },
      },

      y: {
        beginAtZero: true,
        grace: "10%",

        ticks: {
          color: "#767c8a",
          font: { family: "'IBM Plex Mono', monospace", size: 11 },
          callback: (v: any) => formatarEixo(Number(v)),
        },

        grid: {
          color: "rgba(140, 148, 163, 0.08)",
        },
      },
    },
  };
};

// Série temporal em percentual (0-100%): mesmo espírito da série temporal em
// horas, mas com escala travada em 0-100 e rótulos com "%" em vez de "h" —
// evita o eixo Y sem teto e o sufixo de hora que não fazem sentido aqui.
const buildSerieTemporalPercentualData = (indicador: Indicador) => {
  const dados = indicador.valor as Record<string, number | string>;

  return {
    labels: Object.keys(dados),
    datasets: [
      {
        label: indicador.nome,
        data: Object.values(dados).map(numeroDoValor),
        backgroundColor: corAtiva.value,
        borderRadius: 3,
        maxBarThickness: 52,
      },
    ],
  };
};

// Mesmo fix de clipping do builder acima: padding no topo do layout +
// datalabel "clampado" dentro da área desenhável. Como o eixo aqui tem
// `max: 100` fixo (não dá pra usar `grace` para abrir folga acima de 100%),
// o padding + `clamp: true` são o que garante que uma barra em 100% ainda
// mostre o rótulo, empurrando-o para dentro da área reservada em vez de
// cortá-lo na borda do canvas.
const buildSerieTemporalPercentualOptions = () => ({
  responsive: true,
  maintainAspectRatio: false,
  layout: { padding: { top: 28 } },

  plugins: {
    legend: {
      display: false,
    },

    tooltip: {
      callbacks: {
        label: (ctx: any) => `${ctx.raw}%`,
      },
    },

    datalabels: {
      ...DATALABELS_BASE,

      anchor: "end" as const,
      align: "top" as const,
      offset: 4,
      clamp: true,

      formatter: (value: number) => `${value}%`,
    },
  },

  scales: {
    x: {
      ticks: {
        color: "#8b8f9c",
        font: { family: "'IBM Plex Mono', monospace", size: 11 },
        autoSkip: false,
        maxRotation: 0,
        minRotation: 0,
        callback: function (this: any, value: string | number) {
          return quebrarLabel(this.getLabelForValue(value as number));
        },
      },
      grid: {
        display: false,
      },
    },

    y: {
      beginAtZero: true,
      max: 100,

      ticks: {
        color: "#767c8a",
        font: { family: "'IBM Plex Mono', monospace", size: 11 },
        callback: (v: any) => `${v}%`,
      },

      grid: {
        color: "rgba(140, 148, 163, 0.08)",
      },
    },
  },
});

const MODULOS: ModuloSpec[] = [
  {
    id: "entrada",
    label: "Entrada",
    dataKey: "entrada",
    submodulos: [
      {
        id: "entrada-geral",
        titulo: "Indicadores gerais",
        descricao:
          "Tempo até o primeiro evento assistencial e prontuários inertes, considerando todas as especialidades.",
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
        id: "consultas-especialidade",
        titulo: "Indicadores da especialidade correspondente",
        descricao: "Métricas de consultas filtradas pela especialidade atual.",
        graficos: [
          {
            id: "consultas-proporcao-tipos",
            titulo:
            "Porcentagem de cada tipo de consulta",
            tipo: "comparacao-proporcao",
            indicadorNomes: ["Porcentagem dos tipos de consultas"],
            incluirOutros: true,
          },
          {
            id: "consultas-faltas",
            titulo: "Comparação de faltas",
            tipo: "comparacao-proporcao",
            indicadorNomes: [
              "Porcentagem de faltas",
            ],
          },
          {
            id: "consultas-encaminhamentos",
            titulo: "Encaminhamentos mais frequentes após consulta regulada",
            tipo: "distribuicao",
            indicadorNomes: ["Encaminhamento frequente por consulta regulada"],
          },
          {
            id: "consultas-retorno-interconsulta-paciente",
            titulo: "Comparação do número de consultas (de cada tipo) por paciente ativo",
            tipo: "comparacao-dias",
            indicadorNomes: ["Média de consultas de cada tipo por paciente"],
          },
          {
            id: "consultas-intervalo-retornos",
            titulo: "Intervalo médio entre consultas",
            tipo: "serie-temporal",
            indicadorNomes: ["Intervalo médio entre consultas",],
            unidade: "dias",
          },
        ], 
      },
      {
        id: "consultas-geral",
        titulo: "Indicadores gerais",
        descricao:
          "Reguladas, retornos e interconsultas: proporções, encaminhamentos, faltas e intervalos, considerando todas as especialidades.",
        graficos: [
          {
            id: "consultas-porcentagem-global",
            titulo: "Porcentagem global dos tipos de consultas",
            tipo: "comparacao-proporcao",
            indicadorNomes: [
              "Porcentagem global dos tipos de consultas"
            ],
          },
          {
            id: "consultas-tempo-prontuario-agendamento",
            titulo:
            "Tempo médio entre a criação do prontuário e o agendamento da consulta",
            tipo: "valor-simples",
            indicadorNomes: [
              "Tempo medio global entre a criação de prontuário e o primeiro agendamento",
            ], 
          },
          {
            id: "consultas-tempo-agendamento-realizacao",
            titulo: "Tempo médio global do agendamento até realização da consulta",
            tipo: "valor-simples",
            indicadorNomes: [
              "Tempo médio de agendamento até realização (horas)",
            ],
            unidade: "horas"
          },
          {
            id: "consultas-faltas-global",
            titulo: "Porcentagem global de faltas",
            tipo: "comparacao-proporcao",
            indicadorNomes: [
              "Porcentagem global de faltas"
            ],
          },
          {
            id: "consultas-encaminhamento-global",
            titulo: "Encaminhamento global frequente após uma consulta regulada",
            tipo: "distribuicao",
            indicadorNomes: [
              "Encaminhamento global frequente por consulta regulada"
            ],
          },
          {
            id: "consultas-intervalo",
            titulo: "Intervalo médio entre consultas",
            tipo: "comparacao-dias",
            indicadorNomes: [
              "Intervalo médio global entre consultas"
            ],
            unidade: "dias"
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
        id: "exames-especialidade",
        titulo: "Indicadores da especialidade correspondente",
        descricao: "Tudo sobre a especialidade atual.",
        graficos: [
          {
            id: "exames-amb-proporcao",
            titulo: "Porcentagem de exames concluídos",
            tipo: "valor-simples",
            indicadorNomes: [
              "Porcentagem de exames concluídos",
            ],
          },
          {
            id: "exames-amb-proporcao",
            titulo: "Porcentagem de exames regulados",
            tipo: "valor-simples",
            indicadorNomes: [
              "Porcentagem de exames regulados",
            ],
          },
          {
            id: "exames-amb-proporcao",
            titulo: "Porcentagem de exames marcados como pendentes",
            tipo: "valor-simples",
            indicadorNomes: [
              "Porcentagem de exames marcados como pendentes",
            ],
          },
          {
            id: "exames-amb-proporcao",
            titulo: "Comparação dos tipos de exames nos últimos 5 meses",
            tipo: "comparacao-proporcao",
            indicadorNomes: [
              "Distribuição de exames por grupo de executor",
            ],
            rotulos: {
              "Porcentagem de exames ambulatoriais": "Exames Ambulatoriais",
              "Porcentagem de exames emergenciais e pré-operatórios":
              "Emergenciais e Pré-Operatórios",
            },
          },
          {
            id: "exames-amb-tempo-solicitacao",
            titulo:
              "Tempo médio de solicitação até a realização do exame nos últimos 5 meses",
            tipo: "serie-temporal",
            indicadorNomes: [
              "Tempo médio de solicitação até a realização do exame por mês",
            ],
            unidade: "horas"
          },
        ],
      },
      {
        id: "exames-geral",
        titulo: "Indicadores gerais",
        descricao:
          "Métricas gerais sobre exames, agregando todas as especialidades.",
        graficos: [
          {
            id: "exames-amb-proporcao",
            titulo: "Comparação dos tipos de exames nos últimos 5 meses",
            tipo: "comparacao-proporcao",
            indicadorNomes: [
              "Distribuição de exames por grupo de executor (global)",
            ],
            rotulos: {
              "Ambulatoriais": "Exames Ambulatoriais",
              "Pré-operatórios e Emergenciais": "Emergenciais e Pré-Operatórios",
            },
          },
          {
            id: "exames-cmp-tempo-realizacao",
            titulo: "Porcentagem global de exames concluídos",
            tipo: "valor-simples",
            indicadorNomes: ["Porcentagem global de exames concluídos"],
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
        id: "internacao-especialidade",
        titulo: "Indicadores da especialidade correspondente",
        descricao:
          "Internações pré e pós-operatórias, filtradas pela especialidade cirúrgica/clínica atual.",
        graficos: [
          {
            id: "internacao-pre-especialidade",
            titulo:
              "Porcentagem de internações concluídas com sumário de alta informatizado",
            tipo: "comparacao-proporcao",
            indicadorNomes: ["Porcentagem de sumários de alta informatizados"],
          },
          {
            id: "internacao-pos-uti",
            titulo:
              "Porcentagem dos desfechos mais comuns de uma internação",
            tipo: "comparacao-proporcao",
            indicadorNomes: ["Porcentagem dos desfechos mais comuns"],
          },
          {
            id: "internacao-pos-tempo",
            titulo:
              "Tempo médio de permanência de internação nos últimos 5 meses",
            tipo: "serie-temporal",
            indicadorNomes: ["Tempo médio de permanência de internação nos últimos 5 meses"],
            unidade: "dias"
          },
        ],
      },
      {
        id: "internacao-geral",
        titulo: "Indicadores gerais",
        descricao:
          "Por especialidade clínica, tempo médio e comparação entre os três tipos de internação.",
        graficos: [
          {
            id: "internacao-especialidade-clinica",
            titulo:
              "Tempo médio de internação por especialidade clínica",
            tipo: "serie-temporal",
            indicadorNomes: ["Tempo médio de permanência por especialidade"],
            unidade: "min"
          },
          {
            id: "internacao-sumario-alta-mes",
            titulo: "Porcentagem de sumários de alta informatizados por mês",
            tipo: "comparacao-proporcao",
            indicadorNomes: ["Porcentagem de sumários de alta informatizados"],
          },
          {
            id: "internacao-cmp-proporcao",
            titulo: "Porcentagem de registros de pacientes internados por especialidade clínica",
            tipo: "comparacao-proporcao",
            indicadorNomes: ["Porcentagem de registros de pacientes internados por especialidade clínica"],
          },
          {
            id: "internacao-cmp-tempo",
            titulo: "Especialidades com maior número de internações",
            tipo: "comparacao-proporcao",
            indicadorNomes: ["Especialidades com maior percentual de internações"],
          },
          {
            id: "internacao-cmp-participacao",
            titulo: "Porcentagem geral dos desfechos mais comuns",
            tipo: "comparacao-proporcao",
            indicadorNomes: ["Porcentagem geral dos desfechos mais comuns"],
          },
          {
            id: "internacao-tempo-medio",
            titulo: "Tempo médio global de permanência de internação nos últimos 5 meses",
            tipo: "serie-temporal",
            indicadorNomes: ["Tempo médio global de permanência de internação nos últimos 5 meses"],
            unidade: "dias"
          }
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
        id: "cirurgia-especialidade",
        titulo: "Indicadores da especialidade correspondente",
        descricao: "Métricas de cirurgia filtradas pela especialidade atual.",
        graficos: [
          {
            id: "cirurgia-tempo",
            titulo: "Tempo médio de cirurgia",
            tipo: "valor-simples",
            indicadorNomes: ["Tempo médio de cirurgia"],
            unidade: "min",
          },
          {
            id: "cirurgia-porcentagem-origem",
            titulo: "Porcentagem de cirurgias por origem",
            tipo: "comparacao-proporcao",
            indicadorNomes: ["Porcentagem de cirurgias por origem"]
          }
        ],
      },
      {
        id: "cirurgia-geral",
        titulo: "Indicadores gerais",
        descricao:
          "Proporção de pacientes operados e tempo médio de cirurgia, por especialidade.",
        graficos: [
          {
            id: "cirurgia-porcentagem-global",
            titulo: "Porcentagem global de cirurgias concluidas",
            tipo: "valor-simples",
            indicadorNomes: ["Porcentagem global de cirurgias concluidas"],
            unidade: "%"
          },
          {
            id: "cirurgia-tempo-especialidade",
            titulo:
              "Tempo médio de cirurgia por especialidade",
            tipo: "serie-temporal",
            indicadorNomes: ["Tempo médio de cirurgia por especialidade"],
            unidade: "min"
          },
          {
            id: "cirurgia-por-especialidade",
            titulo:
              "Cirurgias por especialidade",
            tipo: "comparacao-proporcao",
            indicadorNomes: ["Cirurgias por especialidade"],
          },
          {
            id: "cirurgia-porcentagem-origem-global",
            titulo: "Porcentagem global de cirurgia por origem",
            tipo: "serie-temporal",
            indicadorNomes: ["Porcentagem global de cirurgias por origem"]
          }
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

// Quando o backend retorna um único indicador cujo valor já é um dicionário
// de categorias fixas somando 100% (ex.: { Ambulatoriais: "45.2%",
// "Pré-operatórios e Emergenciais": "54.8%" }), essa função "achata" esse
// indicador em vários indicadores-folha — um por chave — para que os
// builders de comparação (que esperam 1 indicador por categoria) funcionem
// sem exigir que o backend mude o formato.
// Indicadores cujo valor já é number/string passam direto, sem alteração.
const expandirIndicadorProporcao = (indicador: Indicador): Indicador[] => {
  const valor = indicador.valor;
  if (valor && typeof valor === "object" && !Array.isArray(valor)) {
    return Object.entries(valor).map(([subNome, subValor]) => ({
      nome: subNome,
      valor: subValor as number | string,
    }));
  }
  return [indicador];
};

const graficosResolvidos = computed<GraficoResolvido[]>(() => {
  const lista = indicadoresDoBloco.value;
  const sub = submoduloSelecionado.value;
  if (!sub) return [];

  return sub.graficos.map((spec) => {
    const indicadoresBrutos: Indicador[] = [];
    const faltando: string[] = [];
    for (const nome of spec.indicadorNomes) {
      const encontrado = lista.find((i) => i.nome === nome);
      if (encontrado) indicadoresBrutos.push(encontrado);
      else faltando.push(nome);
    }
    const indisponivel =
      spec.indicadorNomes.length === 0 || faltando.length > 0;

    // A expansão só se aplica aos tipos de comparação (que esperam 1
    // indicador por categoria/barra). "distribuicao" continua recebendo o
    // dicionário bruto, pois seus builders já sabem lidar com ele.
    const deveExpandir =
      !indisponivel &&
      (spec.tipo === "comparacao-proporcao" || spec.tipo === "comparacao-dias");
    const indicadores = deveExpandir
      ? indicadoresBrutos.flatMap(expandirIndicadorProporcao)
      : indicadoresBrutos;

    return { spec, indicadores, faltando, indisponivel };
  });
});

// -------------------------------------------------------------------------
// Helpers de formatação/render
// -------------------------------------------------------------------------

// --- quebra de rótulos longos no eixo X (comparações) -----------------

// Nomes de especialidade/categoria podem ser bem longos (ex.: "HEMODINÂMICA
// E CARDIOLOGIA INTERVENCIONISTA") e não cabem numa linha só sem cortar ou
// se sobrepor à barra vizinha. Em vez de rotacionar o texto, quebramos em
// várias linhas curtas — o Chart.js aceita um array de strings como rótulo
// de tick e desenha cada item numa linha.
const LARGURA_MAX_LABEL = 14;

const quebrarLabel = (texto: string): string[] => {
  const palavras = texto.split(" ");
  const linhas: string[] = [];
  let linhaAtual = "";

  for (const palavra of palavras) {
    const tentativa = linhaAtual ? `${linhaAtual} ${palavra}` : palavra;
    if (tentativa.length > LARGURA_MAX_LABEL && linhaAtual) {
      linhas.push(linhaAtual);
      linhaAtual = palavra;
    } else {
      linhaAtual = tentativa;
    }
  }
  if (linhaAtual) linhas.push(linhaAtual);
  return linhas;
};

// Altura do container do gráfico, em px: parte de uma base confortável
// (a mesma altura que os cards já usavam, h-56 = 224px) e cresce um pouco
// para cada linha extra que o rótulo mais longo precisar, para que a
// quebra de linha calculada acima sempre tenha espaço reservado abaixo
// do eixo X.
// Mesma lógica de alturaComparacao, mas para os gráficos de série temporal,
// cujos rótulos vêm de Object.keys(indicador.valor) em vez de uma lista de
// indicadores. Base de 288px (equivalente ao h-72 usado antes no template).
const alturaSerieTemporal = (indicador: Indicador | undefined, baseAltura = 288): number => {
  if (!indicador) return baseAltura;
  const dados = indicador.valor as Record<string, number>;
  const labels = Object.keys(dados ?? {});
  const maxLinhas = Math.max(1, ...labels.map((l) => quebrarLabel(l).length));
  return baseAltura + (maxLinhas - 1) * 20;
};

const alturaComparacao = (item: GraficoResolvido): number => {
  const labels = item.indicadores.map((i) => rotuloIndicador(item.spec, i.nome));
  const maxLinhas = Math.max(1, ...labels.map((l) => quebrarLabel(l).length));
  return 224 + (maxLinhas - 1) * 20;
};

const rotuloTipo = (tipo: TipoGrafico) => {
  switch (tipo) {
    case "comparacao-proporcao":
    case "comparacao-dias":
    case "comparacao-mista":
      return "Comparação";
    case "distribuicao":
      return "Distribuição";
    case "serie-temporal":
    case "serie-temporal-percentual":
      return "Série temporal";
    default:
      return "Valor";
  }
};

const numeroDoValor = (valor: number | string): number => {
  if (typeof valor === "number") return valor;

  const limpo = valor
    .replace("%", "")
    .replace("horas", "")
    .replace("hora", "")
    .replace("dias", "")
    .replace("dia", "")
    .replace(",", ".")
    .trim();

  const n = parseFloat(limpo);

  return Number.isNaN(n) ? 0 : n;
};

// Formata um valor em minutos mostrando também o equivalente em horas,
// ex.: 120 -> "120 min / 2 horas", 90 -> "90 min / 1.5 horas".
// O número de horas é arredondado em até 2 casas decimais, sem zeros à
// direita (2.00 -> "2", 1.50 -> "1.5"), e o singular "hora" é usado só
// quando o valor arredondado é exatamente 1.
const formatarMinutosComHoras = (minutos: number): string => {
  if (!Number.isFinite(minutos)) return `${minutos} min`;
  const horas = Number((minutos / 60).toFixed(2));
  const horasLabel = horas === 1 ? "hora" : "horas";
  return `${minutos} min / ${horas} ${horasLabel}`;
};

// Versão curta do mesmo conteúdo, para caber como rótulo fixo em cima de
// cada barra (sem espaços, "min"/"h" abreviados e só 1 casa decimal na
// hora) — ex.: 260 -> "260min/4.3h". Usada nos gráficos de série temporal
// e comparação; o formato completo com "horas" por extenso fica reservado
// para o tooltip, onde há espaço de sobra.
const formatarMinutosCompacto = (minutos: number): string => {
  if (!Number.isFinite(minutos)) return `${minutos}min`;
  const horas = Number((minutos / 60).toFixed(1));
  return `${minutos}min/${horas}h`;
};

const formatarValor = (valor: Indicador["valor"] | undefined): string => {
  if (valor === undefined) return "—";
  if (typeof valor === "object") return "";
  return String(valor);
};

// Mesma ideia do formatarValor, mas ciente da unidade declarada na spec do
// gráfico:
//  - unidade "min" (caso da etapa de Cirurgia) mostra o equivalente em horas
//    ao lado do valor bruto em minutos ("120 min / 2 horas");
//  - unidade "%" cola o símbolo direto no número, sem espaço ("50%");
//  - qualquer outra unidade declarada (ex.: "horas", "dias") é exibida logo
//    depois do valor, com espaço ("10 horas");
//  - sem unidade declarada, mantém o comportamento antigo (valor cru).
const formatarValorSimples = (item: GraficoResolvido): string => {
  const bruto = item.indicadores[0]?.valor;
  if (bruto === undefined) return "—";
  if (typeof bruto === "object") return "";

  const unidade = item.spec.unidade;
  if (unidade === "min") {
    return formatarMinutosComHoras(numeroDoValor(bruto));
  }
  if (unidade === "%") {
    return `${bruto}%`;
  }
  if (unidade) {
    return `${bruto} ${unidade}`;
  }
  return String(bruto);
};

// Configuração base do datalabels, reaproveitada em todos os gráficos de barra.
// Contorno mais discreto que um contorno preto opaco — só o suficiente para
// garantir leitura sobre qualquer tom da paleta do módulo.
const DATALABELS_BASE = {
  color: "#f4f1ea",
  font: { weight: 600 as const, size: 11.5, family: "'IBM Plex Mono', monospace" },
  textStrokeColor: "rgba(10, 12, 16, 0.4)",
  textStrokeWidth: 1.5,
};

// --- comparação de proporções (0-100%), com "Outros" residual opcional ---

// Calcula um teto "arredondado" para o eixo Y a partir do maior valor da
// série, em vez de travar sempre em 100%. Adiciona ~15% de folga acima da
// maior barra (espaço para o datalabel) e arredonda para o múltiplo de 10
// mais próximo acima disso, sempre entre 10 e 100.
const calcularMaxEixoY = (valores: number[]): number => {
  const maxValor = Math.max(0, ...valores);
  if (maxValor <= 0) return 10;
  const comFolga = maxValor * 1.15;
  const arredondado = Math.ceil(comFolga / 10) * 10;
  return Math.min(100, Math.max(10, arredondado));
};

const buildComparacaoProporcaoData = (item: GraficoResolvido) => {
  const labels = item.indicadores.map((i) =>
    rotuloIndicador(item.spec, i.nome),
  );
  const valores = item.indicadores.map((i) =>
    numeroDoValor(i.valor as number | string),
  );


  const paleta = paletaDoModulo(activeModulo.value);

  return {
    labels,
    datasets: [
      {
        data: valores,
        backgroundColor: labels.map((_, i) => paleta[i % paleta.length]),
        borderColor: "#12151c",
        borderWidth: 1,
        borderRadius: 3,
        maxBarThickness: 56,
      },
    ],
  };
};

// Agora é uma função de `item`: o teto do eixo Y (`max`) é calculado a partir
// dos valores efetivamente exibidos nesse gráfico específico (incluindo
// "Outros", quando presente), em vez de um `max: 100` fixo para todo mundo.
const chartOptionsComparacaoProporcao = (item: GraficoResolvido) => {
  const valores = item.indicadores.map((i) =>
    numeroDoValor(i.valor as number | string),
  );
  if (item.spec.incluirOutros) {
    const soma = valores.reduce((a, b) => a + b, 0);
    valores.push(Math.max(0, 100 - soma));
  }
  const maxEixo = calcularMaxEixoY(valores);

  return {
    responsive: true,
    maintainAspectRatio: false,
    layout: { padding: { top: 32 } },
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: { label: (ctx: any) => `${ctx.raw}%` },
      },
      datalabels: {
        ...DATALABELS_BASE,
        anchor: "end" as const,
        align: "end" as const,
        offset: 4,
        clamp: true,
        formatter: (value: number) => `${value}%`,
      },
    },
    scales: {
      x: {
        ticks: {
          color: "#8b8f9c",
          font: { family: "'IBM Plex Mono', monospace", size: 11 },
          autoSkip: false,
          maxRotation: 0,
          minRotation: 0,
          callback: function (this: any, value: string | number) {
            return quebrarLabel(this.getLabelForValue(value as number));
          },
        },
        grid: { display: false },
      },
      y: {
        beginAtZero: true,
        max: maxEixo,
        ticks: {
          color: "#767c8a",
          font: { family: "'IBM Plex Mono', monospace", size: 11 },
          callback: (v: string | number) => `${v}%`,
        },
        grid: { color: "rgba(140, 148, 163, 0.08)" },
      },
    },
  };
};

// --- comparação de valores na mesma unidade (dias/horas) ---

const buildComparacaoValorData = (item: GraficoResolvido) => {
  const paleta = paletaDoModulo(activeModulo.value);
  return {
    labels: item.indicadores.map((i) => rotuloIndicador(item.spec, i.nome)),
    datasets: [
      {
        data: item.indicadores.map((i) =>
          numeroDoValor(i.valor as number | string),
        ),
        backgroundColor: item.indicadores.map((_, i) => paleta[i % paleta.length]),
        borderColor: "#12151c",
        borderWidth: 1,
        borderRadius: 3,
        maxBarThickness: 56,
      },
    ],
  };
};

const chartOptionsComparacaoValor = (unidade?: string) => {
  const formatarTooltip = (value: number): string =>
    unidade === "min"
      ? formatarMinutosComHoras(value)
      : `${value}${unidade ? " " + unidade : ""}`;

  const formatarRotulo = (value: number): string =>
    unidade === "min"
      ? formatarMinutosCompacto(value)
      : `${value}${unidade ? " " + unidade : ""}`;

  return {
    responsive: true,
    maintainAspectRatio: false,
    layout: { padding: { top: 32 } },
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (ctx: any) => formatarTooltip(ctx.raw),
        },
      },
      datalabels: {
        ...DATALABELS_BASE,
        anchor: "end" as const,
        align: "end" as const,
        offset: 4,
        clamp: true,
        formatter: (value: number) => formatarRotulo(value),
      },
    },
    scales: {
      x: {
        ticks: {
          color: "#8b8f9c",
          font: { family: "'IBM Plex Mono', monospace", size: 11 },
          autoSkip: false,
          maxRotation: 0,
          minRotation: 0,
          callback: function (this: any, value: string | number) {
            return quebrarLabel(this.getLabelForValue(value as number));
          },
        },
        grid: { display: false },
      },
      y: {
        beginAtZero: true,
        grace: "10%",
        ticks: { color: "#767c8a", font: { family: "'IBM Plex Mono', monospace", size: 11 } },
        grid: { color: "rgba(140, 148, 163, 0.08)" },
      },
    },
  };
};

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
  const paleta = paletaDoModulo(activeModulo.value);

  return {
    labels: entradas.map(([nome]) => nome),
    datasets: [
      {
        label: indicador.nome,
        data: entradas.map(([, valor]) => valor),
        backgroundColor: entradas.map((_, i) => paleta[i % paleta.length]),
        borderRadius: 3,
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
        offset: 4,
        clamp: true,
        formatter: (value: number) => {
          const pct = total > 0 ? Math.round((value / total) * 100) : 0;
          return `${value} (${pct}%)`;
        },
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        grace: "8%",
        ticks: { color: "#767c8a", precision: 0, font: { family: "'IBM Plex Mono', monospace", size: 11 } },
        grid: { color: "rgba(140, 148, 163, 0.08)" },
      },
      y: {
        ticks: { color: "#8b8f9c", font: { size: 12 } },
        grid: { display: false },
      },
    },
  };
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=IBM+Plex+Mono:wght@400;600&display=swap");

.font-serif {
  font-family: "Source Serif 4", Georgia, serif;
}

.font-mono {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
}
</style>