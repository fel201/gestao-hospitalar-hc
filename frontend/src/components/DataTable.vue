<template>
  <div class="w-full overflow-x-auto rounded-xl border border-slate-700">
    <table class="w-full">
      <thead class="bg-slate-950">
        <tr
          class="text-xs font-semibold uppercase tracking-wider text-slate-400 border-b border-slate-700"
        >
          <th
            v-for="header in headers"
            :key="header.value"
            class="px-5 py-4 text-left"
          >
            {{ header.text }}
          </th>

          <th
            v-if="$slots.actions"
            class="px-5 py-4 text-left"
          >
            Ações
          </th>
        </tr>
      </thead>

      <tbody class="bg-slate-800 divide-y divide-slate-700">
        <tr
          v-for="item in items"
          :key="item.id"
          class="hover:bg-slate-700 transition-colors"
        >
          <td
            v-for="header in headers"
            :key="header.value"
            class="px-5 py-4 text-sm text-slate-200"
          >
            {{ item[header.value] }}
          </td>

          <td
            v-if="$slots.actions"
            class="px-5 py-4"
          >
            <slot
              name="actions"
              :item="item"
            />
          </td>
        </tr>

        <tr v-if="items.length === 0">
          <td
            :colspan="headers.length + ($slots.actions ? 1 : 0)"
            class="px-6 py-8 text-center text-slate-400"
          >
            Nenhum dado encontrado.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
interface Header {
  text: string;
  value: string;
}

interface Item {
  id: number | string;
  [key: string]: any;
}

defineProps({
  headers: {
    type: Array as () => Header[],
    required: true,
  },
  items: {
    type: Array as () => Item[],
    required: true,
  },
});
</script>