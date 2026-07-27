<script setup lang="ts">
import { ref } from "vue";
import { onMounted } from "vue";
import api from "../services/api";
import DashboardKpis from "../components/Dashboard/DashboardKpis.vue";
import DashboardJourney from "../components/Dashboard/DashboardJourney.vue";
import DashboardFilters from "../components/Dashboard/DashboardFilters.vue";
import DashboardModuleAnalytics from "../components/Dashboard/DashboardModuleAnalytics.vue";
import type { DashboardInterface } from "../interfaces/dashboard.ts";

// são apenas placeholders
const specialty = ref("Cardiologia");
const startDate = ref("2025-01-01");
const endDate = ref("2026-06-30");

const dashboard = ref<DashboardInterface>();
const loading = ref(false);
const loadingProgress = ref(0);
const loadingMessage = ref("Carregando dados do dashboard...");

// Dicas de carregamento
const loadingMessages = [
  "Carregando dados do dashboard...",
  "Buscando indicadores...",
  "Processando métricas...",
  "Organizando informações...",
  "Quase pronto..."
];

let progressInterval: number | null = null;

const loadDashboard = async () => {
  loading.value = true;
  loadingProgress.value = 0;
  let messageIndex = 0;

  // Inicia o progresso simulado
  progressInterval = window.setInterval(() => {
    if (loadingProgress.value < 90) {
      const incremento = Math.random() * 10 + 5;
      loadingProgress.value = Math.min(loadingProgress.value + incremento, 90);
    }
    
    // Muda a mensagem a cada 2 segundos
    if (messageIndex < loadingMessages.length) {
      loadingMessage.value = loadingMessages[messageIndex];
      messageIndex++;
    }
  }, 1500);

  try {
    const response = await api.get("/api/dashboard", {
      params: {
        especialidade: specialty.value,
        data_inicio: startDate.value,
        data_fim: endDate.value,
      },
    });

    dashboard.value = response.data;
    loadingProgress.value = 100;
    loadingMessage.value = "Carregamento concluído!";
    
    // Pequeno delay para mostrar o 100%
    await new Promise(resolve => setTimeout(resolve, 300));
    
  } catch (error) {
    console.error(error);
    loadingMessage.value = "Erro ao carregar dados";
    loadingProgress.value = 0;
  } finally {
    if (progressInterval) {
      clearInterval(progressInterval);
      progressInterval = null;
    }
    loading.value = false;
  }
};

// Cleanup
const cleanup = () => {
  if (progressInterval) {
    clearInterval(progressInterval);
    progressInterval = null;
  }
};

onMounted(() => {
  loadDashboard();
});

// Também limpa quando o componente for desmontado
import { onBeforeUnmount } from "vue";
onBeforeUnmount(cleanup);
</script>

<template>
  <div class="min-h-screen bg-[#0d0f14] w-full text-slate-200">
    <main class="w-full px-10 py-8">
      <!-- Tela de carregamento -->
      <div 
        v-if="loading" 
        class="mt-10 rounded-lg border border-[#2c3140] bg-[#181c25] p-6 relative overflow-hidden"
      >
        <!-- Barra de progresso superior -->
        <div class="absolute top-0 left-0 right-0 h-1 bg-[#2c3140]">
          <div 
            class="h-full bg-[#4f8a8b] transition-all duration-500 ease-out"
            :style="{ width: loadingProgress + '%' }"
          ></div>
        </div>

        <div class="flex flex-col items-center justify-center py-12 space-y-6">
          <!-- Spinner -->
          <div class="relative">
            <div class="w-16 h-16 rounded-full border-4 border-[#2c3140] border-t-[#4f8a8b] animate-spin"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <svg class="w-6 h-6 text-[#4f8a8b] animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
          </div>

          <div class="text-center space-y-3">
            <p class="font-roboto text-[11px] uppercase tracking-[0.16em] text-[#8b8f9c]">{{ loadingMessage }}</p>
            <p class="font-roboto text-[11px] uppercase tracking-[0.16em] text-[#8b8f9c]">{{ Math.round(loadingProgress) }}% completo</p>
          </div>

          <!-- Barra de progresso detalhada -->
          <div class="w-full max-w-md">
            <div class="h-2 bg-[#2c3140] rounded-full overflow-hidden">
              <div 
                class="h-full bg-[#4f8a8b] rounded-full transition-all duration-500"
                :style="{ width: loadingProgress + '%' }"
              ></div>
            </div>
          </div>

          <!-- Indicadores de progresso -->
          <div class="flex gap-3 mt-2">
            <div 
              v-for="i in 5" 
              :key="i"
              class="w-2 h-2 rounded-full transition-all duration-300"
              :class="loadingProgress >= (i * 20) ? 'bg-[#4f8a8b]' : 'bg-[#2c3140]'"
            ></div>
          </div>
        </div>
      </div>

      <!-- Conteúdo principal -->
      <template v-if="!loading">
        <!-- Filtros -->
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

        <!-- KPIs -->
        <DashboardKpis v-if="dashboard" :kpis="dashboard!.kpis" />

        <!-- Jornada Assistencial -->
        <section v-if="dashboard" class="mt-10 rounded-lg border border-[#2c3140] bg-[#181c25] p-6">
          <div
            class="flex flex-col gap-3 border-b border-[#2c3140] pb-5 md:flex-row md:items-end md:justify-between"
          >
            <div>
              <p class="font-roboto text-[11px] uppercase tracking-[0.16em] text-[#8b8f9c]">
                Jornada Assistencial
              </p>
              <h2 class="mt-1 font-roboto text-2xl font-medium text-[#ece8df]">
                6 etapas - {{ specialty }}
              </h2>
              <p class="mt-2 max-w-2xl text-sm leading-relaxed text-[#9096a3]">
                Visualize a jornada completa do paciente, desde a entrada até a cirurgia e internação.
              </p>
            </div>
          </div>

          <div class="mt-6 flex flex-row gap-6 overflow-x-auto pb-6 snap-x">
            <div 
              v-for="(stage, index) in [
                dashboard.entrada,
                dashboard.consultas,
                dashboard.exames,
                dashboard.cirurgias,
                dashboard.internacao
              ]" 
              :key="index"
              class="min-w-[320px] max-w-[320px] snap-start"
            >
              <div class="rounded-lg border border-[#252a35] bg-[#1b1f29] p-5">
                <DashboardJourney :stage="stage" :tipo="['entrada', 'consultas', 'exames', 'procedimentos', 'internacao'][index]" />
              </div>
            </div>
          </div>
        </section>

        <!-- Módulo de Análise -->
        <DashboardModuleAnalytics v-if="dashboard" :dashboard="dashboard" />
      </template>
    </main>
  </div>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap");

.font-roboto {
  font-family: 'Roboto', sans-serif;
}

/* Animações */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-pulse {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Transição suave */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 500ms;
}

/* Scrollbar personalizada */
.snap-x {
  scroll-snap-type: x mandatory;
}

.snap-start {
  scroll-snap-align: start;
}

/* Scrollbar customizada */
::-webkit-scrollbar {
  height: 6px;
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #1e232c;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #2c3140;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #3a4052;
}
</style>