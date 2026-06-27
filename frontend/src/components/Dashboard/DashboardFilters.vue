<template>
  <section class="bg-white rounded-2xl p-8 shadow-sm mb-8">
    <div class="grid grid-cols-4 gap-4">
      <div>
        <label class="text-xs uppercase text-gray-500"> Especialidade </label>

        <select
          :value="specialty"
          class="w-full border rounded-lg p-3"
          @change="
            emit('update:specialty', ($event.target as HTMLSelectElement).value)
          "
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
      </div>

      <div>
        <label class="text-xs uppercase text-gray-500"> Data Inicial </label>
        <input
          :value="startDate"
          class="w-full border rounded-lg p-3"
          type="date"
          @input="
            emit('update:startDate', ($event.target as HTMLInputElement).value)
          "
        />
      </div>

      <div>
        <label class="text-xs uppercase text-gray-500"> Data Final </label>

        <input
          :value="endDate"
          class="w-full border rounded-lg p-3"  
          type="date"
          @input="
            emit('update:endDate', ($event.target as HTMLInputElement).value)
          "
        />
      </div>

      <div class="flex items-end">
        <button class="w-full bg-blue-900 text-white rounded-lg p-3 font-semibold" @click="emit('search')">Aplicar Filtros</button>
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
