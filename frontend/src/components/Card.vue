<template>
  <div class="mt-10 bg-slate-800 border border-slate-700 rounded-xl shadow-lg">
    <div v-if="$slots.header" class="p-4">
      <slot name="header"></slot>
    </div>
    <div class="p-6">
      <slot></slot>
    </div>
    <div v-if="$slots.footer" class="p-4">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>
