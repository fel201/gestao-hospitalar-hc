<template>
        <div class="flex justify-between mb-4">
          <div>

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
              {{ formatMetric(indicator.nome, indicator.valor) }}
            </span>
          </div>
        </div>
</template>

<script setup lang="ts">
import type { DashboardModuloInterface } from '../../interfaces/dashboard';

function formatMetric(nome: string, valor: number): string {
  const n = nome.toLowerCase()
  if (n.includes('proporção') || n.includes('taxa'))
    return `${(valor * 100).toFixed(1)}%`
  if (n.includes('min') || n.includes('tempo'))
    return `${Math.round(valor)} min`
  if (Number.isInteger(valor) || valor > 10)
    return valor.toLocaleString('pt-BR')
  return valor.toFixed(2).replace('.', ',')
}
defineProps<{
  stage: DashboardModuloInterface
}>();

</script>