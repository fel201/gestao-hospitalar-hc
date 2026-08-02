<template>
  <div class="min-h-screen bg-[#0d0f14] text-slate-200 px-6 py-8">
    <div v-if="carregando" class="flex min-h-[80vh] flex-col items-center justify-center gap-8">
      <div class="rounded-3xl bg-slate-900/70 p-8 text-center shadow-xl shadow-black/20">
        <div class="mx-auto mb-6 flex h-24 w-24 items-center justify-center rounded-full bg-blue-500/10 text-blue-400">
          <svg class="h-10 w-10 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-20" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" />
            <path class="opacity-90" fill="currentColor" d="M12 2a10 10 0 0110 10h-3a7 7 0 00-7-7V2z" />
          </svg>
        </div>
        <h2 class="text-2xl font-semibold text-white">Carregando jornada do paciente</h2>
        <p class="mt-2 text-sm text-slate-400">Buscando histórico de atendimentos e eventos clínicos...</p>
        <div class="mt-8 flex items-center justify-center gap-2">
          <span class="inline-flex h-2.5 w-16 rounded-full bg-slate-800"></span>
          <span class="inline-flex h-2.5 w-16 rounded-full bg-slate-800"></span>
          <span class="inline-flex h-2.5 w-16 rounded-full bg-slate-800"></span>
        </div>
        <p class="mt-4 text-xs uppercase tracking-[0.25em] text-slate-500">{{ dicaAtual }}</p>
      </div>
    </div>

    <div v-else class="space-y-6">
      <!-- Cabeçalho do paciente: card único, com métricas integradas em linha -->
      <Card class="bg-slate-900 border-slate-700 p-6">
        <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div class="min-w-0">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Paciente</p>
            <h1 class="mt-2 truncate text-3xl font-semibold text-white">{{ jornada?.paciente?.nome ?? 'Paciente não identificado' }}</h1>
            <p class="mt-1 text-sm text-slate-400">Prontuário: <span class="font-medium text-white">{{ jornada?.paciente?.prontuario ?? '—' }}</span></p>
          </div>

          <!-- Métricas lado a lado, em vez de empilhadas verticalmente -->
          <div class="grid grid-cols-3 gap-3 lg:min-w-[420px]">
            <div v-for="metrica in metricas" :key="metrica.label" class="rounded-2xl bg-slate-950/50 p-4 text-center">
              <p class="text-2xl font-semibold text-white">{{ metrica.valor }}</p>
              <p class="mt-1 text-[11px] uppercase tracking-[0.2em] text-slate-500">{{ metrica.label }}</p>
            </div>
          </div>
        </div>
      </Card>

      <!-- Corpo principal: timeline + detalhes -->
      <div class="grid gap-6 xl:grid-cols-[0.95fr_1.05fr] xl:items-start">
        <Card class="bg-slate-900 border-slate-700 p-6">
          <div class="mb-6 flex items-center justify-between gap-4">
            <div>
              <h2 class="text-xl font-semibold text-white">Linha do Tempo</h2>
              <p class="mt-1 text-sm text-slate-400">{{ jornada?.eventos?.length || 0 }} evento(s) · clique para ver detalhes</p>
            </div>
          </div>

          <div v-if="!jornada?.eventos?.length" class="rounded-3xl border border-dashed border-slate-700 bg-slate-950/40 p-8 text-center text-slate-400">
            Nenhum evento registrado para este paciente.
          </div>

          <!-- Timeline com trilho vertical e marcador por tipo de evento -->
          <ol v-else class="relative max-h-[640px] space-y-3 overflow-y-auto pr-1 pl-2">
            <li
              v-for="(evento, index) in jornada.eventos"
              :key="index"
              class="relative"
            >
              <div
                @click="selecionarEvento(evento)"
                class="group flex cursor-pointer items-start gap-3 rounded-2xl border border-slate-700 bg-slate-950/50 p-4 transition hover:border-slate-500 hover:bg-slate-900"
                :class="eventoSelecionado === evento ? 'border-blue-500 bg-blue-500/5' : ''"
              >
                <span class="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-slate-900 text-base" :title="evento.tipo">
                  {{ iconeEvento(evento) }}
                </span>

                <div class="min-w-0 flex-1">
                  <div class="flex flex-wrap items-center justify-between gap-2">
                    <p class="truncate text-sm font-medium text-white">{{ labelEvento(evento) }}</p>
                    <span
                      class="shrink-0 rounded-full border px-2.5 py-0.5 text-[10px] uppercase tracking-[0.2em] text-slate-300"
                      :class="eventoSelecionado === evento ? 'border-blue-500 bg-blue-500/10 text-blue-300' : 'border-slate-700 bg-slate-950/70'">
                      {{ evento.tipo }}
                    </span>
                  </div>
                  <p class="mt-1 text-xs text-slate-500">{{ formatarData(evento.data_evento || evento.dthr_inicio) }}</p>
                  <p class="mt-1 truncate text-xs text-slate-500">{{ evento.unidade_executora || 'Hospital das Clínicas' }}</p>
                </div>
              </div>
            </li>
          </ol>
        </Card>

        <Card class="bg-slate-900 border-slate-700 p-6 xl:sticky xl:top-6">
          <div class="mb-6">
            <h2 class="text-xl font-semibold text-white">Detalhes do Evento</h2>
            <p class="mt-1 text-sm text-slate-400">Informações rápidas do registro selecionado.</p>
          </div>

          <div v-if="eventoSelecionado" class="space-y-5">
            <!-- Cabeçalho do detalhe: tipo + data lado a lado -->
            <div class="grid gap-4 sm:grid-cols-[1fr_1fr]">
              <div class="rounded-3xl bg-slate-950/50 p-5">
                <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Tipo</p>
                <p class="mt-2 text-lg font-semibold text-white">{{ labelEvento(eventoSelecionado) }}</p>
              </div>
              <div class="rounded-3xl bg-slate-950/50 p-5">
                <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Data/Hora</p>
                <p class="mt-2 text-sm text-slate-200">{{ formatarData(eventoSelecionado.data_evento || eventoSelecionado.dthr_inicio) }}</p>
              </div>
            </div>

            <div class="grid gap-4 sm:grid-cols-2">
              <div class="rounded-3xl bg-slate-950/50 p-5">
                <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Duração</p>
                <p class="mt-2 text-sm text-slate-200">{{ eventoSelecionado.tempo_permanencia_dias ? eventoSelecionado.tempo_permanencia_dias + ' dias' : (eventoSelecionado.duracao || 'Não informada') }}</p>
              </div>
              <div class="rounded-3xl bg-slate-950/50 p-5">
                <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Unidade</p>
                <p class="mt-2 truncate text-sm text-slate-200">{{ eventoSelecionado.unidade_executora || 'Hospital das Clínicas' }}</p>
              </div>
            </div>

            <div class="rounded-3xl bg-slate-950/50 p-5">
              <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Profissional</p>
              <p class="mt-2 text-sm text-slate-200">{{ eventoSelecionado.profissional || 'Equipe médica' }}</p>
            </div>

            <div class="rounded-3xl bg-slate-950/50 p-5">
              <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Observações</p>
              <p class="mt-2 min-h-20 text-sm leading-6 text-slate-300">{{ eventoSelecionado.observacao || eventoSelecionado.descricao || 'Nenhuma observação disponível.' }}</p>
            </div>
          </div>

          <div v-else class="rounded-3xl border border-dashed border-slate-700 bg-slate-950/40 p-8 text-center text-slate-400">
            Selecione um evento na linha do tempo para visualizar os detalhes.
          </div>
        </Card>
      </div>

      <div class="flex justify-end">
        <Button @click="goBack" variant="secondary" class="px-5 py-3">Voltar</Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import api from '../services/api';
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const codigo = String(route.params.codigo || '');
const jornada = ref<any | null>(null);
const carregando = ref(true);
const eventoSelecionado = ref<any | null>(null);
const dicaAtual = ref('Carregando dados do paciente...');
const etapaAtual = ref(1);
let dicaInterval: number | null = null;

