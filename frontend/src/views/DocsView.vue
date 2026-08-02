<template>
  <div class="mx-auto max-w-3xl">
    <!-- Cabeçalho -->
    <div class="mb-6 flex items-start justify-between gap-4">
      <div>
        <button
          @click="voltar"
          class="mb-3 flex items-center gap-1.5 font-mono text-[11px] uppercase tracking-[0.14em] text-[#767c8a] transition-colors hover:text-[#ece8df]"
        >
          <ArrowLeftIcon class="h-3.5 w-3.5" />
          Voltar
        </button>
        <p class="font-mono text-[11px] uppercase tracking-[0.16em] text-[#8b8f9c]">
          Documentação técnica
        </p>
        <h1 class="mt-1 font-serif text-2xl font-medium text-[#ece8df]">
          {{ tituloPagina }}
        </h1>
      </div>

      <!-- Ações de topo, só na lista geral -->
      <div v-if="!indicadorSolicitado" class="flex shrink-0 gap-2">
        <button
          v-if="temRascunhos()"
          @click="exportando = true"
          class="flex items-center gap-1.5 rounded-md border border-[#2c3140] px-3 py-2 font-mono text-[11px] uppercase tracking-wider text-[#8b8f9c] transition-colors hover:border-[#4f8a8b] hover:text-[#ece8df]"
        >
          <ClipboardDocumentIcon class="h-3.5 w-3.5" />
          Exportar rascunhos
        </button>
        <button
          @click="iniciarCriacao()"
          class="flex items-center gap-1.5 rounded-md border border-[#4f8a8b] bg-[#4f8a8b]/10 px-3 py-2 font-mono text-[11px] uppercase tracking-wider text-[#7fb0b1] transition-colors hover:bg-[#4f8a8b]/20"
        >
          <PlusIcon class="h-3.5 w-3.5" />
          Nova documentação
        </button>
      </div>
    </div>

    <!-- Modal simples de exportação -->
    <div
      v-if="exportando"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-6"
      @click.self="exportando = false"
    >
      <div class="w-full max-w-2xl rounded-md border border-[#2c3140] bg-[#181c25] p-5">
        <div class="mb-3 flex items-center justify-between">
          <h3 class="font-serif text-[15px] font-medium text-[#ece8df]">
            Código para colar em metricasDocs.ts
          </h3>
          <button @click="exportando = false" class="text-[#767c8a] hover:text-[#ece8df]">
            <XMarkIcon class="h-4 w-4" />
          </button>
        </div>
        <p class="mb-3 text-sm leading-relaxed text-[#9096a3]">
          Cole estas entradas dentro do objeto <code class="text-[#c99a3e]">METRICAS_DOCS</code>,
          no arquivo <code class="text-[#c99a3e]">metricasDocs.ts</code>. Depois de commitado, pode
          descartar os rascunhos locais.
        </p>
        <pre
          class="max-h-80 overflow-auto rounded-sm border border-[#2c3140] bg-[#12151c] p-3 font-mono text-xs text-[#c99a3e]"
          >{{ codigoExportado }}</pre
        >
        <div class="mt-4 flex justify-end gap-2">
          <button
            @click="copiarCodigo"
            class="rounded-md border border-[#2c3140] px-3 py-2 font-mono text-[11px] uppercase tracking-wider text-[#8b8f9c] hover:border-[#4f8a8b] hover:text-[#ece8df]"
          >
            {{ copiado ? "Copiado!" : "Copiar" }}
          </button>
        </div>
      </div>
    </div>

    <!-- Formulário de edição/criação -->
    <div v-if="editando" class="space-y-4 rounded-md border border-[#252a35] bg-[#1b1f29] p-5">
      <div v-if="criandoNovo">
        <label class="mb-1 block font-mono text-[10px] uppercase tracking-wider text-[#767c8a]">
          Nome exato do indicador (deve bater com o retornado pelo backend)
        </label>
        <input
          v-model="form.nome"
          type="text"
          placeholder="ex: Porcentagem de exames concluídos"
          class="w-full rounded-md border border-[#2c3140] bg-[#12151c] p-2.5 text-sm text-[#ece8df] focus:border-[#4f8a8b] focus:outline-none"
        />
      </div>

      <div>
        <label class="mb-1 block font-mono text-[10px] uppercase tracking-wider text-[#767c8a]">
          Título de exibição
        </label>
        <input
          v-model="form.titulo"
          type="text"
          class="w-full rounded-md border border-[#2c3140] bg-[#12151c] p-2.5 text-sm text-[#ece8df] focus:border-[#4f8a8b] focus:outline-none"
        />
      </div>

      <div>
        <label class="mb-1 block font-mono text-[10px] uppercase tracking-wider text-[#767c8a]">
          Módulo
        </label>
        <input
          v-model="form.modulo"
          type="text"
          placeholder="ex: Internação, Cirurgia, Exames..."
          class="w-full rounded-md border border-[#2c3140] bg-[#12151c] p-2.5 text-sm text-[#ece8df] focus:border-[#4f8a8b] focus:outline-none"
        />
      </div>


      <div>
        <label class="mb-1 block font-mono text-[10px] uppercase tracking-wider text-[#767c8a]">
          Como é calculado
        </label>
        <textarea
          v-model="form.calculo"
          rows="4"
          class="w-full resize-y rounded-md border border-[#2c3140] bg-[#12151c] p-2.5 text-sm text-[#ece8df] focus:border-[#4f8a8b] focus:outline-none"
        ></textarea>
        
        <div>
          <label class="mb-1 block font-mono text-[10px] uppercase tracking-wider text-[#767c8a]">
            Observações (opcional)
          </label>
          <textarea
            v-model="form.observacoes"
            rows="5"
            placeholder="Contexto adicional sobre o gráfico ou a métrica: o que ele mostra, decisões de leitura, casos especiais..."
            class="w-full resize-y rounded-md border border-[#2c3140] bg-[#12151c] p-2.5 text-sm text-[#ece8df] focus:border-[#4f8a8b] focus:outline-none"
          ></textarea>
        </div>
      </div>


      <div class="flex items-center justify-between pt-1">
        <p class="font-mono text-[10px] text-[#5c6270]">
          Salvo só neste navegador até você exportar e colar no código.
        </p>
        <div class="flex gap-2">
          <button
            @click="cancelarEdicao"
            class="rounded-md border border-[#2c3140] px-3 py-2 font-mono text-[11px] uppercase tracking-wider text-[#8b8f9c] hover:text-[#ece8df]"
          >
            Cancelar
          </button>
          <button
            @click="salvarForm"
            :disabled="!form.nome || !form.titulo"
            class="rounded-md border border-[#4f8a8b] bg-[#4f8a8b]/10 px-3 py-2 font-mono text-[11px] uppercase tracking-wider text-[#7fb0b1] transition-colors hover:bg-[#4f8a8b]/20 disabled:cursor-not-allowed disabled:opacity-40"
          >
            Salvar
          </button>
        </div>
      </div>
    </div>

    <!-- Detalhe de um indicador específico -->
    <div v-else-if="docAtual" class="space-y-8">
      <div class="flex items-center justify-between border-b border-[#252a35] pb-4">
        <span class="font-mono text-[11px] uppercase tracking-[0.14em] text-[#767c8a]">
          {{ docAtual.modulo }}
        </span>
        <div class="flex items-center gap-4">
          <span
            v-if="docAtual.origem === 'rascunho'"
            class="font-mono text-[11px] uppercase tracking-[0.14em] text-[#c99a3e]"
          >
            Rascunho local
          </span>
          <button
            @click="iniciarEdicao(docAtual)"
            class="flex items-center gap-1 font-mono text-[11px] uppercase tracking-[0.14em] text-[#767c8a] transition-colors hover:text-[#ece8df]"
          >
            <PencilIcon class="h-3.5 w-3.5" />
            Editar
          </button>
        </div>
      </div>

      <div>
        <h2 class="font-serif text-[17px] font-medium text-[#ece8df]">Como é calculado</h2>
        <p class="mt-3 whitespace-pre-wrap text-[15px] leading-relaxed text-[#9096a3]">
          {{ docAtual.calculo }}
        </p>
      </div>

      <div v-if="docAtual.observacoes">
        <h2 class="font-serif text-[17px] font-medium text-[#ece8df]">Observações</h2>
        <p class="mt-3 whitespace-pre-wrap text-[15px] leading-relaxed text-[#9096a3]">
          {{ docAtual.observacoes }}
        </p>
      </div>
    </div>

    <!-- Indicador ainda não documentado -->
    <div
      v-else-if="indicadorSolicitado"
      class="rounded-md border border-dashed border-[#2c3140] bg-[#151820] p-6 text-center"
    >
      <p class="font-mono text-xs text-[#666c79]">
        Ainda não há documentação para
        <span class="text-[#8b8f9c]">"{{ indicadorSolicitado }}"</span>.
      </p>
      <button
        @click="iniciarCriacao(indicadorSolicitado)"
        class="mx-auto mt-4 flex items-center gap-1.5 rounded-md border border-[#4f8a8b] bg-[#4f8a8b]/10 px-3 py-2 font-mono text-[11px] uppercase tracking-wider text-[#7fb0b1] transition-colors hover:bg-[#4f8a8b]/20"
      >
        <PlusIcon class="h-3.5 w-3.5" />
        Escrever documentação agora
      </button>
    </div>

    <!-- Lista geral: acesso direto a /docs, sem indicador na query -->
    <div v-else class="space-y-8">
      <p class="text-sm leading-relaxed text-[#767c8a]">
        Clique no ícone <InformationCircleIcon class="inline h-4 w-4 align-text-bottom" /> em
        qualquer gráfico do dashboard para abrir a documentação do indicador diretamente.
      </p>

      <div v-if="docs.length === 0" class="border-t border-[#252a35] pt-6 text-center">
        <p class="font-mono text-xs text-[#666c79]">Nenhuma documentação ainda.</p>
      </div>

      <div v-for="[modulo, itens] in docsPorModulo" :key="modulo">
        <h2 class="font-mono text-[11px] uppercase tracking-[0.16em] text-[#767c8a]">
          {{ modulo }}
        </h2>
        <div class="mt-2 divide-y divide-[#252a35] border-t border-[#252a35]">
          <button
            v-for="item in itens"
            :key="item.nome"
            @click="abrir(item.nome)"
            class="group flex w-full items-center justify-between gap-3 py-3 text-left"
          >
            <p class="font-serif text-[15px] text-[#c7c3ba] transition-colors group-hover:text-[#ece8df]">
              {{ item.titulo }}
            </p>
            <span v-if="item.origem === 'rascunho'" class="shrink-0 text-xs text-[#c99a3e]">
              rascunho
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  ArrowLeftIcon,
  PencilIcon,
  PlusIcon,
  ClipboardDocumentIcon,
  XMarkIcon,
  InformationCircleIcon,
} from "@heroicons/vue/24/outline";
import { useMetricasDocs } from "../composables/useMetricasDocs";
import type { MetricaDoc } from "../data/metricasDocs";

