def total_pacientes_eventos(consultas, internacoes, exames):
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
            exame["paciente_prontuario"]
        )
    return len(
        pacientes_unicos
    )
