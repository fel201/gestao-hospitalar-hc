<template>
  <button
    :class="[buttonClass, { 'cursor-not-allowed': loading }]"
    :disabled="loading || disabled"
    class="flex items-center justify-center font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out"
  >
    <span v-if="loading" class="mr-2">
      <svg class="animate-spin h-5 w-5" :class="textColorClass" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </span>
    <span v-else-if="$slots.icon" class="mr-2">
      <slot name="icon"></slot>
    </span>
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const buttonClass = computed(() => {
  if (props.disabled || props.loading) {
    return "bg-slate-700 text-slate-400";
  }

  switch (props.variant) {
    case "primary":
      return "bg-blue-600 hover:bg-blue-700 text-white";

    case "info":
      return "bg-sky-600 hover:bg-sky-700 text-white";

    case "success":
      return "bg-emerald-600 hover:bg-emerald-700 text-white";

    case "warning":
      return "bg-amber-500 hover:bg-amber-600 text-white";

    case "danger":
      return "bg-red-600 hover:bg-red-700 text-white";

    case "secondary":
      return "bg-slate-700 hover:bg-slate-600 text-white";

    default:
      return "bg-slate-700 hover:bg-slate-600 text-white";
  }
});

const textColorClass = computed(() => {
  if (props.disabled || props.loading) {
    return 'text-gray-500';
  }
  return 'text-white';
});
</script>