const route = useRoute();
const router = useRouter();
const { listar, obter, salvar, temRascunhos, exportarComoCodigo } = useMetricasDocs();

const indicadorSolicitado = computed(() => {
  const q = route.query.indicador;
  return typeof q === "string" ? q : Array.isArray(q) ? q[0] : null;
});

const docAtual = computed(() =>
  indicadorSolicitado.value ? obter(indicadorSolicitado.value) : null,
);

const docs = computed(() => listar());

// Agrupa a lista geral por módulo, na ordem em que os módulos aparecem nos
// dados — assim o módulo passa a ser um cabeçalho de seção (que carrega
// informação real: "esses indicadores pertencem a esse módulo") em vez de
// um selo repetido em cada linha.
const docsPorModulo = computed(() => {
  const grupos = new Map<string, (MetricaDoc & { nome: string })[]>();
  for (const item of docs.value) {
    const lista = grupos.get(item.modulo) ?? [];
    lista.push(item);
    grupos.set(item.modulo, lista);
  }
  return Array.from(grupos.entries());
});

const tituloPagina = computed(() => {
  if (editando.value) return criandoNovo.value ? "Nova documentação" : "Editando documentação";
  return docAtual.value?.titulo ?? "Como as métricas são calculadas";
});

const voltar = () => {
  if (editando.value) {
    cancelarEdicao();
    return;
  }
  if (indicadorSolicitado.value) {
    router.push({ path: "/docs" });
    return;
  }
  router.back();
};

