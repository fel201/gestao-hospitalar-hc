<template>
  <div class="min-h-screen bg-slate-900 text-slate-200">
    <h1 class="text-3xl font-bold tracking-tight text-white mb-2">
      Lista de Pacientes
    </h1>

    <p class="text-slate-400 mb-8">
      Consulta e gerenciamento dos pacientes cadastrados.
    </p>

    <!-- ==========================================
         BARRA DE BUSCA
         ========================================== -->
    <Card>
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
              @keyup.enter="fetchPacientePorCodigo"
            />
            <Button
              @click="fetchPacientePorCodigo"
              :disabled="loadingPaciente"
              variant="success"
              class="whitespace-nowrap"
            >
              <span v-if="loadingPaciente" class="flex items-center gap-2">
                <svg class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Buscando...
              </span>
              <span v-else>Buscar</span>
            </Button>
          </div>
        </div>
      </div>
    </Card>

    <!-- ==========================================
         DETALHES DO PACIENTE (BUSCA)
         ========================================== -->
    <Card v-if="pacienteDetalhe" class="bg-slate-800 border border-slate-700 rounded-xl shadow-lg mb-6">
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold">Detalhes do Paciente</h2>
          <Button @click="pacienteDetalhe = null" variant="ghost" size="sm" class="text-slate-400 hover:text-white">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </Button>
        </div>
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

    <Card class="bg-slate-800 border border-slate-700 rounded-xl shadow-lg relative">
      
      <div v-if="carregandoMudancaPagina" class="absolute inset-0 bg-slate-800/80 backdrop-blur-sm rounded-xl flex flex-col items-center justify-center z-10">
        <div class="flex flex-col items-center space-y-6 p-8">
          <!-- Spinner animado -->
          <div class="relative">
            <div class="w-16 h-16 rounded-full border-4 border-slate-700 border-t-blue-500 animate-spin"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-400 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
          </div>

          <div class="text-center space-y-2">
            <p class="text-lg font-medium text-white">Carregando página {{ pagina }}...</p>
            <p class="text-sm text-slate-400">{{ dicaCarregamentoPagina }}</p>
          </div>

          <!-- Barra de progresso -->
          <div class="w-64 h-1.5 bg-slate-700 rounded-full overflow-hidden">
            <div 
              class="h-full bg-linear-to-r from-blue-500 to-green-300 rounded-full transition-all duration-500"
              :style="{ width: progressoPagina + '%' }"
            ></div>
          </div>
        </div>
      </div>

      <!-- Estado de carregamento inicial da tabela -->
      <div v-if="carregandoTabela && !carregandoMudancaPagina" class="flex flex-col items-center justify-center py-16 space-y-6">
        <!-- Spinner animado -->
        <div class="relative">
          <div class="w-16 h-16 rounded-full border-4 border-slate-700 border-t-blue-500 animate-spin"></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-400 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
        </div>

        <div class="text-center space-y-2">
          <p class="text-lg font-medium text-white">Carregando pacientes...</p>
          <p class="text-sm text-slate-400">{{ dicaCarregamentoInicial }}</p>
        </div>

        <!-- Barra de progresso -->
        <div class="w-64 h-1.5 bg-slate-700 rounded-full overflow-hidden">
          <div 
            class="h-full bg-linear-to-r from-blue-500 to-purple-500 rounded-full transition-all duration-500"
            :style="{ width: progressoInicial + '%' }"
          ></div>
        </div>
      </div>

      <!-- Conteúdo da tabela -->
      <template v-if="!carregandoTabela">
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

        <!-- Estado vazio -->
        <div v-if="!pacientes.length" class="flex flex-col items-center justify-center py-16 text-slate-400">
          <svg class="w-16 h-16 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          <p class="text-lg">Nenhum paciente encontrado</p>
          <p class="text-sm">Tente recarregar a página ou buscar por um código específico</p>
        </div>
      </template>
    </Card>

    <!-- ==========================================
         PAGINAÇÃO
         ========================================== -->
    <div class="flex justify-between items-center mt-6">
      <Button
        variant="secondary"
        :disabled="pagina === 1 || carregandoMudancaPagina"
        @click="paginaAnterior"
        class="min-w-[120px]"
      >
        <span v-if="carregandoMudancaPagina" class="flex items-center gap-2">
          <svg class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Carregando...
        </span>
        <span v-else>← Anterior</span>
      </Button>

      <div class="flex items-center space-x-4">
        <span class="text-sm text-slate-400">
          Página {{ pagina }} de {{ totalPaginas || 1 }} 
          <span class="mx-2">•</span>
          {{ totalPacientes }} pacientes
        </span>

        <!-- Indicador de carregamento na paginação -->
        <div v-if="carregandoMudancaPagina" class="flex items-center gap-2">
          <div class="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
          <div class="w-2 h-2 bg-blue-500 rounded-full animate-pulse" style="animation-delay: 0.3s"></div>
          <div class="w-2 h-2 bg-blue-500 rounded-full animate-pulse" style="animation-delay: 0.6s"></div>
        </div>
      </div>

      <Button
        variant="secondary"
        :disabled="pagina === totalPaginas || carregandoMudancaPagina"
        @click="proximaPagina"
        class="min-w-[120px]"
      >
        <span v-if="carregandoMudancaPagina" class="flex items-center gap-2">
          <svg class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Carregando...
        </span>
        <span v-else>Próxima →</span>
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import api from "../services/api";
import Card from "../components/Card.vue";
import DataTable from "../components/DataTable.vue";
import Button from "../components/Button.vue";

