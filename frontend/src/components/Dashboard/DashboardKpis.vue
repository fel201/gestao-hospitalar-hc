<template>
  <section class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-10">
    
    <div class="bg-slate-800/80 rounded-xl p-5 border border-slate-700 shadow-sm flex items-center gap-4">
      <div class="p-3 bg-blue-500/10 text-blue-500 rounded-lg">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
      </div>
      <div>
        <p class="text-xs uppercase tracking-wider font-semibold text-slate-400 mb-1">Total de Pacientes</p>
        <h2 class="text-2xl font-bold text-slate-100">
          {{ kpis.total_pacientes }}
        </h2>
      </div>
    </div>

    <div class="bg-slate-800/80 rounded-xl p-5 border border-slate-700 shadow-sm flex items-center gap-4">
      <div class="p-3 bg-purple-500/10 text-purple-500 rounded-lg">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
      </div>
      <div>
        <p class="text-xs uppercase tracking-wider font-semibold text-slate-400 mb-1">Total de Eventos</p>
        <h2 class="text-2xl font-bold text-slate-100">
          {{ kpis.total_eventos }}
        </h2>
      </div>
    </div>

    <div class="bg-slate-800/80 rounded-xl p-5 border border-slate-700 shadow-sm flex items-center gap-4">
      <div class="p-3 bg-orange-500/10 text-orange-500 rounded-lg">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
      </div>
      <div>
        <p class="text-xs uppercase tracking-wider font-semibold text-slate-400 mb-1">Tempo Médio de Jornada</p>
        <h2 class="text-2xl font-bold text-slate-100">
          {{ kpis.tempo_medio_jornada }} dias
        </h2>
      </div>
    </div>

    <div class="bg-slate-800/80 rounded-xl p-5 border border-slate-700 shadow-sm flex items-center gap-4">
      <div class="p-3 bg-emerald-500/10 text-emerald-500 rounded-lg">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
      </div>
      <div>
        <p class="text-xs uppercase tracking-wider font-semibold text-slate-400 mb-1">Taxa de Conclusão</p>
        <h2 class="text-2xl font-bold text-slate-100">
          {{ (kpis.taxa_conclusao * 100).toFixed(0) }}%
        </h2>
      </div>
    </div>

  </section>
</template>

<script setup lang="ts">
import type { DashboardKPIsInterface } from "../../interfaces/dashboard.ts";

defineProps<{
  kpis: DashboardKPIsInterface;
}>();
</script>