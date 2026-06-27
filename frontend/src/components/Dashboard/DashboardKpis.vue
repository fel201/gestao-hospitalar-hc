<template>
  <section class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-10">
    <div class="bg-white rounded-2xl p-5 shadow">
      <p class="text-sm text-gray-500">Total de Pacientes</p>

      <h2 class="text-3xl font-bold">
        {{ kpis.total_pacientes }}
      </h2>
    </div>

    <div class="bg-white rounded-2xl p-5 shadow">
      <p class="text-sm text-gray-500">Total de Eventos</p>

      <h2 class="text-3xl font-bold">
        {{ kpis.total_eventos }}
      </h2>
    </div>

    <div class="bg-white rounded-2xl p-5 shadow">
      <p class="text-sm text-gray-500">Tempo Médio da Jornada</p>

      <h2 class="text-3xl font-bold">
        {{ kpis.tempo_medio_jornada }} dias
      </h2>
    </div>

    <div class="bg-white rounded-2xl p-5 shadow">
      <p class="text-sm text-gray-500">Taxa de Conclusão</p>

      <h2 class="text-3xl font-bold">
        {{ (kpis.taxa_conclusao * 100).toFixed(0) }}%
      </h2>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { DashboardKPIsInterface } from "../../interfaces/dashboard.js";

defineProps<{
  kpis: DashboardKPIsInterface;
}>();
</script>