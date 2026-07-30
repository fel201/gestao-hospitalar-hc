<template>
  <div class="rounded-lg border border-[#2c3140] bg-[#181c25] shadow-lg">
    <div v-if="$slots.header" class="p-4 border-b border-[#2c3140] bg-[#15181f]">
      <slot name="header"></slot>
    </div>
    <div class="p-6">
      <slot></slot>
    </div>
    <div v-if="$slots.footer" class="p-4 border-t border-[#2c3140] bg-[#15181f]">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
/* Garante consistência com o tema do DashboardModuleAnalytics */
.rounded-lg {
  border-radius: 0.5rem;
}

.border-\[\#2c3140\] {
  border-color: #2c3140;
}

.bg-\[\#181c25\] {
  background-color: #181c25;
}

.bg-\[\#15181f\] {
  background-color: #15181f;
}
</style>