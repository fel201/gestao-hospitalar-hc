<template>
  <div class="relative h-screen overflow-hidden md:flex bg-slate-900 text-slate-200">
    <!-- Mobile Menu -->
    <div
      class="bg-slate-950 text-slate-200 flex justify-between md:hidden border-b border-slate-800 shrink-0"
    >
      <router-link
        to="/"
        class="block p-4 text-white font-bold tracking-tight"
      >
        Dashboard Assistencial
      </router-link>

      <button
        @click="sidebarOpen = !sidebarOpen"
        class="p-4 hover:bg-slate-800 transition-colors"
      >
        <Bars3Icon class="h-6 w-6" />
      </button>
    </div>

    <!-- Sidebar -->
    <aside
      :class="{ '-translate-x-full': !sidebarOpen }"
      class="bg-slate-950 text-slate-200 w-64 space-y-6 py-7 px-2 absolute inset-y-0 left-0 transform md:relative md:translate-x-0 transition duration-200 ease-in-out z-20 h-full shrink-0 border-r border-slate-800"
    >
      <!-- Logo -->
      <div
        @click="router.push('/')"
        class="cursor-pointer flex items-center gap-3 px-4"
      >
        <CubeTransparentIcon class="h-8 w-8 text-blue-500" />
        <span class="text-xl font-bold tracking-tight text-white">
          Jornada Assistencial
        </span>
      </div>

      <div class="px-4">
        <div class="border-t border-slate-800"></div>
      </div>

      <!-- Navegação -->
      <nav class="space-y-2">
        <router-link
          v-if="authStore.isAuthenticated"
          to="/pacientes"
          class="flex items-center gap-3 py-3 px-4 rounded-lg transition-colors hover:bg-slate-800 hover:text-white"
          active-class="bg-slate-800 text-white"
        >
          <UsersIcon class="h-5 w-5" />
          <span>Pacientes</span>
        </router-link>

        <router-link
          v-if="authStore.isAuthenticated"
          to="/"
          class="flex items-center gap-3 py-3 px-4 rounded-lg transition-colors hover:bg-slate-800 hover:text-white"
          active-class="bg-slate-800 text-white"
        >
          <LayoutDashboard class="h-5 w-5" />
          <span>Dashboard</span>
        </router-link>
      </nav>
    </aside>

    <!-- Conteúdo -->
    <div class="flex-1 flex flex-col bg-slate-900 overflow-y-auto h-full">
      <header
        class="flex justify-between items-center px-8 py-5 bg-slate-950 border-b border-slate-800 shadow-sm sticky top-0 z-10"
      >
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-white">
            {{ $route.name }}
          </h1>

          <p class="text-sm text-slate-400 mt-1">
            Plataforma Integrada Assistencial
          </p>
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

      <main class="flex-1">
        <div
          :class="
            route.name === 'DashboardJornada'
              ? 'w-full px-10 py-8'
              : 'w-full px-10 py-8'
          "
        >
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