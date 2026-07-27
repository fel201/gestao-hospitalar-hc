<template>
  <section class="mb-8 rounded-md border border-[#2c3140] bg-[#181c25] p-6">
    <div class="grid grid-cols-1 gap-6 md:grid-cols-4">

      <div>
        <label class="mb-2 block font-mono text-[10px] font-semibold uppercase tracking-[0.14em] text-[#8b8f9c]">
          Especialidade
        </label>
        <div class="relative">
          <select
            :value="specialty"
            class="w-full cursor-pointer appearance-none rounded-md border border-[#2c3140] bg-[#12151c] p-3 text-[#ece8df] transition-colors focus:border-[#c99a3e] focus:outline-none focus:ring-1 focus:ring-[#c99a3e]"
            @change="emit('update:specialty', ($event.target as HTMLSelectElement).value)"
          >
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
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-[#767c8a]">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </div>
        </div>
      </div>

      <div>
        <label class="mb-2 block font-mono text-[10px] font-semibold uppercase tracking-[0.14em] text-[#8b8f9c]">
          Data Inicial
        </label>
        <input
          :value="startDate"
          class="w-full cursor-pointer rounded-md border border-[#2c3140] bg-[#12151c] p-3 text-[#ece8df] transition-colors [color-scheme:dark] focus:border-[#c99a3e] focus:outline-none focus:ring-1 focus:ring-[#c99a3e]"
          type="date"
          @input="emit('update:startDate', ($event.target as HTMLInputElement).value)"
        />
      </div>

      <div>
        <label class="mb-2 block font-mono text-[10px] font-semibold uppercase tracking-[0.14em] text-[#8b8f9c]">
          Data Final
        </label>
        <input
          :value="endDate"
          class="w-full cursor-pointer rounded-md border border-[#2c3140] bg-[#12151c] p-3 text-[#ece8df] transition-colors [color-scheme:dark] focus:border-[#c99a3e] focus:outline-none focus:ring-1 focus:ring-[#c99a3e]"
          type="date"
          @input="emit('update:endDate', ($event.target as HTMLInputElement).value)"
        />
      </div>

      <div class="flex items-end">
        <button
          class="flex w-full items-center justify-center gap-2 rounded-md border border-[#c99a3e] bg-[#c99a3e]/10 p-3 font-mono text-sm font-semibold uppercase tracking-[0.06em] text-[#e0bd75] transition-colors hover:bg-[#c99a3e]/20"
          @click="emit('search')"
        >
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path>
          </svg>
          Aplicar Filtros
        </button>
      </div>

    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  specialty: string;
  startDate: string;
  endDate: string;
}>();
const emit = defineEmits<{
  (e: "update:specialty", value: string): void;
  (e: "update:startDate", value: string): void;
  (e: "update:endDate", value: string): void;
  (e: "search"): void;
}>();
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap");

.font-mono {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
}
</style>