const toast = useToast();

// Estado de carregamento
const carregandoTabela = ref(true);
const carregandoMudancaPagina = ref(false);
const progressoInicial = ref(0);
const progressoPagina = ref(0);
const dicaCarregamentoInicial = ref("Preparando lista de pacientes...");
const dicaCarregamentoPagina = ref("Carregando próxima página...");

const dicasIniciais = [
  "Preparando lista de pacientes...",
  "Carregando dados cadastrais...",
  "Organizando informações...",
  "Quase pronto..."
];

const dicasPagina = [
  "Carregando próxima página...",
  "Buscando dados dos pacientes...",
  "Organizando lista...",
  "Quase pronto..."
];

let progressoIntervalInicial: number | null = null;
let progressoIntervalPagina: number | null = null;

// Estado da busca
const pacienteCodigoInput = ref<number | null>(null);
const loadingPaciente = ref(false);
const pacienteDetalhe = ref<any | null>(null);
const router = useRouter();

// Configuração da tabela
const headers = ref([
  { text: "Código", value: "codigo" },
  { text: "Prontuário", value: "prontuario" },
  { text: "Nome", value: "nome" },
  { text: "Idade", value: "idade" },
  { text: "Sexo", value: "sexo" },
  { text: "Cidade", value: "cidade" },
]);

const pacientes = ref<any[]>([]);
const pagina = ref(1);
const totalPaginas = ref(1);
const totalPacientes = ref(0);
const pageSize = 50;

// Função para simular progresso inicial
const iniciarProgressoInicial = () => {
  progressoInicial.value = 0;
  let index = 0;
  
  if (progressoIntervalInicial) {
    clearInterval(progressoIntervalInicial);
  }

  progressoIntervalInicial = window.setInterval(() => {
    if (progressoInicial.value < 90) {
      const incremento = Math.random() * 10 + 5;
      progressoInicial.value = Math.min(progressoInicial.value + incremento, 90);
    }
    
    if (index < dicasIniciais.length) {
      dicaCarregamentoInicial.value = dicasIniciais[index];
      index++;
    }
  }, 2000);
};

