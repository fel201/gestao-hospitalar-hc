<template>
  <div class="relative h-screen overflow-hidden md:flex bg-[#12151c] text-[#ece8df]">
    <!-- Mobile Menu -->
    <div
      class="bg-[#181c25] text-[#ece8df] flex justify-between md:hidden border-b border-[#2c3140] shrink-0"
    >
      <router-link
        to="/"
        class="block p-4 font-serif text-lg font-medium text-[#ece8df] tracking-tight"
      >
        Dashboard Assistencial
      </router-link>

      <button
        @click="sidebarOpen = !sidebarOpen"
        class="p-4 hover:bg-[#1f2430] transition-colors text-[#8b8f9c] hover:text-[#ece8df]"
      >
        <Bars3Icon class="h-6 w-6" />
      </button>
    </div>

    <!-- Sidebar -->
    <aside
      :class="{ '-translate-x-full': !sidebarOpen }"
      class="bg-[#15181f] text-[#8b8f9c] w-64 space-y-6 py-7 px-3 absolute inset-y-0 left-0 transform md:relative md:translate-x-0 transition duration-200 ease-in-out z-20 h-full shrink-0 border-r border-[#2c3140]"
    >
      <!-- Logo -->
      <div
        @click="router.push('/')"
        class="cursor-pointer flex items-center gap-3 px-3"
      >
        <CubeTransparentIcon class="h-8 w-8 text-[#4f8a8b]" />
        <div>
          <span class="block font-serif text-lg font-medium tracking-tight text-[#ece8df]">
            Jornada Assistencial
          </span>
          <span class="block font-mono text-[10px] uppercase tracking-[0.14em] text-[#767c8a]">
            Sistema Clínico
          </span>
        </div>
      </div>

      <div class="px-3">
        <div class="border-t border-[#2c3140]"></div>
      </div>

      <!-- Navegação -->
      <nav class="space-y-1.5">
        <router-link
          v-if="authStore.isAuthenticated"
          to="/pacientes"
          class="flex items-center gap-3 py-2.5 px-3 rounded-md font-medium text-sm transition-colors hover:bg-[#1b1f29] hover:text-[#ece8df]"
          active-class="bg-[#1b1f29] text-[#ece8df] border-l-2 border-[#4f8a8b]"
        >
          <UsersIcon class="h-5 w-5 text-[#8b8f9c]" />
          <span>Pacientes</span>
        </router-link>

        <router-link
          v-if="authStore.isAuthenticated"
          to="/"
          class="flex items-center gap-3 py-2.5 px-3 rounded-md font-medium text-sm transition-colors hover:bg-[#1b1f29] hover:text-[#ece8df]"
          active-class="bg-[#1b1f29] text-[#ece8df] border-l-2 border-[#4f8a8b]"
        >
          <LayoutDashboard class="h-5 w-5 text-[#8b8f9c]" />
          <span>Dashboard</span>
        </router-link>
        <router-link
          v-if="authStore.isAuthenticated"
          to="/docs"
          class="flex items-center gap-3 py-2.5 px-3 rounded-md font-medium text-sm transition-colors hover:bg-[#1b1f29] hover:text-[#ece8df]"
          active-class="bg-[#1b1f29] text-[#ece8df] border-l-2 border-[#4f8a8b]"
        >
          <LayoutDashboard class="h-5 w-5 text-[#8b8f9c]" />
          <span>Documentação</span>
        </router-link>
        
      </nav>
    </aside>

    <!-- Conteúdo Principal -->
    <div class="flex-1 flex flex-col bg-[#12151c] overflow-y-auto h-full">
      <!-- Header -->
      <header
        class="flex justify-between items-center px-8 py-5 bg-[#181c25] border-b border-[#2c3140] sticky top-0 z-30"
      >
        <div>
          <p class="font-mono text-[10px] uppercase tracking-[0.16em] text-[#8b8f9c]">
            Módulo Ativo
          </p>
          <h1 class="font-serif text-2xl font-medium text-[#ece8df] mt-0.5">
            {{ $route.name }}
          </h1>
        </div>

        <div>
          <router-link
            v-if="!authStore.isAuthenticated"
            to="/login"
          >
            <Button variant="primary">
              <template #icon>
                <ArrowRightOnRectangleIcon class="h-5 w-5" />
              </template>
              Login
            </Button>
          </router-link>

          <ProfileDropdown v-else />
        </div>
      </header>

      <!-- Main Container -->
      <main class="flex-1">
        <div class="w-full px-8 py-8">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import {
  UsersIcon,
  CubeTransparentIcon,
  Bars3Icon,
  ArrowRightOnRectangleIcon,
} from "@heroicons/vue/24/outline";

import { LayoutDashboard } from "lucide-vue-next";

import ProfileDropdown from "../components/ProfileDropdown.vue";
import Button from "../components/Button.vue";
import { useAuthStore } from "../stores/auth";

const sidebarOpen = ref(false);

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

watch(
  () => route.path,
  () => {
    sidebarOpen.value = false;
  }
);
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=IBM+PlexMono:wght@400;600&display=swap");

.font-serif {
  font-family: "Source Serif 4", Georgia, serif;
}

.font-mono {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
}
</style>