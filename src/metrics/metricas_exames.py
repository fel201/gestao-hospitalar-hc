from ..helpers.jornada_utils import calcular_diferenca_horas
from ..helpers.formatacao import remover_acentos
from typing import Any

import unicodedata

ESPECIALIDADE_AMBULATORIAL = "AMBULATORIO"
ESPECIALIDADE_UTI = "UTI"
ESPECIALIDADE_URGENCIA = "URGENCIA"
ESPECIALIDADE_CIRURGIA = "CIRUR"
CONDICAO_REGULADO = "REGULADO"
SITUACAO_CANCELADO = "CANCELADO"
SITUACAO_LIBERADO = "LIBERADO"
SITUACAO_A_COLETAR = "A COLETAR"

_METRICAS_INDICADORES: list[tuple[str, str]] = [
    ("tempo_medio_solicitacao_realizacao", "Tempo médio de solicitação até a realização do exame"),
    ("concentracao_exames_ambulatoriais_paciente_ativo_mensal", "Concentração de Exames Ambulatoriais por paciente ativo de cada mês"),
    ("concentracao_exames_emergenciais_paciente_ativo_mensal", "Concentração de Exames Emergenciais por paciente ativo de cada mês"),
    ("porcentagem_exames_ambulatoriais", "Porcentagem de exames ambulatoriais"),
    ("porcentagem_exames_emergenciais", "Porcentagem de exames emergenciais"),
    ("porcentagem_exames_preoperatorios", "Porcentagem de exames pré-operatórios"),
    ("porcentagem_exames_regulados", "Porcentagem de exames regulados em relação ao total"),
    ("porcentagem_exames_concluidos", "Porcentagem de exames concluidos em relação ao total"),
    ("porcentagem_exames_cancelados", "Porcentagem de exames marcados como pendentes"),
]

    
def qtd_exames_tipo(exames, tipo):
    total_exames_condicao = 0
    
    for e in exames:
        especialidade = remover_acentos(e["especialidade_solicitante_nome"])
        
        if tipo == "ambulatorial" and ESPECIALIDADE_AMBULATORIAL in especialidade:
            total_exames_condicao += 1
        
        elif tipo == "emergencial" and ESPECIALIDADE_UTI in e["especialidade_solicitante_nome"] \
            or ESPECIALIDADE_URGENCIA in e["especialidade_solicitante_nome"]:
            total_exames_condicao += 1
        
        elif tipo == "pre-operatorio" and ESPECIALIDADE_CIRURGIA in e["especialidade_solicitante_nome"]:
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
    

def tempo_medio_solicitacao_realizacao(exames):
    if not exames:
        return 0

    soma = 0
    outliers = []

    for exame in exames:
        diff = calcular_diferenca_horas(
            exame["data_hora_solicitacao"],
            exame["data_hora_realizacao"],
        )

        soma += diff

        if diff <= 12:
            outliers.append(
                (
                    exame["prontuario"],
                    exame["data_hora_solicitacao"],
                    exame["data_hora_realizacao"],
                    diff,
                )
            )

    tempo_medio = round((soma / len(exames)), 2)

    for o in sorted(outliers, key=lambda x: x[3])[:20]:
        print(o)

    return f"{tempo_medio} horas"

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
        
    for e in exames:
        pacientes.add(e["prontuario"])
        
    qtd = qtd_exames_tipo(exames=exames, tipo=tipo)
    exames_amb_por_pac = round(qtd/len(pacientes), 2)
    return exames_amb_por_pac
    
    
from datetime import datetime

def _mes_anterior(ano: int, mes: int) -> tuple[int, int]:
    """Retorna (ano, mes) do mês anterior."""
    if mes == 1:
        return ano - 1, 12
    return ano, mes - 1

def concentracao_exames_por_paciente_ativo_mensal(
    exames: list[dict],
    tipo: str,
    data_inicio: str,
    data_fim: str,
) -> dict:
    """
    Calcula a concentração de exames por paciente ativo, mês a mês,
    olhando para os últimos 5 meses (ou menos, se o intervalo for menor).

    data_inicio e data_fim no formato "%Y-%m-%d" (ex: "2026-04-30").
    Retorna um dict {"MM/YYYY": valor, ...} em ordem cronológica crescente.
    """
    dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    dt_fim = datetime.strptime(data_fim, "%Y-%m-%d")

    ano_inicio, mes_inicio = dt_inicio.year, dt_inicio.month
    ano_atual, mes_atual = dt_fim.year, dt_fim.month

    
    meses_alvo = []
    while len(meses_alvo) < 5:
        meses_alvo.append((ano_atual, mes_atual))
        if (ano_atual, mes_atual) == (ano_inicio, mes_inicio):
            break
        ano_atual, mes_atual = _mes_anterior(ano_atual, mes_atual)

    # Ordena do mais antigo para o mais recente
    meses_alvo.reverse()

    resultado = {}
    for ano, mes in meses_alvo:
        chave = f"{mes:02d}/{ano}"

        exames_do_mes = []
        for e in exames:
            data_exame = datetime.strptime(e["data_hora_realizacao"], "%d/%m/%Y, %H:%M")
            if data_exame.year == ano and data_exame.month == mes:
                exames_do_mes.append(e)

        if not exames_do_mes:
            resultado[chave] = 0
            continue

        resultado[chave] = concentracao_exames_por_paciente_ativo(
            exames=exames_do_mes, tipo=tipo
        )
    print(resultado)
    return resultado    

def dicionario_metricas_exames(exames, data_inicio, data_fim):
    return {
        "tempo_medio_solicitacao_realizacao": tempo_medio_solicitacao_realizacao(exames=exames),
        "concentracao_exames_ambulatoriais_paciente_ativo_mensal":
            concentracao_exames_por_paciente_ativo_mensal(
                exames=exames,
                tipo="ambulatorial",
                data_inicio=data_inicio,
                data_fim=data_fim
            ),
        "concentracao_exames_emergenciais_paciente_ativo_mensal":
            concentracao_exames_por_paciente_ativo_mensal(
                exames=exames,
                tipo="emergencial",
                data_inicio=data_inicio,
                data_fim=data_fim
            ),
        "porcentagem_exames_ambulatoriais":
            porcentagem_exames_do_tipo(
                exames=exames,
                tipo="ambulatorial"
            ),
        "porcentagem_exames_emergenciais":
            porcentagem_exames_do_tipo(
                exames=exames, tipo="emergencial"
            ),
        "porcentagem_exames_preoperatorios":
            porcentagem_exames_do_tipo(
                exames=exames,
                tipo="pre-operatorio"
            ),
        "porcentagem_exames_regulados":
            porcentagem_exames_regulados(
                exames=exames
            ),
        "porcentagem_exames_concluidos":
            porcentagem_exames_concluidos(
                exames=exames
            ),
        "porcentagem_exames_cancelados":
            porcentagem_exames_cancelados(
                exames=exames
            )
    }
    
def metricas_exames(exames, data_inicio, data_fim):
    metricas_key = dicionario_metricas_exames(exames=exames, data_inicio=data_inicio, data_fim=data_fim)
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