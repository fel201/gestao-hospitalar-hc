CONDICAO_AMBULATORIAL = "AMBULATÓRIO"
CONDICAO_EMERGENCIA = "UTI"
from ..helpers.jornada_utils import calcular_diferenca_horas
from typing import Any

def tempo_medio_solicitacao_realizacao(exames: list[dict[str, Any]]) -> dict:
    if not exames:
        return {"tempo_medio_solic_realiz": 0}

    soma_tempos = 0

    for exame in exames:
        soma_tempos += calcular_diferenca_horas(
            exame["data_hora_solicitacao"],
            exame["data_hora_realizacao"],
        )

    tempo_medio = round((soma_tempos / len(exames)) * 60, 2)

    return tempo_medio

#Proporção de exames ambulatoriais em relação ao total

def proporcao_exames(exames: list[dict, any], tipo: str) -> dict:
    total_exames = len(exames)
    total_exames_condicao = 0
    
    if tipo == "ambulatorial": 
        condicao = CONDICAO_AMBULATORIAL
    else:
        condicao = CONDICAO_EMERGENCIA
    
    if total_exames == 0: return {}
    
    for e in exames:
        if condicao in e["especialidade_solicitante_nome"]:
            total_exames_condicao += 1
    
    proporcao = round((total_exames_condicao/total_exames)*100, 2)
    return {
        "total_exames_condicao": total_exames_condicao,
        "proporcao_exames": proporcao
    }
    
def exames_por_paciente(exames: list[dict, any], tipo: str) -> dict:
    pacientes = set()
    if tipo == "ambulatorial": 
        condicao = CONDICAO_AMBULATORIAL
    else:
        condicao = CONDICAO_EMERGENCIA
        
    for e in exames:
        if condicao in e["especialidade_solicitante_nome"]:
            pacientes.add(e["prontuario"])
        
    qtd_exames_ambulatoriais = (proporcao_exames(exames=exames, tipo=tipo))["total_exames_condicao"]
    exames_amb_por_pac = round(qtd_exames_ambulatoriais/len(pacientes), 2)
    print(exames_amb_por_pac)
    return {    
        "total_pacientes": len(pacientes),
        "exames_por_pac": exames_amb_por_pac
    }
    