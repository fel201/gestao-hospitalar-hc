# Modelo de Dados e Dicionário

## 1. Modelo Entidade-Relacionamento
```mermaid
erDiagram

    PACIENTE ||--o{ CONSULTA : realiza
    PACIENTE ||--o{ EXAME : possui
    PACIENTE ||--o{ INTERNACAO : realiza

    PACIENTE {
        int pac_id PK
        string prontuario
        string nome
    }

    CONSULTA {
        int consulta_id PK
        int pac_id FK
        string cid
        datetime data_hora_consulta
        datetime data_hora_fim
        string justificativa
        string justificativa_falta
        string tipo_consulta
        string especialidade
        string procedimento
        datetime data_procedimento
        boolean indica_retorno
    }

    EXAME {
        int exame_id PK
        int pac_id FK
        int atendimento
        string nome_exame
        string tipo_exame
        string situacao_exame
        string especialidade_solicitante_nome
        int unidade_executora
    }

    INTERNACAO {
        int internacao_id PK
        int pac_id FK
        int atendimento
        datetime dthr_inicio
        datetime dthr_fim
        int tempo_permanencia_dias
        string situacao_sumario_alta
        string descricao_origem_evento
        string descricao_tipo_alta_medica
    }
```


## 2. Dicionário de Dados
* Tabela PACIENTES, PRONTUARIOS, etc.

### [SCHEMA] Esquema JSON - Paciente
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Paciente",
  "type": "object",
  "properties": {
    "pac_id": { "type": "integer" },
    "prontuario": { "type": "string", "minLength": 1 },
    "nome": { "type": "string", "minLength": 3 }
  },
  "required": ["pac_id", "prontuario", "nome"]
}
```

## 3. Regras de Integridade
* Os dados recebidos do AGHU para pacientes, consultas, exames e internações devem seguir estritamente o conjunto de colunas definido neste modelo.
* Logs obrigatórios e proibição de exclusão física.

## 4. Esquema de Métricas (Metrics-First)

O sistema persiste apenas métricas derivadas e metadados necessários para análise e visualização. Não persistir PII ou texto livre contendo informações clínicas sensíveis.

METRICA {
        int metrica_id PK
        int pac_codigo?  # opcional: referência pseudonimizada ao paciente (não CPF)
        string tipo_metrica
        numeric valor
        datetime dthr
        json contexto  # JSON com metadados (unidade, especialidade, evento_origem, atendimento_id opcional)
}

### [SCHEMA] Esquema JSON - Metrica
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Metrica",
    "type": "object",
    "properties": {
        "metrica_id": { "type": "integer" },
        "pac_codigo": { "type": ["integer", "null"] },
        "tipo_metrica": { "type": "string" },
        "valor": { "type": "number" },
        "dthr": { "type": "string", "format": "date-time" },
        "contexto": { "type": "object" }
    },
    "required": ["metrica_id","tipo_metrica","valor","dthr"]
}
```

As integrações com AGHU devem transformar eventos clínicos em métricas antes de persistência na plataforma.
