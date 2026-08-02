<template>
  <section class="mb-10 grid grid-cols-1 gap-5 md:grid-cols-3">
    <div
      v-for="kpi in kpisResolvidos"
      :key="kpi.label"
      class="relative overflow-hidden rounded-md border border-[#2c3140] bg-[#181c25] p-5 pl-6"
    >
      <span
        class="absolute inset-y-0 left-0 w-[3px]"
        :style="{ backgroundColor: kpi.cor }"
      />
      <div class="flex items-center gap-4">
        <div
          class="flex h-11 w-11 shrink-0 items-center justify-center rounded-md border"
          :style="{ borderColor: kpi.cor + '55', color: kpi.cor }"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="kpi.icone"></path>
          </svg>
        </div>
        <div>
          <p class="mb-1 font-mono text-[10px] uppercase tracking-[0.14em] text-[#8b8f9c]">
            {{ kpi.label }}
          </p>
          <h2 class="font-serif text-2xl font-semibold leading-none text-[#ece8df]">
            {{ kpi.valor }}
          </h2>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { DashboardKPIsInterface } from "../../interfaces/dashboard.ts";

const props = defineProps<{
  kpis: DashboardKPIsInterface;
}>();

// Mesma paleta de identidade usada no fluxo assistencial e no Journey.
// Aqui os KPIs são agregados (não pertencem a um módulo só), então a cor
// serve para diferenciar os cartões visualmente, sem alegar um vínculo
// direto com uma etapa específica.
const kpisResolvidos = computed(() => [
  {
    label: "Total de Pacientes",
    valor: props.kpis.total_pacientes,
    cor: "#4f8a8b",
    icone:
      "M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z",
  },
  {
    label: "Total de Eventos",
    valor: props.kpis.total_eventos,
    cor: "#c99a3e",
    icone: "M13 10V3L4 14h7v7l9-11h-7z",
  },
  {
    label: "Taxa de Conclusão",
    valor: `${(props.kpis.taxa_conclusao * 100).toFixed(0)}%`,
    cor: "#5a7599",
    icone: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z",
  },
]);
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