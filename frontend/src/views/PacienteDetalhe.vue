<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Detalhes do Paciente</h1>

    <Card class="mb-6">
      <div class="space-y-4 text-sm">
        <div><span class="font-medium">Código:</span> {{ codigo }}</div>
        <div><span class="font-medium">Nome:</span> {{ jornada?.paciente?.nome ?? 'Carregando...' }}</div>
        <div><span class="font-medium">Prontuário:</span> {{ jornada?.paciente?.prontuario ?? 'Carregando...' }}</div>
      </div>
    </Card>

    <Card class="mb-6">
      <template #header>
        <h2 class="text-lg font-semibold">Linha do Tempo</h2>
      </template>

      <div class="mb-4 flex flex-wrap gap-3 items-center">
        <label class="font-medium">Filtrar por evento:</label>
        <select v-model="tipoSelecionado" class="border rounded px-3 py-2">
          <option value="">Todos</option>
          <option value="consulta">Consulta</option>
          <option value="exame">Exame</option>
          <option value="internacao">Internação</option>
        </select>
        <Button variant="secondary" @click="loadJornada">Atualizar</Button>
      </div>

      <!-- MÉTRICAS -->
      <div v-if="jornada?.metricas" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <Card>
          <div class="text-center">
            <p class="text-sm text-gray-500">Total de Eventos</p>
            <p class="text-3xl font-bold">
              {{ jornada.metricas.numero_eventos }}
            </p>
          </div>
        </Card>

        <Card>
          <div class="text-center">
            <p class="text-sm text-gray-500">Consultas</p>
            <p class="text-3xl font-bold text-blue-600">
              {{ jornada.metricas.numero_consultas }}
            </p>
          </div>
        </Card>

        <Card>
          <div class="text-center">
            <p class="text-sm text-gray-500">Exames</p>
            <p class="text-3xl font-bold text-green-600">
              {{ jornada.metricas.numero_exames }}
            </p>
          </div>
        </Card>

        <Card>
          <div class="text-center">
            <p class="text-sm text-gray-500">Internações</p>
            <p class="text-3xl font-bold text-red-600">
              {{ jornada.metricas.numero_internacoes }}
            </p>
          </div>
        </Card>
      </div>

      <div v-if="jornada?.eventos?.length" class="space-y-6">
        <div v-for="(item, index) in jornada.eventos" :key="`${item.tipo}-${index}`" class="relative">
          <!-- linha vertical -->
          <div v-if="index !== jornada.eventos.length - 1" class="absolute left-4 top-12 bottom-0 w-px bg-gray-300">
          </div>

          <!-- marcador -->
          <div class="absolute left-2 top-5 w-4 h-4 rounded-full bg-primary"></div>

          <!-- card do evento (bg-blue-200 ficou ótimo :D)-->
          <div class="ml-10 border rounded-lg p-4 shadow-sm bg-blue-200">
            <div class="flex justify-between items-start mb-3">
              <div>
                <h3 class="font-semibold text-base">
                  <template v-if="item.tipo === 'consulta'">
                    Consulta Médica
                  </template>

                  <template v-else-if="item.tipo === 'exame'">
                    {{ item.nome_exame }}
                  </template>

                  <template v-else-if="item.tipo === 'internacao'">
                    Internação
                  </template>
                </h3>

                <p class="text-sm text-gray-500">
                  {{ item.data_evento }}
                </p>
              </div>

              <span class="text-xs border rounded px-2 py-1 uppercase">
                {{ item.tipo }}
              </span>
            </div>

            <!-- CONSULTA -->
            <template v-if="item.tipo === 'consulta'">
              <div class="space-y-1 text-sm">
                <div>
                  <strong>Especialidade:</strong>
                  {{ item.especialidade || 'Não informado' }}
                </div>

                <div>
                  <strong>Procedimento:</strong>
                  {{ item.procedimento || 'Não informado' }}
                </div>

                <div>
                  <strong>CID:</strong>
                  {{ item.cid || 'Não informado' }}
                </div>

                <div v-if="item.indica_retorno">
                  <strong>Retorno:</strong>
                  {{ item.indica_retorno }}
                </div>
              </div>
            </template>

            <!-- EXAME -->
            <template v-else-if="item.tipo === 'exame'">
              <div class="space-y-1 text-sm">
                <div>
                  <strong>Tipo:</strong>
                  {{ item.tipo_exame || 'Não informado' }}
                </div>

                <div>
                  <strong>Situação:</strong>
                  {{ item.situacao_exame || 'Não informado' }}
                </div>

                <div>
                  <strong>Atendimento:</strong>
                  {{ item.atendimento_id || 'Não informado' }}
                </div>
              </div>
            </template>

            <!-- INTERNAÇÃO -->
            <template v-else-if="item.tipo === 'internacao'">
              <div class="space-y-1 text-sm">
                <div>
                  <strong>Especialidade:</strong>
                  {{ item.especialidade || 'Não informado' }}
                </div>

                <div>
                  <strong>Tempo de permanência:</strong>
                  {{ item.tempo_permanencia_dias + ' dias' || 'Não informado' }}
                </div>

                <div>
                  <strong>Alta:</strong>
                  {{ item.descricao_tipo_alta_medica || 'Não informado' }}
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>

      <div v-else class="text-sm text-muted">
        Nenhum evento encontrado.
      </div>
    </Card>

    <div class="mt-6">
      <Button @click="goBack" variant="secondary">Voltar para a lista</Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
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
const tipoSelecionado = ref('');

const loadJornada = async () => {
  if (!codigo) {
    toast.error('Código de paciente inválido.');
    return;
  }

  try {
    const params: Record<string, any> = { codigo };
    if (tipoSelecionado.value) {
      params.tipo = tipoSelecionado.value;
    }

    const { data } = await api.get('/api/paciente/jornada', { params });
    jornada.value = data;
    console.log(jornada.value);
  } catch (error) {
    toast.error('Não foi possível carregar a jornada do paciente.');
  }
};

const goBack = () => {
  router.push({ name: 'Pacientes' });
};

onMounted(loadJornada);
</script>
