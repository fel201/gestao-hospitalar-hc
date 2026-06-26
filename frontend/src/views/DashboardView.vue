<script setup lang="ts">
import { ref } from "vue";
import { onMounted } from "vue";
import api from "../services/api";
interface StageIndicator {
  label: string;
  value: string | number;
}

interface StageEvent {
  label: string;
  value: number;
}

interface JourneyStage {
  id: number;
  title: string;
  subtitle: string;
  totalEvents: number;
  events: StageEvent[];
  indicators: StageIndicator[];
}
// são apenas placeholders

const specialty = ref("Cardiologia");
const startDate = ref("2024-01-01");
const endDate = ref("2024-06-30");

const dashboard = ref(null);
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
      <section class="bg-white rounded-2xl p-8 shadow-sm mb-8">
        <div class="grid grid-cols-4 gap-4">
          <div>
            <label class="text-xs uppercase text-gray-500">
              Especialidade
            </label>

            <select v-model="specialty" class="w-full border rounded-lg p-3">
              <option>Cardiologia</option>
              <option>Neurologia</option>
              <option>Ortopedia</option>
              <option>Nutrição</option>
              <option>Nefrologia</option>
              <option>Oncologia</option>
              <option>Psiquiatria</option>
              <option>Urologia</option>
              <option>Pneumologia</option>
              <option>Gastroenterologia</option>
              <option>Ginecologia</option>
              <option>Endocrinologia</option>
            </select>
          </div>

          <div>
            <label class="text-xs uppercase text-gray-500">
              Data Inicial
            </label>

            <input
              v-model="startDate"
              type="date"
              class="w-full border rounded-lg p-3"
            />
          </div>

          <div>
            <label class="text-xs uppercase text-gray-500"> Data Final </label>

            <input
              v-model="endDate"
              type="date"
              class="w-full border rounded-lg p-3"
            />
          </div>

          <div class="flex items-end">
            <button
              @click="loadDashboard"
              class="w-full bg-blue-900 text-white rounded-lg p-3 font-semibold"
            >
              Aplicar Filtros
            </button>
          </div>
        </div>
      </section>

      <!-- KPIS -->
      <section
        class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-10"
      >
        <div class="bg-white rounded-2xl p-5 shadow">
          <p class="text-sm text-gray-500">Total de Pacientes</p>

          <h2 class="text-3xl font-bold">
            {{ dashboard?.kpis.total_pacientes ?? 0 }}
          </h2>

        </div>

        <div class="bg-white rounded-2xl p-5 shadow">
          <p class="text-sm text-gray-500">Total de Eventos</p>

          <h2 class="text-3xl font-bold">
            {{ dashboard?.kpis.total_eventos ?? 0 }}
          </h2>
        </div>

        <div class="bg-white rounded-2xl p-5 shadow">
          <p class="text-sm text-gray-500">Tempo Médio da Jornada</p>

          <h2 class="text-3xl font-bold">
            {{ dashboard?.kpis.tempo_medio_jornada ?? 0 }} dias
          </h2>
        </div>

        <div class="bg-white rounded-2xl p-5 shadow">
          <p class="text-sm text-gray-500">Taxa de Conclusão</p>

          <h2 class="text-3xl font-bold">
            {{ ((dashboard?.kpis.taxa_conclusao ?? 0) * 100).toFixed(0) }}%
          </h2>
        </div>
      </section>

      <!-- jornada -->
      <section>
        <h2 class="text-xl font-bold mb-4">Jornada Assistencial</h2>

        <div class="flex gap-6 overflow-x-auto pb-4">
          <div
            v-for="stage in dashboard?.etapas"
            :key="stage.id"
            class="bg-white rounded-2xl shadow min-w-[320px] p-5"
          >
            <div class="flex justify-between mb-4">
              <div>
                <p class="text-sm text-gray-500">
                  {{ stage.subtitle }}
                </p>

                <h3 class="font-bold text-2xl">
                  {{ stage.titulo }}
                </h3>
              </div>

              <div class="text-right">
                <span class="font-bold text-3xl">
                  {{ stage.total_eventos }}
                </span>

                <p class="text-xs text-gray-500">eventos</p>
              </div>
            </div>

            <div class="mb-5">
              <h4 class="font-semibold text-sm uppercase mb-3">Eventos</h4>

              <div
                v-for="event in stage.eventos"
                :key="event.nome"
                class="flex justify-between py-1"
              >
                <span>
                  {{ event.nome }}
                </span>

                <span class="font-semibold">
                  {{ event.valor }}
                </span>
              </div>
            </div>

            <div>
              <h4 class="font-semibold text-sm uppercase mb-3">Indicadores</h4>

              <div
                v-for="indicator in stage.indicadores"
                :key="indicator.nome"
                class="flex justify-between py-1"
              >
                <span>
                  {{ indicator.nome }}
                </span>

                <span class="font-semibold">
                  {{ indicator.valor }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>
