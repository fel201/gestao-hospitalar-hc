from itertools import chain

from .metricas_consultas import _parse_dt
from ..helpers.jornada_utils import calcular_diferenca_horas


_METRICAS_INDICADORES: list[tuple[str, str]] = [
    (
        "tempo_medio_cadastro_evento",
        "Tempo médio da data de cadastro até o primeiro evento",
    ),
    (
        "taxa_prontuarios_inertes",
        "Taxa de prontuários inertes",
    ),
]


def tempo_medio_cadastro_evento(
    consultas,
    exames,
    internacoes,
    pacientes,
    cirurgias,
):
    primeiros_eventos = {}

    # percorre todos os eventos apenas uma vez
    for evento in chain(consultas, exames, internacoes, cirurgias):
        prontuario = evento["prontuario"]

        if not prontuario:
            continue

        data_evento = _parse_dt(evento["data_hora_realizacao"])
        if data_evento is None:
            continue

        if prontuario not in primeiros_eventos:
            primeiros_eventos[prontuario] = (data_evento, evento)
        else:
            data_atual, _ = primeiros_eventos[prontuario]

            if data_evento < data_atual:
                primeiros_eventos[prontuario] = (data_evento, evento)

    tempo_total = 0
    pacientes_com_evento = 0

    for paciente in pacientes:
        prontuario = paciente["prontuario"]

        if prontuario not in primeiros_eventos:
            continue

        _, primeiro_evento = primeiros_eventos[prontuario]

        data_cadastro = f'{paciente["data_cadastro"]}, 00:00'

        tempo_total += calcular_diferenca_horas(
            data_cadastro,
            primeiro_evento["data_hora_realizacao"],
        )

        pacientes_com_evento += 1

    tempo_medio = (
        tempo_total / pacientes_com_evento
        if pacientes_com_evento > 0
        else 0
    )

    if tempo_medio > 24:
        valor_final = f"{round(tempo_medio / 24)} dias"
    else:
        valor_final = f"{round(tempo_medio, 2)} horas"

    return valor_final


def taxa_prontuarios_inertes(
    consultas,
    exames,
    internacoes,
    pacientes,
    cirurgias,
):
    prontuarios_com_evento = set()

    for evento in chain(consultas, exames, internacoes, cirurgias):
        if evento["prontuario"]:
            prontuarios_com_evento.add(evento["prontuario"])

    if not pacientes:
        return "0%"

    inertes = sum(
        1
        for paciente in pacientes
        if paciente["prontuario"] not in prontuarios_com_evento
    )

    taxa = round((inertes / len(pacientes)) * 100, 2)
    return f"{taxa}%"


def dicionario_metricas_entradas(
    consultas,
    exames,
    internacoes,
    pacientes,
    cirurgias,
):
    return {
        "tempo_medio_cadastro_evento": tempo_medio_cadastro_evento(
            consultas=consultas,
            exames=exames,
            internacoes=internacoes,
            pacientes=pacientes,
            cirurgias=cirurgias,
        ),
        "taxa_prontuarios_inertes": taxa_prontuarios_inertes(
            consultas=consultas,
            exames=exames,
            internacoes=internacoes,
            pacientes=pacientes,
            cirurgias=cirurgias,
        ),
    }


def metricas_entradas(
    consultas,
    exames,
    internacoes,
    pacientes,
    cirurgias,
):
    metricas_key = dicionario_metricas_entradas(
        consultas=consultas,
        exames=exames,
        internacoes=internacoes,
        pacientes=pacientes,
        cirurgias=cirurgias,
    )

    indicadores = []

    for metrica, nome_display in _METRICAS_INDICADORES:
        if metrica not in metricas_key:
            continue

        indicadores.append(
            {
                "nome": nome_display,
                "valor": metricas_key[metrica],
            }
        )

    return indicadores