// --- edição / criação ---

const editando = ref(false);
const criandoNovo = ref(false);
const form = reactive<MetricaDoc & { nome: string }>({
  nome: "",
  titulo: "",
  modulo: "",
  calculo: "",
  observacoes: ""
});

const resetForm = () => {
  form.nome = "";
  form.titulo = "";
  form.modulo = "";
  form.observacoes = "";
};

const iniciarCriacao = (nomeSugerido?: string | null) => {
  resetForm();
  if (nomeSugerido) form.nome = nomeSugerido;
  criandoNovo.value = true;
  editando.value = true;
};

const iniciarEdicao = (doc: MetricaDoc & { nome: string }) => {
  resetForm();
  Object.assign(form, doc);
  criandoNovo.value = false;
  editando.value = true;
};

const cancelarEdicao = () => {
  editando.value = false;
  criandoNovo.value = false;
  resetForm();
};

const salvarForm = () => {
  if (!form.nome || !form.titulo) return;
  const { nome, ...doc } = form;
  salvar(nome, doc);
  editando.value = false;
  criandoNovo.value = false;
  router.push({ path: "/docs", query: { indicador: nome } });
};

const abrir = (nome: string) => {
  router.push({ path: "/docs", query: { indicador: nome } });
};

// --- exportação ---

const exportando = ref(false);
const copiado = ref(false);
const codigoExportado = computed(() => exportarComoCodigo());

const copiarCodigo = async () => {
  try {
    await navigator.clipboard.writeText(codigoExportado.value);
    copiado.value = true;
    setTimeout(() => (copiado.value = false), 1500);
  } catch {
    // Clipboard indisponível (ex.: contexto não-seguro) — o usuário ainda
    // pode selecionar o texto manualmente no <pre>.
  }
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