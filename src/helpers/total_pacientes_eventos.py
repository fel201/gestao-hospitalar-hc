def total_pacientes_eventos(consultas, internacoes, exames, cirurgias):
    pacientes_unicos = set()
    for consulta in consultas:
        pacientes_unicos.add(
            consulta["prontuario"]
        )
    for internacao in internacoes:
        pacientes_unicos.add(
            internacao["prontuario"]
        )
    for exame in exames:
        pacientes_unicos.add(
            exame["prontuario"]
        )
    for cirurgia in cirurgias:
        pacientes_unicos.add(cirurgia["prontuario"])

    return len(
        pacientes_unicos
    )
