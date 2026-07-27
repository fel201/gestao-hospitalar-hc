<template>
  <teleport to="body">
    <!-- Overlay com Blur -->
    <transition name="fade">
      <div 
        v-if="show" 
        class="fixed inset-0 bg-[#0d0f14]/80 backdrop-blur-sm z-40 transition-opacity" 
        @click="close"
      ></div>
    </transition>

    <!-- Container do Modal -->
    <transition name="modal-scale">
      <div 
        v-if="show" 
        class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6"
      >
        <div 
          class="rounded-lg border border-[#2c3140] bg-[#181c25] shadow-2xl w-full max-w-lg overflow-hidden transform transition-all"
          @click.stop
        >
          <!-- Header -->
          <div class="px-6 py-4 border-b border-[#2c3140] flex justify-between items-center bg-[#15181f]">
            <h2 class="text-xl font-roboto font-medium text-[#ece8df]">
              <slot name="header">Título do Modal</slot>
            </h2>
            <button 
              @click="close" 
              class="p-2 rounded-full text-[#8b8f9c] hover:text-[#ece8df] hover:bg-[#1b1f29] transition-colors"
            >
              <XMarkIcon class="h-6 w-6" />
            </button>
          </div>

          <!-- Body -->
          <div class="px-6 py-6 text-[#8b8f9c] font-roboto leading-relaxed">
            <slot></slot>
          </div>

          <!-- Footer -->
          <div v-if="$slots.footer" class="px-6 py-4 border-t border-[#2c3140] bg-[#15181f] flex justify-end space-x-3">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, watch } from 'vue';
import { XMarkIcon } from '@heroicons/vue/24/outline';

const props = defineProps({
  show: { type: Boolean, default: false },
});

const emit = defineEmits(['close']);
const close = () => emit('close');

// Bloqueia o scroll do corpo quando o modal abre
watch(() => props.show, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});

const handleEscape = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && props.show) close();
};

onMounted(() => document.addEventListener('keydown', handleEscape));
onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape);
  document.body.style.overflow = ''; // Garante limpeza no unmount
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap");

.font-roboto {
  font-family: 'Roboto', sans-serif;
}

/* Animações de transição */
.fade-enter-active, 
.fade-leave-active { 
  transition: opacity 0.2s ease; 
}

.fade-enter-from, 
.fade-leave-to { 
  opacity: 0; 
}

.modal-scale-enter-active { 
  transition: all 0.3s ease-out; 
}

.modal-scale-leave-active { 
  transition: all 0.2s ease-in; 
}

.modal-scale-enter-from { 
  opacity: 0; 
  transform: scale(0.95) translateY(-10px); 
}

.modal-scale-leave-to { 
  opacity: 0; 
  transform: scale(0.95) translateY(10px); 
}

/* Hover effects */
.hover\:bg-\[\#1b1f29\]:hover {
  background-color: #1b1f29;
}

.hover\:text-\[\#ece8df\]:hover {
  color: #ece8df;
}
</style>