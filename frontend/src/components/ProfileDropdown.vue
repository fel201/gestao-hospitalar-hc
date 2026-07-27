<template>
  <div class="relative">
    <!-- Botão do avatar -->
    <button 
      @click="isOpen = !isOpen" 
      class="relative z-10 block h-10 w-10 rounded-full overflow-hidden border border-[#2c3140] focus:outline-none focus:border-[#4f8a8b] transition-transform active:scale-95 hover:border-[#4f8a8b]"
    >
      <UserCircleIcon class="h-full w-full text-[#8b8f9c]" />
    </button>

    <!-- Overlay -->
    <div v-if="isOpen" @click="isOpen = false" class="fixed inset-0 h-full w-full z-10"></div>

    <!-- Dropdown -->
    <div 
      v-if="isOpen" 
      class="absolute right-0 mt-2 w-80 rounded-lg border border-[#2c3140] bg-[#181c25] shadow-2xl z-20 overflow-hidden transform origin-top-right transition-all"
    >
      <!-- Header com informações do usuário -->
      <div class="p-5 border-b border-[#2c3140]">
        <div class="flex items-center space-x-4">
          <div class="flex-shrink-0">
            <div class="h-14 w-14 rounded-full bg-[#1b1f29] flex items-center justify-center border border-[#2c3140]">
              <UserCircleIcon class="h-10 w-10 text-[#8b8f9c]" />
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-lg font-roboto font-medium text-[#ece8df] leading-tight break-words">
              {{ authStore.user?.givenName?.[0] || authStore.user?.username || 'Usuário' }}
            </p>
            <p class="text-sm font-roboto text-[#8b8f9c] break-all mt-0.5">
              {{ authStore.user?.userPrincipalName?.[0] || authStore.user?.username }}
            </p>
          </div>
        </div>
      </div>
      
      <!-- Informações do usuário -->
      <div class="border-b border-[#2c3140] bg-[#15181f]">
        <div class="p-5 space-y-4 text-sm">
          <div class="flex items-start">
            <BriefcaseIcon class="h-5 w-5 mr-3 text-[#8b8f9c] shrink-0 mt-0.5" />
            <div class="flex-1">
              <p class="text-[10px] font-roboto font-bold text-[#767c8a] uppercase tracking-wider mb-0.5">Cargo</p>
              <p class="text-[#ece8df] font-roboto font-medium leading-snug">{{ authStore.user?.title?.[0] || 'Não Informado' }}</p>
            </div>
          </div>
          <div class="flex items-start">
            <BuildingOffice2Icon class="h-5 w-5 mr-3 text-[#8b8f9c] shrink-0 mt-0.5" />
            <div class="flex-1">
              <p class="text-[10px] font-roboto font-bold text-[#767c8a] uppercase tracking-wider mb-0.5">Setor</p>
              <p class="text-[#ece8df] font-roboto font-medium leading-snug">{{ authStore.user?.department?.[0] || 'Não Informado' }}</p>
            </div>
          </div>
          <div class="flex items-start">
            <IdentificationIcon class="h-5 w-5 mr-3 text-[#8b8f9c] shrink-0 mt-0.5" />
            <div class="flex-1">
              <p class="text-[10px] font-roboto font-bold text-[#767c8a] uppercase tracking-wider mb-0.5">Matrícula</p>
              <p class="text-[#ece8df] font-roboto font-medium leading-snug">{{ authStore.user?.employeeNumber?.[0] || 'Não Informado' }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Botão de logout -->
      <div class="bg-[#15181f]">
        <a 
          href="#" 
          @click.prevent="handleLogout" 
          class="flex items-center justify-center px-4 py-3.5 text-sm font-roboto font-semibold text-[#b1615b] hover:bg-[#1b1f29] hover:text-[#c97a72] transition duration-150 ease-in-out border-t border-[#2c3140]"
        >
          <ArrowLeftOnRectangleIcon class="h-5 w-5 mr-2" />
          <span>Sair da Conta</span>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { UserCircleIcon, ArrowLeftOnRectangleIcon, BriefcaseIcon, BuildingOffice2Icon, IdentificationIcon } from '@heroicons/vue/24/outline';
import { useAuthStore } from '../stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const isOpen = ref(false);

const handleLogout = async () => {
  await authStore.logout(router);
};

// Close dropdown on navigation
watch(() => route.path, () => {
  isOpen.value = false;
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap");

.font-roboto {
  font-family: 'Roboto', sans-serif;
}

/* Animações e transições */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

.transform {
  transform: scale(1);
}

.origin-top-right {
  transform-origin: top right;
}

/* Hover effects */
.hover\:border-\[#4f8a8b\]:hover {
  border-color: #4f8a8b;
}

.hover\:bg-\[\#1b1f29\]:hover {
  background-color: #1b1f29;
}

.hover\:text-\[\#c97a72\]:hover {
  color: #c97a72;
}
</style>