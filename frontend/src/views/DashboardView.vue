<script setup lang="ts">
import { ref } from 'vue'

interface StageIndicator {
  label: string
  value: string | number
}

interface StageEvent {
  label: string
  value: number
}

interface JourneyStage {
  id: number
  title: string
  subtitle: string
  totalEvents: number
  events: StageEvent[]
  indicators: StageIndicator[]
}
// são apenas placeholders

const specialty = ref('Cardiologia')
const startDate = ref('2024-01-01')
const endDate = ref('2024-06-30')

const stages = ref<JourneyStage[]>([
  {
    id: 1,
    title: 'Entrada',
    subtitle: 'Abertura de Prontuário',
    totalEvents: 1517,
    events: [
      { label: 'Criação de prontuário', value: 1240 },
      { label: 'Cadastro emergência', value: 183 },
      { label: 'Transferência externa', value: 94 }
    ],
    indicators: [
      { label: 'Tempo médio cadastro', value: '12 min' },
      { label: 'Origem ambulatorial', value: '68%' },
      { label: 'Pacientes novos', value: '342' }
    ]
  },
  {
    id: 2,
    title: 'Consultas',
    subtitle: 'Atendimento Ambulatorial',
    totalEvents: 3605,
    events: [
      { label: 'Consulta ambulatorial', value: 2183 },
      { label: 'Retorno ambulatorial', value: 891 },
      { label: 'Teleconsulta', value: 214 },
      { label: 'Consulta urgência', value: 317 }
    ],
    indicators: [
      { label: 'Tempo médio espera', value: '38 min' },
      { label: 'Taxa de retorno', value: '42%' },
      { label: 'Consultas / paciente', value: '2.8' }
    ]
  }
])
</script>

<template>
  <div class="min-h-screen bg-slate-100">
    
    <!-- cabeçalho principal -->
    <header class="bg-slate-900 text-white px-8 py-4">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold">
            Jornada do Paciente
          </h1>
          <p class="text-sm text-slate-300">
            Plataforma Integrada Assistencial
          </p>
        </div>

        <div class="text-sm">
          Perspectiva:
          <span class="font-semibold">
            Paciente
          </span>
        </div>
      </div>
    </header>

    <main class="p-8">

      <!-- filtros -->
      <section
        class="bg-white rounded-2xl p-6 shadow mb-6"
      >
        <div class="grid grid-cols-4 gap-4">

          <div>
            <label class="text-xs uppercase text-gray-500">
              Especialidade
            </label>

            <select
              v-model="specialty"
              class="w-full border rounded-lg p-3"
            >
              <option>Cardiologia</option>
              <option>Neurologia</option>
              <option>Ortopedia</option>
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
            <label class="text-xs uppercase text-gray-500">
              Data Final
            </label>

            <input
              v-model="endDate"
              type="date"
              class="w-full border rounded-lg p-3"
            />
          </div>

          <div class="flex items-end">
            <button
              class="w-full bg-blue-900 text-white rounded-lg p-3 font-semibold"
            >
              Aplicar Filtros
            </button>
          </div>

        </div>
      </section>

      <!-- KPIS -->
      <section
        class="grid grid-cols-4 gap-4 mb-8"
      >
        <div class="bg-white rounded-2xl p-5 shadow">
          <p class="text-sm text-gray-500">
            Total de Pacientes
          </p>

          <h2 class="text-3xl font-bold">
            1.240
          </h2>
        </div>

        <div class="bg-white rounded-2xl p-5 shadow">
          <p class="text-sm text-gray-500">
            Total de Eventos
          </p>

          <h2 class="text-3xl font-bold">
            10.797
          </h2>
        </div>

        <div class="bg-white rounded-2xl p-5 shadow">
          <p class="text-sm text-gray-500">
            Tempo Médio da Jornada
          </p>

          <h2 class="text-3xl font-bold">
            47 dias
          </h2>
        </div>

        <div class="bg-white rounded-2xl p-5 shadow">
          <p class="text-sm text-gray-500">
            Taxa de Conclusão
          </p>

          <h2 class="text-3xl font-bold">
            78%
          </h2>
        </div>
      </section>

      <!-- jornada -->
      <section>
        <h2
          class="text-xl font-bold mb-4"
        >
          Jornada Assistencial
        </h2>

        <div
          class="flex gap-6 overflow-x-auto pb-4"
        >
          <div
            v-for="stage in stages"
            :key="stage.id"
            class="bg-white rounded-2xl shadow min-w-[320px] p-5"
          >
            <div
              class="flex justify-between mb-4"
            >
              <div>
                <p class="text-sm text-gray-500">
                  {{ stage.subtitle }}
                </p>

                <h3 class="font-bold text-xl">
                  {{ stage.title }}
                </h3>
              </div>

              <div class="text-right">
                <span
                  class="font-bold text-2xl"
                >
                  {{ stage.totalEvents }}
                </span>

                <p class="text-xs text-gray-500">
                  eventos
                </p>
              </div>
            </div>

            <div class="mb-5">
              <h4
                class="font-semibold text-sm uppercase mb-3"
              >
                Eventos
              </h4>

              <div
                v-for="event in stage.events"
                :key="event.label"
                class="flex justify-between py-1"
              >
                <span>
                  {{ event.label }}
                </span>

                <span class="font-semibold">
                  {{ event.value }}
                </span>
              </div>
            </div>

            <div>
              <h4
                class="font-semibold text-sm uppercase mb-3"
              >
                Indicadores
              </h4>

              <div
                v-for="indicator in stage.indicators"
                :key="indicator.label"
                class="flex justify-between py-1"
              >
                <span>
                  {{ indicator.label }}
                </span>

                <span class="font-semibold">
                  {{ indicator.value }}
                </span>
              </div>
            </div>

          </div>
        </div>
      </section>

    </main>
  </div>
</template>