def filtrar_eventos(evento: str, dados, especialidade):
    campos = {
        "consulta": "especialidade",
        "internacao": "especialidade",
        "exame": "especialidade_solicitante_nome",
    }

    campo = campos[evento]

    return [
        d for d in dados
        if especialidade.lower() in d[campo].lower()
    ]
