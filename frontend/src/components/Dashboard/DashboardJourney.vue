<template>
  <div class="flex h-full w-full flex-col bg-transparent">

    <div class="mb-5 flex items-start justify-between border-b border-[#2c3140] pb-4">
      <div class="flex items-center gap-3">
        <div
          class="flex h-10 w-10 shrink-0 items-center justify-center rounded-md border"
          :style="{ borderColor: config.cor, color: config.cor }"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="config.icone"></path>
          </svg>
        </div>
        <div>
          <p class="font-mono text-[10px] uppercase tracking-[0.14em] text-[#767c8a]">{{ config.subtitulo }}</p>
          <h3 class="font-serif text-lg font-medium leading-snug text-[#ece8df]">{{ config.titulo }}</h3>
        </div>
      </div>
      <div class="shrink-0 pl-3 text-right">
        <p class="font-mono text-xl font-semibold leading-none" :style="{ color: config.cor }">
          {{ stage?.total_eventos || 0 }}
        </p>
        <p class="mt-1 font-mono text-[10px] uppercase tracking-[0.12em] text-[#767c8a]">eventos</p>
      </div>
    </div>

    <!-- EVENTOS -->
    <div class="mb-6">
      <p class="mb-3 font-mono text-[10px] font-semibold uppercase tracking-[0.14em] text-[#767c8a]">Eventos</p>

      <div class="space-y-3.5">
        <div v-for="(evento, index) in stage?.eventos" :key="index">
          <div class="mb-1.5 flex items-baseline justify-between gap-3">
            <span class="text-sm font-medium text-[#9096a3]">{{ evento.nome }}</span>
            <span class="shrink-0 font-mono text-sm font-semibold tabular-nums text-[#ece8df]">{{ evento.valor }}</span>
          </div>
          <div class="h-1 w-full overflow-hidden rounded-sm bg-[#252a35]">
            <div
              class="h-full rounded-sm transition-all duration-300"
              :style="{ width: evento.porcentagem || '50%', backgroundColor: config.cor }"
            ></div>
          </div>
        </div>

        <div v-if="!stage?.eventos || stage?.eventos.length === 0" class="text-sm italic text-[#5c6270]">
          Nenhum evento registrado.
        </div>
      </div>
    </div>

    <!-- INDICADORES -->
    <div>
      <p class="mb-2 font-mono text-[10px] font-semibold uppercase tracking-[0.14em] text-[#767c8a]">Indicadores</p>

      <div class="divide-y divide-[#252a35]">
        <div
          v-for="(indicador, index) in stage?.indicadores"
          :key="index"
          class="flex items-start justify-between gap-3 py-2.5 first:pt-1"
        >
          <span class="wrap-break-word text-sm leading-snug text-[#9096a3]">{{ indicador.nome }}</span>

          <div class="flex max-w-[55%] shrink-0 flex-col items-end">
            <!-- valor simples (número / string / percentual) -->
            <div v-if="!isObjectValue(indicador.valor)" class="flex items-center gap-2">
              <span class="whitespace-nowrap text-right font-mono text-sm font-semibold tabular-nums text-[#ece8df]">
                {{ indicador.valor }}
              </span>

              <span
                v-if="indicador.variacao"
                :class="['flex shrink-0 items-center gap-0.5 text-xs font-semibold', avaliarIndicador(indicador).cor]"
              >
                <svg class="h-3 w-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="avaliarIndicador(indicador).icone"></path>
                </svg>
                {{ indicador.variacao }}
              </span>
            </div>

            <!-- valor composto (objeto/dict vindo do backend) -->
            <div v-else class="flex w-full flex-col items-end gap-1">
              <div
                v-for="(v, k) in indicador.valor"
                :key="k"
                class="flex w-full items-center justify-between gap-3 text-xs"
              >
                <span class="truncate text-[#767c8a]">{{ k }}</span>
                <span class="shrink-0 font-mono font-semibold tabular-nums text-[#b7bcc7]">{{ v }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="!stage?.indicadores || stage?.indicadores.length === 0" class="py-2 text-sm italic text-[#5c6270]">
          Nenhum indicador disponível.
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  stage: {
    type: Object,
    required: false,
    default: () => ({})
  },
  tipo: {
    type: String,
    required: true
  }
});

// Mesma cor de identidade por etapa usada em todo o dashboard: a cor deixa
// de ser decoração e passa a indicar em que ponto do fluxo assistencial
// aquele cartão está.
const config = computed(() => {
  const mapa: Record<string, any> = {
    entrada: {
      titulo: 'Entrada', subtitulo: 'Abertura de Prontuário', cor: '#4f8a8b',
      icone: 'M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1'
    },
    consultas: {
      titulo: 'Consultas', subtitulo: 'Atendimento Ambulatorial', cor: '#c99a3e',
      icone: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z'
    },
    exames: {
      titulo: 'Exames', subtitulo: 'Exames e Laudos', cor: '#b1615b',
      icone: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z'
    },
    procedimentos: {
      titulo: 'Procedimentos', subtitulo: 'Intervenções Clínicas', cor: '#a2653a',
      icone: 'M13 10V3L4 14h7v7l9-11h-7z'
    },
    internacao: {
      titulo: 'Internação', subtitulo: 'Internações e UTI', cor: '#5a7599',
      icone: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4'
    }
  };
  return mapa[props.tipo] || mapa.consultas;
});

// Detecta se o valor do indicador é um objeto/dict (ex.: contagens por categoria)
// em vez de um número/string simples, para poder renderizá-lo como uma
// mini-lista ao invés de um JSON cru.
const isObjectValue = (valor: any) => {
  return valor !== null && typeof valor === 'object' && !Array.isArray(valor);
};

// Cores semânticas de variação (bom/atenção/ruim) — aqui a cor carrega uma
// informação real de avaliação, por isso continua independente da paleta
// de identidade dos módulos.
const avaliarIndicador = (indicador: any) => {

  if (indicador.status === 'ruim') {
    return { cor: 'text-[#c96a5f]', icone: 'M5 10l7-7m0 0l7 7m-7-7v18' }; // Seta p/ cima
  }
  if (indicador.status === 'atencao') {
    return { cor: 'text-[#c99a3e]', icone: 'M5 12h14' }; // Traço reto
  }
  if (indicador.status === 'bom') {
    return { cor: 'text-[#5f9e82]', icone: 'M19 14l-7 7m0 0l-7-7m7 7V3' }; // Seta p/ baixo
  }

  // Fallback (Se o backend ainda não tiver implementado o campo "status", ele tenta adivinhar pelo antigo "positivo")
  if (indicador.positivo !== undefined) {
    return indicador.positivo
      ? { cor: 'text-[#5f9e82]', icone: 'M5 10l7-7m0 0l7 7m-7-7v18' }
      : { cor: 'text-[#c96a5f]', icone: 'M19 14l-7 7m0 0l-7-7m7 7V3' };
  }

  // Default neutro
  return { cor: 'text-[#767c8a]', icone: 'M5 12h14' };
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