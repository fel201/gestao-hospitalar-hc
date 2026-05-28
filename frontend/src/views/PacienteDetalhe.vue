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
        <h2 class="text-lg font-semibold">Consultas</h2>
      </template>
      <div v-if="jornada?.consultas?.length" class="space-y-4 text-sm">
        <div v-for="item in jornada.consultas" :key="item.consulta_id" class="border rounded p-3">
          <div><span class="font-medium">Consulta ID:</span> {{ item.consulta_id }}</div>
          <div><span class="font-medium">CID:</span> {{ item.cid }}</div>
          <div><span class="font-medium">Data/Hora:</span> {{ item.data_hora_consulta }}</div>
          <div><span class="font-medium">Fim:</span> {{ item.data_hora_fim }}</div>
          <div><span class="font-medium">Especialidade:</span> {{ item.especialidade }}</div>
          <div><span class="font-medium">Procedimento:</span> {{ item.procedimento }}</div>
          <div><span class="font-medium">Tipo:</span> {{ item.tipo_consulta }}</div>
          <div><span class="font-medium">Justificativa:</span> {{ item.justificativa }}</div>
          <div><span class="font-medium">Justificativa falta:</span> {{ item.justificativa_falta }}</div>
          <div><span class="font-medium">Retorno:</span> {{ item.indica_retorno }}</div>
        </div>
      </div>
      <div v-else class="text-sm text-muted">Nenhuma consulta encontrada.</div>
    </Card>

    <Card class="mb-6">
      <template #header>
        <h2 class="text-lg font-semibold">Exames</h2>
      </template>
      <div v-if="jornada?.exames?.length" class="space-y-4 text-sm">
        <div v-for="item in jornada.exames" :key="item.exame_id" class="border rounded p-3">
          <div><span class="font-medium">Exame ID:</span> {{ item.exame_id }}</div>
          <div><span class="font-medium">Atendimento:</span> {{ item.atendimento_id }}</div>
          <div><span class="font-medium">Nome do exame:</span> {{ item.nome_exame }}</div>
          <div><span class="font-medium">Tipo:</span> {{ item.tipo_exame }}</div>
          <div><span class="font-medium">Situação:</span> {{ item.situacao_exame }}</div>
          <div><span class="font-medium">Especialidade solicitante:</span> {{ item.especialidade_solicitante_nome }}</div>
          <div><span class="font-medium">Unidade executora:</span> {{ item.unidade_executora_id }}</div>
        </div>
      </div>
      <div v-else class="text-sm text-muted">Nenhum exame encontrado.</div>
    </Card>

    <Card class="mb-6">
      <template #header>
        <h2 class="text-lg font-semibold">Internações</h2>
      </template>
      <div v-if="jornada?.internacoes?.length" class="space-y-4 text-sm">
        <div v-for="item in jornada.internacoes" :key="item.internacao_id" class="border rounded p-3">
          <div><span class="font-medium">Internação ID:</span> {{ item.internacao_id }}</div>
          <div><span class="font-medium">Atendimento:</span> {{ item.atendimento_id }}</div>
          <div><span class="font-medium">Início:</span> {{ item.dthr_inicio }}</div>
          <div><span class="font-medium">Fim:</span> {{ item.dthr_fim }}</div>
          <div><span class="font-medium">Tempo permanência:</span> {{ item.tempo_permanencia_dias }}</div>
          <div><span class="font-medium">Situação alta:</span> {{ item.situacao_sumario_alta }}</div>
          <div><span class="font-medium">Origem:</span> {{ item.descricao_origem_evento }}</div>
          <div><span class="font-medium">Tipo alta:</span> {{ item.descricao_tipo_alta_medica }}</div>
        </div>
      </div>
      <div v-else class="text-sm text-muted">Nenhuma internação encontrada.</div>
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

const loadJornada = async () => {
  if (!codigo) {
    toast.error('Código de paciente inválido.');
    return;
  }

  try {
    const { data } = await api.get('/api/paciente/jornada', { params: { codigo } });
    jornada.value = data;
  } catch (error) {
    toast.error('Não foi possível carregar a jornada do paciente.');
  }
};

const goBack = () => {
  router.push({ name: 'Pacientes' });
};

onMounted(loadJornada);
</script>