const dicas = [
  'Carregando dados do paciente...',
  'Buscando histórico de consultas...',
  'Recuperando exames realizados...',
  'Organizando informações clínicas...',
  'Preparando linha do tempo...',
  'Quase pronto!'
];

// Métricas do cabeçalho, centralizadas em um só lugar para facilitar
// adicionar/remover indicadores sem mexer no template
const metricas = computed(() => [
  { label: 'Exames', valor: jornada.value?.metricas?.numero_exames ?? '—' },
  { label: 'Internações', valor: jornada.value?.metricas?.numero_internacoes ?? '—' },
  { label: 'Consultas', valor: jornada.value?.metricas?.numero_consultas ?? '—' },
]);

const labelEvento = (item: any): string => {
  if (!item) return '';
  switch (item.tipo) {
    case 'consulta':
      return item.especialidade ? `Consulta — ${item.especialidade}` : 'Consulta médica';
    case 'exame':
      return item.nome_exame || 'Exame';
    case 'internacao':
      return item.especialidade ? `Internação — ${item.especialidade}` : 'Internação';
    default:
      return item.tipo ?? 'Evento';
  }
};

// Ícone simples por tipo de evento, para dar contexto visual rápido na timeline
const iconeEvento = (item: any): string => {
  switch (item?.tipo) {
    case 'consulta':
      return '🩺';
    case 'exame':
      return '🧪';
    case 'internacao':
      return '🏥';
    default:
      return '•';
  }
};

