<script setup lang="ts">
import { ref } from "vue";
import { onMounted } from "vue";
import api from "../services/api";
import DashboardKpis from "../components/Dashboard/DashboardKpis.vue";
import DashboardJourney from "../components/Dashboard/DashboardJourney.vue";
import DashboardFilters from "../components/Dashboard/DashboardFilters.vue";
import type {
  DashboardInterface
} from "../interfaces/dashboard.ts";

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
      <section v-if="dashboard">
        <h2 class="text-xl font-bold mb-4">Jornada Assistencial</h2>

        <div class="flex flex-col gap-6 pr-4 h-[400px]">
          <div
            v-for="stage in dashboard?.etapas"
            :key="stage.id"
            class="bg-white rounded-2xl shadow min-w-[320px] p-5"
          >
            <DashboardJourney :stage="stage" />
          </div>
        </div>
      </section>
    </main>
  </div>
</template>
