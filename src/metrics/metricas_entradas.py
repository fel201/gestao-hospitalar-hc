from itertools import chain

from .metricas_consultas import _parse_dt
from ..helpers.jornada_utils import calcular_diferenca_horas


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
        # modificando o formato pra ficar compatível com a função
        data_cadastro = f'{paciente["data_cadastro"]}, 00:00'

        tempo_total += calcular_diferenca_horas(
            data_cadastro,
            primeiro_evento["data_hora_realizacao"]
        )

        pacientes_com_evento += 1

    tempo_medio = (
        tempo_total / pacientes_com_evento
        if pacientes_com_evento > 0 
        else 0
    )
    valor_final = ""
    if tempo_medio > 24:
        tempo_medio = round(tempo_medio/24)
        valor_final = f"{tempo_medio} dias"
    return {
        "nome": "Tempo médio da data de cadastro até o primeiro evento",
        "valor": valor_final
    }
    
def taxa_prontuarios_inertes(
    consultas,
    exames,
    internacoes,
    pacientes,
    cirurgias
):
    prontuarios_com_evento = set()
    count = 0
    for evento in chain(consultas, exames, internacoes, cirurgias):
        if evento["prontuario"]:
            prontuarios_com_evento.add(evento["prontuario"])    
            count+=1
    inertes = 0

    for paciente in pacientes:
        if paciente["prontuario"] not in prontuarios_com_evento:
            inertes += 1

        
    taxa_prontuarios_inertes = round((inertes/len(pacientes))*100, 2)
    return {
        "nome": "Taxa de prontuários inertes",
        "valor": f"{taxa_prontuarios_inertes}%",
    }