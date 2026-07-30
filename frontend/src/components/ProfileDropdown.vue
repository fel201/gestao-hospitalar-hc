<template>
  <div class="relative">
    <!-- Botão do avatar -->
    <button
      ref="buttonRef"
      @click="toggleDropdown"
      class="relative z-10 block h-10 w-10 rounded-full overflow-hidden border border-[#2c3140] focus:outline-none focus:border-[#4f8a8b] transition-transform active:scale-95 hover:border-[#4f8a8b]"
    >
      <UserCircleIcon class="h-full w-full text-[#8b8f9c]" />
    </button>

    <Teleport to="body">
      <!-- Overlay -->
      <div
        v-if="isOpen"
        @click="closeDropdown"
        class="fixed inset-0 z-40"
      />

      <!-- Dropdown -->
      <div
        v-if="isOpen"
        class="fixed w-80 rounded-lg border border-[#2c3140] bg-[#181c25] shadow-2xl z-50 overflow-hidden"
        :style="dropdownStyle"
      >
        <!-- Header -->
        <div class="p-5 border-b border-[#2c3140]">
          <div class="flex items-center space-x-4">
            <div class="flex-shrink-0">
              <div class="h-14 w-14 rounded-full bg-[#1b1f29] flex items-center justify-center border border-[#2c3140]">
                <UserCircleIcon class="h-10 w-10 text-[#8b8f9c]" />
              </div>
            </div>

            <div class="flex-1 min-w-0">
              <p class="text-lg font-body font-medium text-[#ece8df]">
                {{ authStore.user?.givenName?.[0] || authStore.user?.username || "Usuário" }}
              </p>

              <p class="text-sm font-body text-[#8b8f9c] break-all">
                {{ authStore.user?.userPrincipalName?.[0] || authStore.user?.username }}
              </p>
            </div>
          </div>
        </div>

        <!-- Informações -->
        <div class="border-b border-[#2c3140] bg-[#15181f]">
          <div class="p-5 space-y-4 text-sm">
            <div class="flex items-start">
              <BriefcaseIcon class="h-5 w-5 mr-3 text-[#8b8f9c]" />
              <div>
                <p class="text-[10px] uppercase tracking-wider text-[#767c8a]">
                  Cargo
                </p>
                <p class="text-[#ece8df]">
                  {{ authStore.user?.title?.[0] || "Não Informado" }}
                </p>
              </div>
            </div>

            <div class="flex items-start">
              <BuildingOffice2Icon class="h-5 w-5 mr-3 text-[#8b8f9c]" />
              <div>
                <p class="text-[10px] uppercase tracking-wider text-[#767c8a]">
                  Setor
                </p>
                <p class="text-[#ece8df]">
                  {{ authStore.user?.department?.[0] || "Não Informado" }}
                </p>
              </div>
            </div>

            <div class="flex items-start">
              <IdentificationIcon class="h-5 w-5 mr-3 text-[#8b8f9c]" />
              <div>
                <p class="text-[10px] uppercase tracking-wider text-[#767c8a]">
                  Matrícula
                </p>
                <p class="text-[#ece8df]">
                  {{ authStore.user?.employeeNumber?.[0] || "Não Informado" }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Logout -->
        <div class="bg-[#15181f]">
          <a
            href="#"
            @click.prevent="handleLogout"
            class="flex items-center justify-center px-4 py-3.5 text-sm font-semibold text-[#b1615b] hover:bg-[#1b1f29]"
          >
            <ArrowLeftOnRectangleIcon class="h-5 w-5 mr-2" />
            Sair da Conta
          </a>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  UserCircleIcon,
  ArrowLeftOnRectangleIcon,
  BriefcaseIcon,
  BuildingOffice2Icon,
  IdentificationIcon,
} from "@heroicons/vue/24/outline";

import { useAuthStore } from "../stores/auth";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const isOpen = ref(false);
const buttonRef = ref<HTMLElement | null>(null);

const dropdownPosition = ref({
  top: 0,
  left: 0,
});

const dropdownStyle = computed(() => ({
  top: `${dropdownPosition.value.top}px`,
  left: `${dropdownPosition.value.left}px`,
}));

function updatePosition() {
  if (!buttonRef.value) return;

  const rect = buttonRef.value.getBoundingClientRect();

  dropdownPosition.value = {
    top: rect.bottom + 8,
    left: rect.right - 320, // 320 = w-80
  };
}

function toggleDropdown() {
  if (!isOpen.value) {
    updatePosition();
  }

  isOpen.value = !isOpen.value;
}

function closeDropdown() {
  isOpen.value = false;
}

const handleLogout = async () => {
  await authStore.logout(router);
};

watch(
  () => route.path,
  () => {
    isOpen.value = false;
  }
);
</script>