// Função para simular progresso da paginação
const iniciarProgressoPagina = () => {
  progressoPagina.value = 0;
  let index = 0;
  
  if (progressoIntervalPagina) {
    clearInterval(progressoIntervalPagina);
  }

  progressoIntervalPagina = window.setInterval(() => {
    if (progressoPagina.value < 90) {
      const incremento = Math.random() * 15 + 5;
      progressoPagina.value = Math.min(progressoPagina.value + incremento, 90);
    }
    
    if (index < dicasPagina.length) {
      dicaCarregamentoPagina.value = dicasPagina[index];
      index++;
    }
  }, 1500);
};

const finalizarProgressoInicial = () => {
  progressoInicial.value = 100;
  dicaCarregamentoInicial.value = "Carregamento concluído!";
  
  if (progressoIntervalInicial) {
    clearInterval(progressoIntervalInicial);
    progressoIntervalInicial = null;
  }
};

const finalizarProgressoPagina = () => {
  progressoPagina.value = 100;
  dicaCarregamentoPagina.value = "Página carregada!";
  
  if (progressoIntervalPagina) {
    clearInterval(progressoIntervalPagina);
    progressoIntervalPagina = null;
  }
};

// Função para carregar pacientes
const carregarPacientes = async (isMudancaPagina = false) => {
  try {
    if (isMudancaPagina) {
      carregandoMudancaPagina.value = true;
      iniciarProgressoPagina();
    } else {
      carregandoTabela.value = true;
      iniciarProgressoInicial();
    }

    const { data } = await api.get("/api/pacientes", {
      params: {
        page: pagina.value,
        page_size: pageSize,
      },
    });

    pacientes.value = data.items || [];
    totalPaginas.value = data.total_pages || 1;
    totalPacientes.value = data.total || 0;

    // Pequeno delay para mostrar o progresso
    await new Promise(resolve => setTimeout(resolve, 400));
    
    if (isMudancaPagina) {
      finalizarProgressoPagina();
      // Delay extra para mostrar o 100%
      await new Promise(resolve => setTimeout(resolve, 300));
    } else {
      finalizarProgressoInicial();
      await new Promise(resolve => setTimeout(resolve, 300));
    }

  } catch (error) {
    toast.error("Falha ao carregar a lista de pacientes.");
    if (isMudancaPagina) {
      finalizarProgressoPagina();
    } else {
      finalizarProgressoInicial();
    }
  } finally {
    carregandoTabela.value = false;
    carregandoMudancaPagina.value = false;
  }
};

const proximaPagina = async () => {
  if (pagina.value < totalPaginas.value && !carregandoMudancaPagina.value) {
    pagina.value++;
    await carregarPacientes(true);
  }
};

const paginaAnterior = async () => {
  if (pagina.value > 1 && !carregandoMudancaPagina.value) {
    pagina.value--;
    await carregarPacientes(true);
  }
};

// Busca por código
const fetchPacientePorCodigo = async () => {
  if (!pacienteCodigoInput.value) {
    toast.error("Por favor, digite um código.");
    return;
  }
  
  loadingPaciente.value = true;
  pacienteDetalhe.value = null;
  
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

// Navegação para detalhes
const viewPaciente = (item: any) => {
  router.push({
    name: "PacienteDetalhe",
    params: { codigo: String(item.codigo) },
  });
};

// Cleanup
const cleanup = () => {
  if (progressoIntervalInicial) {
    clearInterval(progressoIntervalInicial);
    progressoIntervalInicial = null;
  }
  if (progressoIntervalPagina) {
    clearInterval(progressoIntervalPagina);
    progressoIntervalPagina = null;
  }
};

// Lifecycle
onMounted(() => {
  carregarPacientes(false);
});

onBeforeUnmount(cleanup);
</script>

<style scoped>
/* Animações de carregamento */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-pulse {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Transição suave para a barra de progresso */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 500ms;
}

/* Efeito de backdrop blur */
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}

/* Overlay com opacidade */
.absolute {
  position: absolute;
}

.inset-0 {
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

.z-10 {
  z-index: 10;
}

/* Indicadores de carregamento na paginação */
.animate-pulse {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { 
    opacity: 1;
    transform: scale(1);
  }
  50% { 
    opacity: 0.5;
    transform: scale(0.8);
  }
}
</style>