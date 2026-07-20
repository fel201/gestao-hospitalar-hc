TIPO_AMBULATORIAL = "AMBULATÓRIO"
TIPO_EMERGENCIAL = "UTI"
CONDICAO_REGULADO = "REGULADO"
SITUACAO_CANCELADO = "CANCELADO"
SITUACAO_LIBERADO = "LIBERADO"
SITUACAO_A_COLETAR = "A COLETAR"
from ..helpers.jornada_utils import calcular_diferenca_horas
from typing import Any

_METRICAS_INDICADORES: list[tuple[str, str]] = [
    ("tempo_medio_solicitacao_realizacao", "Tempo médio de solicitação até a realização do exame"),
    ("concentracao_exames_ambulatoriais_paciente_ativo", "Concentração de Exames Ambulatoriais por paciente ativo"),
    ("concentracao_exames_emergenciais_paciente_ativo", "Concentração de Exames Emergenciais por paciente ativo"),
    ("porcentagem_exames_ambulatoriais", "Porcentagem de exames ambulatoriais"),
    ("porcentagem_exames_emergenciais", "Porcentagem de exames emergenciais"),
    ("porcentagem_exames_regulados", "Porcentagem de exames regulados em relação ao total"),
    ("porcentagem_exames_concluidos", "Porcentagem de exames concluidos em relação ao total"),
    ("porcentagem_exames_cancelados", "Porcentagem de exames marcados como pendentes"),
]

    
def qtd_exames_tipo(exames, tipo):
    if tipo == "ambulatorial": 
        condicao = TIPO_AMBULATORIAL
    else:
        condicao = TIPO_EMERGENCIAL
    total_exames_condicao = 0
    
    for e in exames:
        if condicao in e["especialidade_solicitante_nome"]:
            total_exames_condicao += 1
            
    return total_exames_condicao
def exames_cancelados(exames):
    e = [c for c in exames if SITUACAO_CANCELADO in c["situacao"].upper()]
    return e

def exames_concluidos(exames):
    e = [c for c in exames if SITUACAO_LIBERADO in c["situacao"].upper()]    
    return e

def exames_regulados(exames):
    e = [c for c in exames if CONDICAO_REGULADO in c["condicao"].upper()]
    return e

def porcentagem_exames_cancelados(exames):
    tamanho_exames_c = len(exames_cancelados(exames=exames))
    taxa = round((tamanho_exames_c/len(exames))*100, 2)
    return f"{taxa}%"
    
def porcentagem_exames_regulados(exames):
    p_exames_regulados = round(len(exames_regulados(exames=exames))/len(exames)*100, 2)
    return f"{p_exames_regulados}%"

def porcentagem_exames_concluidos(exames):
    n_exames_concluidos = len(exames_concluidos(exames=exames))
    p_exames_concluidos = round((n_exames_concluidos/len(exames))*100, 2)
    return f"{p_exames_concluidos}%"
    

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


def porcentagem_exames_do_tipo(exames: list[dict, any], tipo: str) -> dict:
    total_exames = len(exames)
    if total_exames == 0: return 0
    
    qtd_exames = qtd_exames_tipo(exames=exames, tipo=tipo)
    proporcao = round((qtd_exames/total_exames)*100, 2)
    
    return f"{proporcao}%"

# total de exames realizados / numero de pacientes atendidos
# Calcula a intensidade de investigação por paciente ativo
# paciente ativo: aquele que já realizou pelo menos um exame no hospital
def concentracao_exames_por_paciente_ativo(exames: list[dict, any], tipo: str) -> dict:
    pacientes = set()
    if tipo == "ambulatorial": 
        condicao = TIPO_AMBULATORIAL
    else:
        condicao = TIPO_EMERGENCIAL
        
    for e in exames:
        if condicao in e["especialidade_solicitante_nome"]:
            pacientes.add(e["prontuario"])
        
    qtd = qtd_exames_tipo(exames=exames, tipo=tipo)
    exames_amb_por_pac = round(qtd/len(pacientes), 2)
    print(qtd, tipo)
    print(len(pacientes),"pacientes")
    return exames_amb_por_pac
    
def dicionario_metricas_exames(exames):
    return {
        "tempo_medio_solicitacao_realizacao": tempo_medio_solicitacao_realizacao(exames=exames),
        "concentracao_exames_ambulatoriais_paciente_ativo": concentracao_exames_por_paciente_ativo(exames=exames, tipo="ambulatorial"),
        "concentracao_exames_emergenciais_paciente_ativo": concentracao_exames_por_paciente_ativo(exames=exames, tipo="emergencial"),
        "porcentagem_exames_ambulatoriais": porcentagem_exames_do_tipo(exames=exames, tipo="ambulatorial"),
        "porcentagem_exames_emergenciais": porcentagem_exames_do_tipo(exames=exames, tipo="emergencial"),
        "porcentagem_exames_regulados": porcentagem_exames_regulados(exames=exames),
        "porcentagem_exames_concluidos": porcentagem_exames_concluidos(exames=exames),
        "porcentagem_exames_cancelados": porcentagem_exames_cancelados(exames=exames)
    }
    
def metricas_exames(exames):
    metricas_key = dicionario_metricas_exames(exames=exames)
    indicadores = []
    
    for metrica, nome_display in _METRICAS_INDICADORES:
        if metrica not in metricas_key:
            continue
        
        valor = metricas_key[metrica]
        indicadores.append({
            "nome": nome_display,
            "valor": valor
        })
        
    return indicadores