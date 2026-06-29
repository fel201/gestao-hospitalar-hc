<template>
  <section class="bg-slate-800/80 border border-slate-700 rounded-xl p-6 shadow-sm mb-8">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      
      <div>
        <label class="block text-[11px] uppercase tracking-wider font-bold text-slate-400 mb-2">Especialidade</label>
        <div class="relative">
          <select
            :value="specialty"
            class="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded-lg p-3 appearance-none focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors cursor-pointer"
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
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-400">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </div>
        </div>
      </div>

      <div>
        <label class="block text-[11px] uppercase tracking-wider font-bold text-slate-400 mb-2">Data Inicial</label>
        <input
          :value="startDate"
          class="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded-lg p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors [color-scheme:dark] cursor-pointer"
          type="date"
          @input="emit('update:startDate', ($event.target as HTMLInputElement).value)"
        />
      </div>

      <div>
        <label class="block text-[11px] uppercase tracking-wider font-bold text-slate-400 mb-2">Data Final</label>
        <input
          :value="endDate"
          class="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded-lg p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors [color-scheme:dark] cursor-pointer"  
          type="date"
          @input="emit('update:endDate', ($event.target as HTMLInputElement).value)"
        />
      </div>

      <div class="flex items-end">
        <button 
          class="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg p-3 font-semibold transition-colors flex items-center justify-center gap-2 shadow-sm" 
          @click="emit('search')"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>
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