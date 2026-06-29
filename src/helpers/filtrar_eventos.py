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

def filtrar_eventos(evento: str, dados, especialidade):
    campos = {
        "consulta": "especialidade",
        "internacao": "especialidade",
        "cirurgia": "especialidade",
        "exame": "especialidade_solicitante_nome",
    }

    campo = campos[evento]

    palavra = GRUPOS_ESPECIALIDADE.get(
        especialidade.lower(),
        especialidade.upper()
    )

    return [
        d
        for d in dados
        if palavra in d[campo].upper()
    ]
