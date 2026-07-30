from datetime import datetime

GRUPOS_ESPECIALIDADE = {
    "acupuntura": "ACUPUNTURA",
    "alergia": "ALERGIA",
    "cardiologia": "CARDIO",
    "cirurgia": "CIRURGIA",
    "endocrino": "ENDOCRINO",
    "gastroenterologia": "GASTRO",
    "ginecologia": "GINECO",
    "hematologia": "HEMATO",
    "mastologia": "MASTOLOGIA",
    "nefrologia": "NEFRO",
    "neurologia": "NEURO",
    "nutricao": "NUTRI",
    "oftalmo": "OFTALMO",
    "ortopedia": "ORTOP",
    "proctologia": "PROCTO",
    "reumato": "REUMATO",
    "urologia": "UROLOGIA",
    "servico_social": "SERVIÇO SOCIAL",
    "enfermagem": "ENFERMAGEM",
}

_CAMPOS_ESPECIALIDADE = {
    "consulta": "especialidade",
    "internacao": "especialidade",
    "cirurgia": "especialidade",
    "exame": "especialidade_solicitante_nome",
}

# formato usado internamente por 'data_hora_realizacao' nos eventos e pelas
# datas de borda já formatadas por _formatar_data_iso_para_padrao
_DATE_FMT = "%d/%m/%Y, %H:%M"


def filtrar_eventos(evento: str, dados, especialidade):
    campo = _CAMPOS_ESPECIALIDADE[evento]

    palavra = GRUPOS_ESPECIALIDADE.get(
        especialidade.lower(),
        especialidade.upper()
    )

    return [
        d
        for d in dados
        if palavra in d[campo].upper()
    ]


