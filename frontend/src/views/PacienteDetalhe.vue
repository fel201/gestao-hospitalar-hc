<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Detalhes do Paciente</h1>
    <Card>
      <div class="space-y-4 text-sm">
        <div><span class="font-medium">Código:</span> {{ codigo }}</div>
        <div><span class="font-medium">Nome:</span> {{ paciente?.nome ?? 'Carregando...' }}</div>
        <div><span class="font-medium">Prontuário:</span> {{ paciente?.prontuario ?? 'Carregando...' }}</div>
        <div><span class="font-medium">Cidade:</span> {{ paciente?.cidade ?? 'Carregando...' }}</div>
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
const paciente = ref<any | null>(null);

const loadPaciente = async () => {
  if (!codigo) {
    toast.error('Código de paciente inválido.');
    return;
  }

  try {
    const { data } = await api.get(`/api/pacientes/${codigo}`);
    paciente.value = data;
  } catch (error) {
    toast.error('Não foi possível carregar os detalhes do paciente.');
  }
};

const goBack = () => {
  router.push({ name: 'Pacientes' });
};

onMounted(loadPaciente);
</script>
