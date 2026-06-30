<template>
  <div class="min-h-screen bg-slate-900 text-slate-200">
    <h1 class="text-3xl font-bold tracking-tight text-white mb-2">
      Lista de Pacientes
    </h1>

    <p class="text-slate-400 mb-8">
      Consulta e gerenciamento dos pacientes cadastrados.
    </p>
    <Card class="bg-slate-800 border border-slate-700 rounded-xl shadow-lg">
      <div class="mb-6 flex items-center space-x-4">
        <div class="form-group flex-1">
          <label for="pacienteCodigoInput" class="form-label"
            >Buscar Paciente por Código</label
          >
          <div class="flex items-center space-x-2">
          <input
            id="pacienteCodigoInput"
            v-model="pacienteCodigoInput"
            type="number"
            placeholder="Digite o código do paciente"
            class="w-full bg-slate-900 border border-slate-700 rounded-lg p-3
                  text-slate-200 placeholder:text-slate-500
                  focus:outline-none focus:border-blue-500
                  focus:ring-1 focus:ring-blue-500
                  transition-colors"
            />
            <Button
              @click="fetchPacientePorCodigo"
              :disabled="loadingPaciente"
              variant="success"
              class="whitespace-nowrap"
            >
              <span v-if="loadingPaciente">Buscando...</span>
              <span v-else>Buscar</span>
            </Button>
          </div>
        </div>
      </div>
    </Card>

    <Card v-if="pacienteDetalhe" >
      <template #header>
        <h2 class="text-lg font-semibold">Detalhes do Paciente</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div>
          <span class="font-medium">Código:</span> {{ pacienteDetalhe.codigo }}
        </div>
        <div>
          <span class="font-medium">Prontuário:</span>
          {{ pacienteDetalhe.prontuario }}
        </div>
        <div>
          <span class="font-medium">Nome:</span> {{ pacienteDetalhe.nome }}
        </div>
        <div>
          <span class="font-medium">Idade:</span> {{ pacienteDetalhe.idade }}
        </div>
        <div>
          <span class="font-medium">Sexo:</span> {{ pacienteDetalhe.sexo }}
        </div>
        <div>
          <span class="font-medium">Estado Civil:</span>
          {{ pacienteDetalhe.estado_civil }}
        </div>
        <div>
          <span class="font-medium">Cor:</span> {{ pacienteDetalhe.cor }}
        </div>
        <div>
          <span class="font-medium">Nome da Mãe:</span>
          {{ pacienteDetalhe.nome_mae }}
        </div>
        <div v-if="pacienteDetalhe.nome_pai">
          <span class="font-medium">Nome do Pai:</span>
          {{ pacienteDetalhe.nome_pai }}
        </div>
        <div>
          <span class="font-medium">Nacionalidade:</span>
          {{ pacienteDetalhe.nacionalidade }}
        </div>
        <div>
          <span class="font-medium">Naturalidade:</span>
          {{ pacienteDetalhe.naturalidade }}
        </div>
        <div>
          <span class="font-medium">Cidade:</span> {{ pacienteDetalhe.cidade }}
        </div>
        <div><span class="font-medium">UF:</span> {{ pacienteDetalhe.uf }}</div>
      </div>
    </Card>

    <Card class="bg-slate-800 border border-slate-700 rounded-xl shadow-lg">
      <DataTable :headers="headers" :items="pacientes">
        <template #actions="{ item }">
          <div class="flex space-x-2">
            <Button @click="viewPaciente(item)" variant="info" size="sm">
              <svg
                class="h-4 w-4"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                />
              </svg>
            </Button>
          </div>
        </template>
      </DataTable>
    </Card class="bg-slate-800 border border-slate-700 rounded-xl shadow-lg">
    <div class="flex justify-between items-center mt-6">
      <Button
        variant="secondary"
        :disabled="pagina === 1"
        @click="paginaAnterior"
      >
        Anterior
      </Button>

      <span>
        Página {{ pagina }} de {{ totalPaginas }} ({{
          totalPacientes
        }}
        pacientes)
      </span>

      <Button
        variant="secondary"
        :disabled="pagina === totalPaginas"
        @click="proximaPagina"
      >
        Próxima
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import api from "../services/api";
import Card from "../components/Card.vue";
import DataTable from "../components/DataTable.vue";
import Button from "../components/Button.vue";

const toast = useToast();

const pacienteCodigoInput = ref(null);
const loadingPaciente = ref(false);
const pacienteDetalhe = ref<any | null>(null);
const router = useRouter();

const headers = ref([
  { text: "Código", value: "codigo" },
  { text: "Prontuário", value: "prontuario" },
  { text: "Nome", value: "nome" },
  { text: "Idade", value: "idade" },
  { text: "Sexo", value: "sexo" },
  { text: "Cidade", value: "cidade" },
]);

const pacientes = ref([]);
const pagina = ref(1);
const totalPaginas = ref(1);
const totalPacientes = ref(0);
const pageSize = 50;

const carregarPacientes = async () => {
  try {
    const { data } = await api.get("/api/pacientes", {
      params: {
        page: pagina.value,
        page_size: pageSize,
      },
    });

    pacientes.value = data.items;
    totalPaginas.value = data.total_pages;
    totalPacientes.value = data.total;
  } catch (error) {
    toast.error("Falha ao carregar a lista de pacientes.");
  }
};

const proximaPagina = async () => {
  if (pagina.value < totalPaginas.value) {
    pagina.value++;
    await carregarPacientes();
  }
};

const paginaAnterior = async () => {
  if (pagina.value > 1) {
    pagina.value--;
    await carregarPacientes();
  }
};

onMounted(() => {
  carregarPacientes();
});

const fetchPacientePorCodigo = async () => {
  if (!pacienteCodigoInput.value) {
    toast.error("Por favor, digite um código.");
    return;
  }
  loadingPaciente.value = true;
  pacienteDetalhe.value = null; // Clear previous details
  try {
    const { data } = await api.get(
      `/api/pacientes/${pacienteCodigoInput.value}`,
    );
    pacienteDetalhe.value = data;
    toast.success(`Paciente encontrado: ${data.nome}`);
  } catch (error) {
    toast.error("Paciente não encontrado.");
  } finally {
    loadingPaciente.value = false;
  }
};

const viewPaciente = (item: any) => {
  router.push({
    name: "PacienteDetalhe",
    params: { codigo: String(item.codigo) },
  });
};
</script>
