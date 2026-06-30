<template>
  <div class="flex flex-col h-full w-full bg-transparent">
    
    <div class="flex justify-between items-start mb-6">
      <div class="flex items-center gap-3">
        <div class="p-2 rounded-full bg-blue-900/30 text-blue-400">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="config.icone"></path>
          </svg>
        </div>
        <div>
          <p class="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">{{ config.subtitulo }}</p>
          <h3 class="text-lg font-bold text-slate-100">{{ config.titulo }}</h3>
        </div>
      </div>
      <div class="text-right">
        <p class="text-xl font-bold text-blue-400">{{ stage?.total_eventos || 0 }}</p>
        <p class="text-[10px] text-slate-500 uppercase tracking-wider">eventos</p>
      </div>
    </div>

    <div class="mb-6">
      <p class="text-[11px] text-slate-500 uppercase tracking-wider font-bold mb-3">Eventos</p>
      
      <div class="space-y-4">
        <div v-for="(evento, index) in stage?.eventos" :key="index">
          <div class="flex justify-between text-sm mb-1">
            <span class="text-slate-400 font-medium">{{ evento.nome }}</span>
            <span class="font-bold text-slate-200">{{ evento.valor }}</span>
          </div>
          <div class="h-0.5 w-full bg-slate-700/50 rounded">
            <div class="h-0.5 rounded bg-blue-600" :style="{ width: evento.porcentagem || '50%' }"></div>
          </div>
        </div>
        
        <div v-if="!stage?.eventos || stage?.eventos.length === 0" class="text-sm text-slate-600 italic">
          Nenhum evento registrado.
        </div>
      </div>
    </div>

    <div>
      <p class="text-[11px] text-slate-500 uppercase tracking-wider font-bold mb-3">Indicadores</p>
      
      <div class="space-y-2">
        <div v-for="(indicador, index) in stage?.indicadores" :key="index" class="flex justify-between items-center text-sm">
          <span class="text-slate-400">{{ indicador.nome }}</span>
          <div class="flex items-center gap-2">
            <span class="font-bold text-slate-200">{{ indicador.valor }}</span>
            
            <span v-if="indicador.variacao" :class="['text-xs font-semibold flex items-center', avaliarIndicador(indicador).cor]">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="avaliarIndicador(indicador).icone"></path>
              </svg>
              {{ indicador.variacao }}
            </span>
          </div>
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

// 1. O mapa agora apenas devolve os textos e os SVGs corretos, sem misturar cores vibrantes.
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

// 2. A inteligência que define se uma métrica está Crítica (Vermelho), Alerta (Amarelo) ou Boa (Verde)
const avaliarIndicador = (indicador: any) => {
  // O ideal é que a sua API (no Python/FastAPI) mande um campo "status" junto com o indicador.
  // Ex: { nome: 'Tempo de espera', valor: '38 min', variacao: '+5 min', status: 'ruim' }
  
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