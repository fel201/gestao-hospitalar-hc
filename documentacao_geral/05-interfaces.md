# Interfaces e Integrações

## 1. Protótipos
* [Prototipação da linha do tempo do paciente](https://www.figma.com/make/f9gHlb6W4nD1YsP2dd991K/User-Journey-Mapping-Panel?fullscreen=1&t=gMW54aou6TeWuQfb-1&code-node-id=0-9)

## 2. Hardware
* Computadores utilizados por profissionais hospitalares.
* Servidor para armazenamento e processamento dos dados.
* Rede interna hospitalar para comunicação entre sistemas.

## 3. Software
* Integração com AGHU. 

### [SCHEMA] Interface de Integração (TypeScript)
```typescript
// baseado nos dados que a gente recebeu
interface AGHUPacienteDTO {
  prontuario: string;
  pac_codigo: number;
  data_cadastro: string;
  nome_iniciais: string;
  nome_social_iniciais?: string;
  nome_mae_iniciais?: string;
  nome_pai_iniciais?: string;
  idade: number;
  sexo?: string;
  estado_civil?: string;
  cor?: string;
  etnia?: string;
  grau_instrucao?: string;
  profissao?: string;
  naturalidade?: string;
  nacionalidade?: string;
  situacao_prontuario?: string;
  logradouro?: string;
  bairro?: string;
  cidade?: string;
  uf?: string;
}

interface AGHUConsultaDTO {
  id: number;
  num_consulta: number;
  prontuario: string;
  data_procedimento?: string;
  procedimento?: string;
  procedimento_quantidade?: number;
  profissional_atendeu?: string;
  categoria_profissional?: string;
  profissional_grade?: string;
  profissional_procedimento?: string;
  grade?: string;
  sigla_especialidade?: string;
  especialidade?: string;
  data_hora_consulta?: string;
  turno?: string;
  data_hora_criacao?: string;
  data_hora_alteracao?: string;
  data_hora_inicio?: string;
  data_hora_fim?: string;
  codigo_plano_saude?: string;
  codigo_convenio?: string;
  servidor_marcacao?: string;
  equipe?: string;
  unidade_funcional?: string;
  centro_custos?: string;
  situacao_consulta?: string;
  codigo_cid?: string;
  cid?: string;
  retorno?: boolean;
  motivo_consulta?: string;
  justificativa?: string;
  justificativa_falta?: string;
  condicao_atendimento?: string;
  id_paciente?: number;
  codigo_central?: string;
  tipo?: string;
}

interface AGHUExameDTO {
  paciente_id: number;
  paciente_prontuario: string;
  atendimento_id: number;
  exame_id: number;
  nome_exame: string;
  nome_usual_exame?: string;
  tipo_exame?: string;
  data_hora_solicitacao?: string;
  data_hora_agendamento?: string;
  data_hora_coleta?: string;
  data_hora_realizacao?: string;
  data_hora_liberacao?: string;
  unidade_executora_id?: number;
  unidade_executora_sigla?: string;
  unidade_executora_nome?: string;
  especialidade_solicitante_sigla?: string;
  especialidade_solicitante_nome?: string;
  centro_custos_solicitante?: string;
  profissional_solicitante?: string;
  grade_solicitacao_id?: number;
  condicao_exame?: string;
  situacao_codigo?: string;
  situacao?: string;
}

interface AGHUInternacaoDTO {
  atendimento: number;
  id_internacao: number;
  prontuario: string;
  codigo_paciente: number;
  dthr_inicio: string;
  dthr_fim?: string;
  tempo_permanencia_dias?: number;
  indica_alta_manual?: boolean;
  ind_saida_pac?: string;
  situacao_sumario_alta?: string;
  descricao_origem_evento?: string;
  descricao_tipo_alta_medica?: string;
  lto_lto_id?: number;
  qrt_numero?: string;
  unf_seq?: number;
  unf_descricao?: string;
  unf_sigla?: string;
  unf_andar?: string;
  local_atendimento?: string;
  modalidade_assistencial?: string;
  cid_codigo?: string;
  cid_descricao?: string;
  flag_obito_internacao?: string;
  dt_obito?: string;
  esp_seq?: number;
  esp_sigla?: string;
  esp_nome_especialidade?: string;
  esp_nome_reduzido?: string;
  med_codigo?: number;
  med_nome_iniciais?: string;
}
```
