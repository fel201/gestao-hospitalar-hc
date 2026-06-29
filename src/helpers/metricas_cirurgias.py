from collections import defaultdict


def pacientes_operados(cirurgias):
    pacientes = {
        c["paciente_id"]
        for c in cirurgias
        if str(c["cancelada"]).upper() != "S"
    }

    return len(pacientes)


def tempo_medio_cirurgia(cirurgias):
    tempos = []

    for c in cirurgias:
        if str(c["cancelada"]).upper() == "S":
            continue

        try:
            tempos.append(float(c["duracao_cirurgia"]))
        except (TypeError, ValueError):
            pass

    if not tempos:
        return 0

    return round(sum(tempos) / len(tempos), 2)


def proporcao_pacientes_operados(cirurgias, total_pacientes):
    if total_pacientes == 0:
        return 0

    return round(
        pacientes_operados(cirurgias) / total_pacientes,
        4,
    )


def cirurgias_por_especialidade(cirurgias):
    resultado = defaultdict(int)

    for c in cirurgias:
        if str(c["cancelada"]).upper() == "S":
            continue

        resultado[c["especialidade"]] += 1

    return dict(resultado)


def metricas_cirurgias(cirurgias, total_pacientes):
    return [
        {
            "nome": "Pacientes operados",
            "valor": pacientes_operados(cirurgias),
        },
        {
            "nome": "Proporção de pacientes operados (%)",
            "valor": round(proporcao_pacientes_operados(cirurgias, total_pacientes)*100, 2),
        },
        {
            "nome": "Tempo médio de cirurgia (min)",
            "valor": tempo_medio_cirurgia(cirurgias),
        },
    ]