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
    "nome": { "type": "string", "minLength": 3 },
    "cpf": { "type": "string", "pattern": "^[0-9]{11}$" },
    "cns": { "type": "string", "pattern": "^[0-9]{15}$" },
    "data_nascimento": { "type": "string", "format": "date" }
  },
  "required": ["nome", "cpf", "data_nascimento"]
}
```

## 3. Regras de Integridade
* Logs obrigatórios e proibição de exclusão física.
