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
  <div class="min-h-screen bg-slate-900 w-full font-sans text-slate-200">
    
    <main class="w-full px-10 py-8">
      <!-- Tela de carregamento -->
      <div v-if="loading" class="bg-slate-800/90 backdrop-blur-sm rounded-xl border border-slate-700 p-8 relative overflow-hidden">
        <!-- Barra de progresso superior -->
        <div class="absolute top-0 left-0 right-0 h-1 bg-slate-700">
          <div 
            class="h-full bg-linear-to-r from-red-600 to-red-400 transition-all duration-500 ease-out"
            :style="{ width: loadingProgress + '%' }"
          ></div>
        </div>

        <div class="flex flex-col items-center justify-center py-12 space-y-6">
          <!-- Spinner com ícone -->
          <div class="relative">
            <div class="w-16 h-16 rounded-full border-4 border-slate-700 border-t-red-500 animate-spin"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <svg class="w-6 h-6 text-red-400 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
          </div>

          <div class="text-center space-y-3">
            <p class="text-lg font-medium text-white">{{ loadingMessage }}</p>
            <p class="text-sm text-slate-400">{{ Math.round(loadingProgress) }}% completo</p>
          </div>

          <!-- Barra de progresso detalhada -->
          <div class="w-full max-w-md">
            <div class="h-2 bg-slate-700 rounded-full overflow-hidden">
              <div 
                class="h-full bg-linear-to-r from-red-600 to-red-400 rounded-full transition-all duration-500"
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
              :class="loadingProgress >= (i * 20) ? 'bg-red-500' : 'bg-slate-600'"
            ></div>
          </div>
        </div>
      </div>

      <!-- Conteúdo principal (aparece quando não está carregando) -->
      <template v-if="!loading">
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
              <DashboardJourney :stage="dashboard.exames" tipo="exames" />
            </div>

            <div class="bg-slate-800/80 rounded-xl shadow-lg border border-slate-700 min-w-[320px] max-w-[320px] snap-start border-t-4 border-t-blue-900 p-5">
              <DashboardJourney :stage="dashboard.cirurgias" tipo="procedimentos" />
            </div>

            <div class="bg-slate-800/80 rounded-xl shadow-lg border border-slate-700 min-w-[320px] max-w-[320px] snap-start border-t-4 border-t-blue-900 p-5">
              <DashboardJourney :stage="dashboard.internacao" tipo="internacao" />
            </div>

          </div>
        </section>
      </template>
    </main>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  height: 8px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #1e293b;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #475569;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #64748b;
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

.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>