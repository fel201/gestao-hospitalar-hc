<template>
  <div class="flex flex-col h-full w-full bg-transparent">

    <div class="flex justify-between items-start mb-5">
      <div class="flex items-center gap-3">
        <div class="p-2 rounded-full bg-blue-900/30 text-blue-400 shrink-0">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="config.icone"></path>
          </svg>
        </div>
        <div>
          <p class="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">{{ config.subtitulo }}</p>
          <h3 class="text-lg font-bold text-slate-100 leading-snug">{{ config.titulo }}</h3>
        </div>
      </div>
      <div class="text-right shrink-0 pl-3">
        <p class="text-xl font-bold text-blue-400 leading-none">{{ stage?.total_eventos || 0 }}</p>
        <p class="text-[10px] text-slate-500 uppercase tracking-wider mt-1">eventos</p>
      </div>
    </div>

    <!-- EVENTOS -->
    <div class="mb-6">
      <p class="text-[11px] text-slate-500 uppercase tracking-wider font-bold mb-3">Eventos</p>

      <div class="space-y-3.5">
        <div v-for="(evento, index) in stage?.eventos" :key="index">
          <div class="flex justify-between items-baseline gap-3 mb-1.5">
            <span class="text-sm text-slate-400 font-medium">{{ evento.nome }}</span>
            <span class="text-sm font-bold text-slate-200 tabular-nums shrink-0">{{ evento.valor }}</span>
          </div>
          <div class="h-1 w-full bg-slate-700/40 rounded-full overflow-hidden">
            <div
              class="h-full rounded-full bg-blue-600 transition-all duration-300"
              :style="{ width: evento.porcentagem || '50%' }"
            ></div>
          </div>
        </div>

        <div v-if="!stage?.eventos || stage?.eventos.length === 0" class="text-sm text-slate-600 italic">
          Nenhum evento registrado.
        </div>
      </div>
    </div>

    <!-- INDICADORES -->
    <div>
      <p class="text-[11px] text-slate-500 uppercase tracking-wider font-bold mb-2">Indicadores</p>

      <div class="divide-y divide-slate-800/60">
        <div
          v-for="(indicador, index) in stage?.indicadores"
          :key="index"
          class="flex justify-between items-start gap-3 py-2.5 first:pt-1"
        >
          <span class="text-sm text-slate-400 leading-snug wrap-break-word">{{ indicador.nome }}</span>

          <div class="flex flex-col items-end shrink-0 max-w-[55%]">
            <!-- valor simples (número / string / percentual) -->
            <div v-if="!isObjectValue(indicador.valor)" class="flex items-center gap-2">
              <span class="text-sm font-bold text-slate-200 tabular-nums whitespace-nowrap text-right">
                {{ indicador.valor }}
              </span>

              <span
                v-if="indicador.variacao"
                :class="['text-xs font-semibold flex items-center gap-0.5 shrink-0', avaliarIndicador(indicador).cor]"
              >
                <svg class="w-3 h-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="avaliarIndicador(indicador).icone"></path>
                </svg>
                {{ indicador.variacao }}
              </span>
            </div>

            <!-- valor composto (objeto/dict vindo do backend) -->
            <div v-else class="flex flex-col items-end gap-1 w-full">
              <div
                v-for="(v, k) in indicador.valor"
                :key="k"
                class="flex justify-between items-center gap-3 w-full text-xs"
              >
                <span class="text-slate-500 truncate">{{ k }}</span>
                <span class="font-semibold text-slate-300 tabular-nums shrink-0">{{ v }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="!stage?.indicadores || stage?.indicadores.length === 0" class="text-sm text-slate-600 italic py-2">
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

const config = computed(() => {
  const mapa: Record<string, any> = {
    entrada: {
      titulo: 'Entrada', subtitulo: 'Abertura de Prontuário',
      icone: 'M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1'
    },
    consultas: {
      titulo: 'Consultas', subtitulo: 'Atendimento Ambulatorial',
      icone: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z'
    },
    exames: {
      titulo: 'Exames', subtitulo: 'Exames e Laudos',
      icone: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z'
    },
    procedimentos: {
      titulo: 'Procedimentos', subtitulo: 'Intervenções Clínicas',
      icone: 'M13 10V3L4 14h7v7l9-11h-7z'
    },
    internacao: {
      titulo: 'Internação', subtitulo: 'Internações e UTI',
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

const avaliarIndicador = (indicador: any) => {

  if (indicador.status === 'ruim') {
    return { cor: 'text-red-500', icone: 'M5 10l7-7m0 0l7 7m-7-7v18' }; // Seta p/ cima
  }
  if (indicador.status === 'atencao') {
    return { cor: 'text-yellow-500', icone: 'M5 12h14' }; // Traço reto
  }
  if (indicador.status === 'bom') {
    return { cor: 'text-emerald-500', icone: 'M19 14l-7 7m0 0l-7-7m7 7V3' }; // Seta p/ baixo
  }

  // Fallback (Se o backend ainda não tiver implementado o campo "status", ele tenta adivinhar pelo antigo "positivo")
  if (indicador.positivo !== undefined) {
    return indicador.positivo
      ? { cor: 'text-emerald-500', icone: 'M5 10l7-7m0 0l7 7m-7-7v18' }
      : { cor: 'text-red-500', icone: 'M19 14l-7 7m0 0l-7-7m7 7V3' };
  }

  // Default neutro
  return { cor: 'text-slate-400', icone: 'M5 12h14' };
};
</script>