const formatarData = (dataStr: string): string => {
  if (!dataStr) return 'Data não informada';
  const data = new Date(dataStr);
  if (isNaN(data.getTime())) return dataStr;
  const pad = (value: number) => String(value).padStart(2, '0');
  return `${pad(data.getDate())}/${pad(data.getMonth() + 1)}/${data.getFullYear()} às ${pad(data.getHours())}:${pad(data.getMinutes())}`;
};

const selecionarEvento = (evento: any) => {
  eventoSelecionado.value = evento;
};

const iniciarAnimacaoCarregamento = () => {
  let index = 0;
  dicaAtual.value = dicas[0];
  etapaAtual.value = 1;

  dicaInterval = window.setInterval(() => {
    index = (index + 1) % dicas.length;
    dicaAtual.value = dicas[index];
    etapaAtual.value = Math.min(4, index + 1);
  }, 1800);
};

const loadJornada = async () => {
  if (!codigo) {
    toast.error('Código do paciente inválido.');
    router.push({ name: 'Pacientes' });
    return;
  }

  carregando.value = true;
  iniciarAnimacaoCarregamento();

  try {
    const { data } = await api.get('/api/paciente/jornada', {
      params: { codigo },
    });

    jornada.value = data;
    eventoSelecionado.value = data?.eventos?.[0] ?? null;
    dicaAtual.value = 'Carregamento concluído!';
    etapaAtual.value = 4;
  } catch (error) {
    toast.error('Não foi possível carregar a jornada do paciente.');
  } finally {
    carregando.value = false;
    if (dicaInterval !== null) {
      clearInterval(dicaInterval);
      dicaInterval = null;
    }
  }
};

const goBack = () => {
  router.push({ name: 'Pacientes' });
};

onMounted(loadJornada);

onBeforeUnmount(() => {
  if (dicaInterval !== null) {
    clearInterval(dicaInterval);
    dicaInterval = null;
  }
});
</script>

<style scoped>
.animate-progress {
  animation: progress 2s ease-in-out infinite;
}

@keyframes progress {
  0% { transform: translateX(-100%); }
  50% { transform: translateX(100%); }
  100% { transform: translateX(-100%); }
}
</style>