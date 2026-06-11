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
interface PacienteDTO {
  pac_id: number;
  prontuario: string;
  nome: string;
}

interface ConsultaDTO {
  consulta_id: number;
  pac_id: number;
  cid?: string;
  data_evento?: string;
  data_hora_fim?: string;
  justificativa?: string;
  justificativa_falta?: string;
  tipo_consulta?: string;
  especialidade?: string;
  procedimento?: string;
  data_procedimento?: string;
  indica_retorno?: boolean;
  situacao_consulta?: string;
  unidade_funcional?: string;
}

interface ExameDTO {
  exame_id: number;
  pac_id: number;
  atendimento_id?: number;
  nome_exame?: string;
  tipo_exame?: string;
  data_hora_solicitacao?: string;
  data_evento?: string;
  data_hora_liberacao?: string;
  situacao_exame?: string;
  especialidade_solicitante_nome?: string;
  unidade_executora_id?: number;
}

interface InternacaoDTO {
  internacao_id: number;
  pac_id: number;
  atendimento_id?: number;
  data_evento: string;
  dthr_fim?: string;
  tempo_permanencia_dias?: number;
  situacao_sumario_alta?: string;
  descricao_origem_evento?: string;
  descricao_tipo_alta_medica?: string;
  especialidade_internacao?: string;
}

## 3. Contratos de API (Endpoints Principais)

> O contrato de ingestão do AGHU deve utilizar estritamente as colunas definidas em `SDD/04-modelo-dados.md` para as tabelas de paciente, consulta, exame e internação.

### GET /api/pacientes/:id_paciente/jornada
Resumo: Retorna eventos agregados e métricas derivadas para alimentar o dashboard da jornada do paciente.

Exemplo de resposta (campos representativos, não PII):

```json
{
  "pac_codigo": 12345,
  "jornada": [
    {"tipo_evento": "consulta", "dthr": "2026-05-01T09:15:00Z", "unidade": "Ambulatório A", "metrica_ids": [1,2]},
    {"tipo_evento": "exame", "dthr": "2026-05-02T11:30:00Z", "unidade": "Laboratório 1", "metrica_ids": [3]}
  ],
  "metricas_summary": [
    {"tipo_metrica": "tempo_entre_eventos_medio", "valor": 2.5},
    {"tipo_metrica": "num_eventos", "valor": 5}
  ]
}
```

Observações:
- `pac_codigo` é o identificador herdado do AGHU. Nunca enviar CPF/CNS via este endpoint.
- `metricas_summary` referencia métricas persistidas na tabela `METRICA`.

### GET /api/pacientes/:id_paciente
Resumo: Retorna dados triviais e não sensíveis para contextualizar a UI.

Exemplo de resposta:

```json
{
  "pac_codigo": 12345,
  "nome_reduzido": "S. Silva",
  "idade": 58,
  "sexo": "F"
}
```

### GET /api/pacientes
Resumo: Lista paginada (50 por página por padrão) contendo metadados não sensíveis.

### GET /api/metricas
Resumo: Retorna métricas agregadas e filtros (por período, unidade, tipo_metrica).

```
