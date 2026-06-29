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
  <div class="min-h-screen bg-slate-100 w-full">
    <!-- cabeçalho principal -->
    <header class="bg-slate-900 text-white px-8 py-4">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold">Jornada do Paciente</h1>
          <p class="text-sm text-slate-300">
            Plataforma Integrada Assistencial
          </p>
        </div>

        <div class="text-sm">
          Perspectiva:
          <span class="font-semibold"> Paciente </span>
        </div>
      </div>
    </header>
    <!-- carregamento -->
    <div v-if="loading" class="fixed inset-0 flex items-center justify-center">
      <div class="w-10 h-10 border-4 border-slate-200 border-t-slate-700 rounded-full animate-spin" />
    </div>
    <main class="w-full px-10 py-8">
      <!-- filtros -->
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

      <!-- KPIS -->
      <DashboardKpis v-if="dashboard" :kpis="dashboard!.kpis" />

      <!-- jornada -->
      <section v-if="dashboard" class="mt-8">
        <div class="flex items-center justify-between mb-6 text-slate-700">
          <h2 class="text-xl font-bold flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            Jornada Assistencial
          </h2>
          <span class="text-sm font-medium text-slate-400">6 etapas - Cardiologia</span>
        </div>

        <div class="flex flex-row gap-6 overflow-x-auto pb-6 snap-x">
          
          <div class="bg-white rounded-xl shadow-sm border border-slate-200 min-w-[320px] max-w-[320px] snap-start border-t-4 border-t-emerald-500 p-5">
            <DashboardJourney :stage="dashboard.entrada" tipo="entrada" />
          </div>

          <div class="bg-white rounded-xl shadow-sm border border-slate-200 min-w-[320px] max-w-[320px] snap-start border-t-4 border-t-blue-500 p-5">
            <DashboardJourney :stage="dashboard.consultas" tipo="consultas" />
          </div>

          <div class="bg-white rounded-xl shadow-sm border border-slate-200 min-w-[320px] max-w-[320px] snap-start border-t-4 border-t-purple-500 p-5">
            <DashboardJourney :stage="dashboard.diagnostico" tipo="diagnostico" />
          </div>

          <div class="bg-white rounded-xl shadow-sm border border-slate-200 min-w-[320px] max-w-[320px] snap-start border-t-4 border-t-orange-500 p-5">
            <DashboardJourney :stage="dashboard.procedimentos" tipo="procedimentos" />
          </div>

          <div class="bg-white rounded-xl shadow-sm border border-slate-200 min-w-[320px] max-w-[320px] snap-start border-t-4 border-t-red-500 p-5">
            <DashboardJourney :stage="dashboard.internacao" tipo="internacao" />
          </div>

        </div>
      </section>
    </main>
  </div>
</template>
