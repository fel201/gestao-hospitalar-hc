<template>
  <div class="min-h-screen bg-[#15181f] text-slate-200">
    <div class="mx-auto max-w-6xl px-6 py-8">

      <div class="space-y-6">
        <Card>
          <template #header>
            <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 class="text-lg font-semibold text-white">Pesquisa por prontuário</h2>
                <p class="text-sm text-slate-400">Busca direta pelo prontuário do paciente.</p>
              </div>
            </div>
          </template>

          <div class="grid gap-4">
            <div class="grid gap-2">
              <label for="pacienteProntuarioInput" class="text-sm font-medium text-slate-200">Prontuário</label>
              <input
                id="pacienteProntuarioInput"
                v-model="pacienteProntuarioInput"
                type="text"
                placeholder="Digite o prontuário do paciente"
                class="w-full rounded-xl border border-[#2c3140] bg-[#12161f] px-4 py-3 text-slate-100 placeholder:text-slate-500 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500/20 transition"
                @keyup.enter="fetchPacientePorProntuario"
              />
            </div>

            <div class="flex flex-wrap items-center justify-end gap-3">
              <Button
                @click="fetchPacientePorProntuario"
                :loading="loadingPaciente"
                variant="success"
                class="whitespace-nowrap px-4 py-2"
              >
                Buscar
              </Button>
            </div>
          </div>

          <template #footer v-if="pacienteDetalhe">
            <div class="flex justify-end">
              <Button @click="showTimeline" variant="info">
                Exibir linha do tempo
              </Button>
            </div>
          </template>
        </Card>

        <Card>
          <template #header>
            <h2 class="text-lg font-semibold text-white">Resultado</h2>
          </template>

          <div class="min-h-60 px-2 py-6">
            <div v-if="loadingPaciente" class="flex h-full flex-col items-center justify-center gap-3 text-slate-400">
              <svg class="w-14 h-14 text-slate-500 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v4m0 8v4m8-8h-4M4 12H0m15.071-7.071l-2.828 2.828M6.757 17.243l-2.828 2.828m12.02 0l-2.828-2.828M6.757 6.757L3.929 9.586" />
              </svg>
              <p class="text-base font-medium text-white">Buscando o paciente...</p>
              <p class="text-sm text-slate-400">Aguarde enquanto localizamos o prontuário.</p>
            </div>

            <div v-else-if="pacienteDetalhe" class="grid gap-4 text-sm text-slate-200">
              <div class="grid gap-3 sm:grid-cols-2">
                <div class="rounded-2xl bg-[#12161f] p-4">
                  <p class="text-sm text-slate-400">Código</p>
                  <p class="mt-1 text-base font-medium text-white">{{ pacienteDetalhe.codigo }}</p>
                </div>
                <div class="rounded-2xl bg-[#12161f] p-4">
                  <p class="text-sm text-slate-400">Prontuário</p>
                  <p class="mt-1 text-base font-medium text-white">{{ pacienteDetalhe.prontuario }}</p>
                </div>
              </div>

              <div class="grid gap-3 sm:grid-cols-2">
                <div class="rounded-2xl bg-[#12161f] p-4">
                  <p class="text-sm text-slate-400">Nome</p>
                  <p class="mt-1 text-base font-medium text-white">{{ pacienteDetalhe.nome }}</p>
                </div>
                <div class="rounded-2xl bg-[#12161f] p-4">
                  <p class="text-sm text-slate-400">Idade</p>
                  <p class="mt-1 text-base font-medium text-white">{{ pacienteDetalhe.idade }}</p>
                </div>
              </div>

              <div class="grid gap-3 sm:grid-cols-2">
                <div class="rounded-2xl bg-[#12161f] p-4">
                  <p class="text-sm text-slate-400">Sexo</p>
                  <p class="mt-1 text-base font-medium text-white">{{ pacienteDetalhe.sexo }}</p>
                </div>
                <div class="rounded-2xl bg-[#12161f] p-4">
                  <p class="text-sm text-slate-400">Estado Civil</p>
                  <p class="mt-1 text-base font-medium text-white">{{ pacienteDetalhe.estado_civil }}</p>
                </div>
              </div>

              <div class="grid gap-3 sm:grid-cols-2">
                <div class="rounded-2xl bg-[#12161f] p-4">
                  <p class="text-sm text-slate-400">Cidade</p>
                  <p class="mt-1 text-base font-medium text-white">{{ pacienteDetalhe.cidade }}</p>
                </div>
                <div class="rounded-2xl bg-[#12161f] p-4">
                  <p class="text-sm text-slate-400">UF</p>
                  <p class="mt-1 text-base font-medium text-white">{{ pacienteDetalhe.uf }}</p>
                </div>
              </div>
            </div>

            <div v-else-if="pesquisaExecutada" class="flex h-full flex-col items-center justify-center gap-3 text-center text-slate-400">
              <svg class="w-14 h-14 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.29 3.86L1.82 18a1 1 0 00.86 1.5h18.64a1 1 0 00.86-1.5L13.71 3.86a1 1 0 00-1.72 0zM12 9v4m0 4h.01" />
              </svg>
              <p class="text-base font-semibold text-white">Paciente não encontrado</p>
              <p class="max-w-md text-sm text-slate-400">Verifique se o prontuário está correto e tente novamente.</p>
            </div>

            <div v-else class="flex h-full flex-col items-center justify-center gap-3 text-center text-slate-400">
              <svg class="w-14 h-14 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-5 18h2m-6-4h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <p class="text-base font-semibold text-white">Digite um prontuário para iniciar a busca.</p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import api from "../services/api";
import Card from "../components/Card.vue";
import Button from "../components/Button.vue";

const toast = useToast();
const router = useRouter();
const pacienteProntuarioInput = ref("");
const loadingPaciente = ref(false);
const pacienteDetalhe = ref<any | null>(null);
const pesquisaExecutada = ref(false);

const fetchPacientePorProntuario = async () => {
  if (!pacienteProntuarioInput.value.trim()) {
    toast.error("Por favor, digite o prontuário.");
    return;
  }

  loadingPaciente.value = true;
  pacienteDetalhe.value = null;
  pesquisaExecutada.value = false;

  try {
    const { data } = await api.get(
      `/api/pacientes/prontuario/${encodeURIComponent(pacienteProntuarioInput.value.trim())}`
    );

    pacienteDetalhe.value = data;
    pesquisaExecutada.value = true;
    toast.success(`Paciente encontrado: ${data.nome}`);
  } catch (error: any) {
    pesquisaExecutada.value = true;
    if (error.response?.status === 404) {
      toast.error("Paciente não encontrado.");
    } else {
      toast.error("Erro ao buscar paciente.");
    }
  } finally {
    loadingPaciente.value = false;
  }
};

const showTimeline = () => {
  if (!pacienteDetalhe.value) {
    toast.error("Nenhum paciente carregado para exibir a linha do tempo.");
    return;
  }

  router.push({
    name: "PacienteDetalhe",
    params: { codigo: String(pacienteDetalhe.value.codigo) },
  });
};
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
