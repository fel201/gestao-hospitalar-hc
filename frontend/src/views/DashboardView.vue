<script setup lang="ts">
import { ref } from "vue";
import { onMounted } from "vue";
import api from "../services/api";
import DashboardKpis from "../components/Dashboard/DashboardKpis.vue";
import DashboardJourney from "../components/Dashboard/DashboardJourney.vue";
import DashboardFilters from "../components/Dashboard/DashboardFilters.vue";
import type { DashboardInterface } from "../interfaces/dashboard.ts";

// são apenas placeholders

const specialty = ref("Cardiologia");
const startDate = ref("2024-01-01");
const endDate = ref("2024-06-30");

const dashboard = ref<DashboardInterface>();
const loading = ref(false);

const loadDashboard = async () => {
  loading.value = true;

  try {
    const response = await api.get("/api/dashboard", {
      params: {
        especialidade: specialty.value,
        data_inicio: startDate.value,
        data_fim: endDate.value,
      },
    });

    dashboard.value = response.data;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadDashboard();
});
</script>

<template>
  <div class="min-h-screen bg-slate-900 w-full font-sans text-slate-200">
    
    <!-- cabeçalho-->
    <header class="bg-slate-950 text-white px-8 py-5 border-b border-slate-800 shadow-sm">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold tracking-tight">Dashboard Assistencial</h1>
          <p class="text-sm text-slate-400 mt-1">
            Plataforma Integrada Assistencial
          </p>
        </div>

        <div class="text-sm text-slate-400 bg-slate-900 px-4 py-2 rounded-full border border-slate-700">
          Perspectiva:
          <span class="font-semibold text-white ml-1"> Paciente </span>
        </div>
      </div>
    </header>

    <div v-if="loading" class="fixed inset-0 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm z-50">
      <div class="w-10 h-10 border-4 border-slate-600 border-t-blue-500 rounded-full animate-spin" />
    </div>

    <main class="w-full px-10 py-8">
      <DashboardFilters
        v-if="dashboard"
        :specialty="specialty"
        :start-date="startDate"
        :end-date="endDate"
        @update:specialty="specialty = $event"
        @update:start-date="startDate = $event"
        @update:end-date="endDate = $event"
        @search="loadDashboard"
      />

      <DashboardKpis v-if="dashboard" :kpis="dashboard!.kpis" />

      <!-- dashboard-->
      <section v-if="dashboard" class="mt-8">
        <div class="flex items-center justify-between mb-6 text-slate-200">
          <h2 class="text-xl font-bold flex items-center gap-2">
            <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            Jornada Assistencial
          </h2>
          <span class="text-sm font-medium text-slate-500">6 etapas - {{ specialty }}</span>
        </div>

        <div class="flex flex-row gap-6 overflow-x-auto pb-6 snap-x custom-scrollbar">
          
          <div class="bg-slate-800/80 rounded-xl shadow-lg border border-slate-700 min-w-[320px] max-w-[320px] snap-start border-t-4 border-t-blue-900 p-5">
            <DashboardJourney :stage="dashboard.entrada" tipo="entrada" />
          </div>

          <div class="bg-slate-800/80 rounded-xl shadow-lg border border-slate-700 min-w-[320px] max-w-[320px] snap-start border-t-4 border-t-blue-900 p-5">
            <DashboardJourney :stage="dashboard.consultas" tipo="consultas" />
          </div>

          <div class="bg-slate-800/80 rounded-xl shadow-lg border border-slate-700 min-w-[320px] max-w-[320px] snap-start border-t-4 border-t-blue-900 p-5">
            <DashboardJourney :stage="dashboard.diagnostico" tipo="diagnostico" />
          </div>

          <div class="bg-slate-800/80 rounded-xl shadow-lg border border-slate-700 min-w-[320px] max-w-[320px] snap-start border-t-4 border-t-blue-900 p-5">
            <DashboardJourney :stage="dashboard.procedimentos" tipo="procedimentos" />
          </div>

          <div class="bg-slate-800/80 rounded-xl shadow-lg border border-slate-700 min-w-[320px] max-w-[320px] snap-start border-t-4 border-t-blue-900 p-5">
            <DashboardJourney :stage="dashboard.internacao" tipo="internacao" />
          </div>

        </div>
      </section>
    </main>
  </div>
</template>

<!-- style para tema escuro-->
<style scoped>

.custom-scrollbar::-webkit-scrollbar {
  height: 8px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #1e293b; /* slate-800 */
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #475569; /* slate-600 */
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #64748b; /* slate-500 */
}
</style>