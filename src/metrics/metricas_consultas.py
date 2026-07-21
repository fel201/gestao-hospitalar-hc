# Formato de data esperado: 'dd/m/yyyy, HH:MM'  (ex: '13/1/2025, 09:51')

from __future__ import annotations
from ..helpers.jornada_utils import calcular_diferenca_horas, dias_entre
from datetime import datetime
from collections import defaultdict
from typing import Any

RETORNO_ATENDIDO   = "PACIENTE ATENDIDO"
RETORNO_PACIENTE_FALTOU     = "PACIENTE FALTOU"
RETORNO_PROFISSIONAL_FALTOU = "PROFISSIONAL FALTOU"
RETORNO_AGENDADO   = "PACIENTE AGENDADO"

CONDICAO_PRIMEIRA  = "PRIMEIRA CONSULTA"
CONDICAO_RETORNO   = "RETORNO"
CONDICAO_REGULADA  = "CONSULTA REGULADA"
CONDICAO_INTERCON  = "INTERCONSULTA"

DATE_FMT = "%d/%m/%Y, %H:%M"


# helpers internos

def _parse_dt(s: str) -> datetime | None:
    """Converte string de data/hora para datetime; retorna None se inválida."""
    if not s:
        return None
    try:
        
        return datetime.strptime(s.strip(), "%-d/%m/%Y, %H:%M")  
    except ValueError:
        pass
    try:
        return datetime.strptime(s.strip(), "%d/%m/%Y, %H:%M")
    except ValueError:
        return None


def concentracao_consultas_paciente_ativo(consultas):
    pacientes = set()
    for c in consultas:
        prontuario = c["prontuario"]
        if prontuario:
            pacientes.add(prontuario)
    
    return len(consultas) / len(pacientes)

def consultas_primeira_vez(consultas):
    c = [
        c for c in consultas
        if "PRIMEIRA CONSULTA" in c["condicao"]
    ]
    return c

def consultas_concluidas(consultas):
    consultas_concluidas = [
        c for c in consultas
        if "PACIENTE ATENDIDO" in c["retorno"]
    ]
    return consultas_concluidas

def porcentagem_consultas_concluidas(consultas):
    consultas_con = consultas_concluidas(consultas=consultas)
    taxa = round(len(consultas_con)/len(consultas)*100, 2)
    return f"{taxa}%"
    

def porcentagem_consultas_reguladas(consultas: list[dict[str, Any]]) -> dict:
    """
    Calcula a proporção de consultas com Condição = 'CONSULTA REGULADA'
    em relação ao total.
    """
    total = len(consultas)
    if total == 0:
        return {"total": 0, "reguladas": 0, "proporcao": 0.0}

    reguladas = sum(
        1 for c in consultas
        if CONDICAO_REGULADA in c.get("condicao", "") 
    )
    proporcao = round((reguladas/total)*100, 2)
    return f"{proporcao}%"

def porcentagem_faltas_pacientes(consultas: list[dict[str, Any]]) -> dict:
    total = len(consultas)
    if total == 0:
        return {
            "total": 0, "porcentagem_faltas_pacientes": 0.0,
        }

    faltas = sum(1 for c in consultas if RETORNO_PACIENTE_FALTOU in c.get("retorno", ""))
    porcentagem_faltas_pacientes = round((faltas / total)*100, 2)
    return f"{porcentagem_faltas_pacientes}%"


def porcentagem_faltas_profissional(consultas: list[dict[str, Any]]) -> dict:
    total = len(consultas)
    if total == 0:
        return {
            "total": 0, "porcentagem_faltas_profissionais": 0
        }
    
    faltas = sum(1 for c in consultas if RETORNO_PROFISSIONAL_FALTOU in c.get("retorno", ""))
    porcentagem_faltas_profissionais = round((faltas / total)*100, 2)
    return f"{porcentagem_faltas_profissionais}%"

def tempo_medio_agendamento_realizacao(consultas: list[dict[str, Any]]) -> dict:
    """
    tempo médio (em horas) entre o horário agendado da consulta
    e o momento em que ela foi finalizada.
    """
    deltas = []
    for c in consultas:
        if RETORNO_ATENDIDO not in c.get("retorno", ""):
            continue
        if CONDICAO_REGULADA in c.get("condicao", ""):
            h = calcular_diferenca_horas(c.get("data_hora_criacao", ""), c.get("data_hora_realizacao", ""))
            if h is not None and h >= 0:
                deltas.append(h)

    if not deltas:
        return 0

    media = sum(deltas) / len(deltas)
    media_horas = round(media, 4)
    return media_horas

def porcentagem_consultas_sem_prontuario(consultas: list[dict[str, Any]]) -> dict:
    total = len(consultas)
    if total == 0: return {"total": 0, "proporcao_sem_prontuario": 0}
    
    consultas_sem_prontuario = []
    for c in consultas:
        if c["prontuario"] == "":
            consultas_sem_prontuario.append(c)

    proporcao = round((len(consultas_sem_prontuario)/total)*100, 2)
    return f"{proporcao}%"
    
def porcentagem_consultas_retorno(consultas: list[dict[str, Any]]) -> dict:
    """
    Proporção de consultas com Condição = 'RETORNO' sobre o total.
    """
    total = len(consultas)
    if total == 0:
        return {"total": 0, "retornos": 0, "proporcao": 0.0}

    retornos = sum(1 for c in consultas if CONDICAO_RETORNO in c.get("condicao", ""))
    proporcao = round((retornos/total)*100, 2)
    return f"{proporcao}%"

def media_retornos_por_paciente(consultas: list[dict[str, Any]]) -> dict:
    """
    Calcula o número médio de consultas de retorno por paciente.
    """
    retornos_por_paciente: dict[str, int] = defaultdict(int)

    for c in consultas:
        if CONDICAO_RETORNO in c.get("condicao", ""):
            pid = c.get("prontuario", "")
            if pid:
                retornos_por_paciente[pid] += 1

    total_pacientes = len(retornos_por_paciente)
    total_retornos = sum(retornos_por_paciente.values())

    if total_pacientes == 0:
        return {
            "total_pacientes": 0,
            "total_retornos": 0,
            "media_retornos_por_paciente": 0.0,
        }
    media_retornos_por_paciente = round(total_retornos / total_pacientes, 2)
    
    return media_retornos_por_paciente

def media_interconsultas_por_paciente(consultas: list[dict[str, Any]]) -> dict:
    interconsultas_por_paciente: dict[str, int] = defaultdict(int)

    for c in consultas:
        if CONDICAO_INTERCON in c.get("condicao", ""):
            pid = c.get("prontuario", "")
            if pid:
                interconsultas_por_paciente[pid] += 1

    total_pacientes = len(interconsultas_por_paciente)
    total_interconsultas = sum(interconsultas_por_paciente.values())

    if total_pacientes == 0:
        return {
            "total_pacientes": 0,
            "total_interconsultas": 0,
            "media_interconsultas_por_paciente": 0.0,
        }
    media_interconsultas_por_paciente = round(total_interconsultas / total_pacientes, 2)
    return media_interconsultas_por_paciente

def media_reguladas_por_paciente(consultas: list[dict[str, Any]]) -> dict:
    reguladas_por_paciente: dict[str, int] = defaultdict(int)

    for c in consultas:
        if CONDICAO_INTERCON in c.get("condicao", ""):
            pid = c.get("prontuario", "")
            if pid:
                reguladas_por_paciente[pid] += 1

    total_pacientes = len(reguladas_por_paciente)
    total_reguladas = sum(reguladas_por_paciente.values())

    if total_pacientes == 0:
        return {
            "total_pacientes": 0,
            "total_retornos": 0,
            "media_reguladas_por_paciente": 0.0,
        }
    media_reguladas_por_paciente = round(total_reguladas / total_pacientes, 2)
    return media_reguladas_por_paciente

def intervalo_medio_regulada_primeiro_retorno(consultas: list[dict[str, Any]]) -> dict:
    """
    Para cada paciente, encontra a consulta regulada mais antiga e o primeiro
    retorno posterior. Calcula a média desses intervalos em dias.
    """
    # Agrupa por paciente
    por_paciente: dict[str, list[dict]] = defaultdict(list)
    for c in consultas:
        prontuario = c.get("prontuario", "")
        if prontuario:
            por_paciente[prontuario].append(c)

    intervalos = []
    count = 0
    for prontuario, eventos in por_paciente.items():
        reguladas = sorted(
            [e for e in eventos if CONDICAO_REGULADA in e.get("condicao", "")],
            key=lambda e: _parse_dt(e.get("data_hora_realizacao", "")) or datetime.max,
        )
        retornos = sorted(
            [e for e in eventos if CONDICAO_RETORNO in e.get("condicao", "")],
            key=lambda e: _parse_dt(e.get("data_hora_realizacao", "")) or datetime.max,
        )

        if not reguladas or not retornos:
            continue

        dt_reg = _parse_dt(reguladas[0].get("data_hora_realizacao", ""))
        if dt_reg is None:
            continue
        
        # Primeiro retorno APÓS a consulta regulada
        primeiro_retorno = next(
            (
                r for r in retornos
                if (_parse_dt(r.get("data_hora_realizacao", "")) or datetime.min) > dt_reg
            ),
            None,
        )
        if primeiro_retorno is None:
            continue

        dias = dias_entre(
            reguladas[0].get("data_hora_realizacao", ""),
            primeiro_retorno.get("data_hora_realizacao", ""),
        )
        if dias is not None and dias >= 0:
            intervalos.append(dias)

    if not intervalos:
        return 0
    media_dias = round(sum(intervalos) / len(intervalos), 2)
    
    return media_dias


def intervalo_medio_retornos_consecutivos(consultas: list[dict[str, Any]]) -> dict:
    """
    Para cada paciente com mais de um retorno, calcula os intervalos entre
    retornos consecutivos. Retorna a média global em dias.
    """
    por_paciente: dict[str, list[dict]] = defaultdict(list)
    for c in consultas:
        pid = c.get("prontuario", "")
        if pid and CONDICAO_RETORNO in c.get("condicao", ""):
            por_paciente[pid].append(c)

    intervalos = []
    for pid, retornos in por_paciente.items():
        retornos_ord = sorted(
            retornos,
            key=lambda e: _parse_dt(e.get("data_hora_realizacao", "")) or datetime.max,
        )
        for i in range(1, len(retornos_ord)):
            dias = dias_entre(
                retornos_ord[i - 1].get("data_hora_realizacao", ""),
                retornos_ord[i].get("data_hora_realizacao", ""),
            )
            if dias is not None and dias >= 0:
                intervalos.append(dias)

    if not intervalos:
        return {"n_intervalos": 0, "media_dias": 0.0}

    media_dias = round(sum(intervalos) / len(intervalos), 2)
    return f"{media_dias} dias"


# Tempo médio entre a criação do prontuário e o agendamento da consulta
def tempo_medio_criacao_prontuario_primeiro_agendamento(pacientes, consultas):
    """
    Calcula o tempo médio (em horas) entre a criação do prontuário
    (data_cadastro do paciente) e a realização da primeira consulta
    associada a esse prontuário.
    """
    # Agrupa as consultas por prontuário, guardando apenas a primeira
    # (menor data_hora_realizacao) de cada uma.
    primeira_consulta_por_prontuario = {}

    for consulta in consultas:
        prontuario = consulta["prontuario"]
        data_hora = datetime.strptime(consulta["data_hora_realizacao"], "%d/%m/%Y, %H:%M")

        atual = primeira_consulta_por_prontuario.get(prontuario)
        if atual is None or data_hora < atual["data_hora_dt"]:
            primeira_consulta_por_prontuario[prontuario] = {
                "data_hora_realizacao": consulta["data_hora_realizacao"],
                "data_hora_dt": data_hora,
            }

    tempo_total = 0
    quantidade = 0

    for paciente in pacientes:
        prontuario = paciente["prontuario"]
        primeiro_evento = primeira_consulta_por_prontuario.get(prontuario)

        # paciente sem nenhuma consulta agendada/realizada não entra na média
        if primeiro_evento is None:
            continue

        data_cadastro = f'{paciente["data_cadastro"]}, 00:00'

        tempo_total += dias_entre(
            data_cadastro,
            primeiro_evento["data_hora_realizacao"]
        )
        quantidade += 1

    if quantidade == 0:
        return 0
    tempo_medio = round(tempo_total / quantidade, 2)
    return tempo_medio

def encaminhamentos_por_consulta_regulada(
    consultas: list[dict[str, Any]]
) -> dict:
    """
    para cada consulta regulada identifica o primeiro encaminhamento
    subsequente do mesmo paciente.
    """

    por_paciente: dict[str, list[dict]] = defaultdict(list)

    for consulta in consultas:
        prontuario = consulta.get("prontuario")
        if prontuario:
            por_paciente[prontuario].append(consulta)

    encaminhamentos: dict[str, int] = defaultdict(int)
    total_reguladas = 0

    for eventos in por_paciente.values():

        eventos.sort(
            key=lambda e: _parse_dt(e.get("data_hora_realizacao", "")) or datetime.max
        )

        for i, evento in enumerate(eventos):

            if CONDICAO_REGULADA not in evento.get("condicao", ""):
                continue

            total_reguladas += 1

            for prox in eventos[i + 1:]:

                condicao = prox.get("condicao", "").upper()

                if CONDICAO_RETORNO in condicao:
                    encaminhamentos["RETORNO"] += 1

                    break

                if CONDICAO_INTERCON in condicao:
                    encaminhamentos["INTERCONSULTA"] += 1

                    break
                
    resultado = dict(
        sorted(encaminhamentos.items(), key=lambda x: x[1], reverse=True)
    )
    return resultado



def porcentagem_interconsultas(consultas: list[dict[str, Any]]) -> dict:
    """
    Proporção de consultas com Condição = 'INTERCONSULTA' sobre o total.
    """
    total = len(consultas)
    if total == 0:
        return {"total": 0, "interconsultas": 0, "proporcao": 0.0}

    interconsultas = sum(
        1 for c in consultas if CONDICAO_INTERCON in c.get("condicao", "")
    )
    proporcao = round((interconsultas/total)*100, 2)
    return f"{proporcao}%"

def porcentagem_pacientes_com_interconsulta(consultas: list[dict[str, Any]]) -> dict:
    """
    Calcula a proporção de pacientes únicos que possuem ao menos uma
    consulta com Condição = 'INTERCONSULTA'.
    """
    todos = {c.get("prontuario") for c in consultas if c.get("prontuario")}
    com_intercon = {
        c.get("prontuario")
        for c in consultas
        if CONDICAO_INTERCON in c.get("condicao", "") and c.get("prontuario")
    }

    total = len(todos)
    if total == 0:
        return {"total_pacientes": 0, "pacientes_com_interconsulta": 0, "proporcao": 0.0}
    proporcao = round(len(com_intercon) / total, 2)
    return f"{proporcao}%"



# função de conveniência: roda todas as métricas de uma vez
def dicionario_metricas_consultas(consultas: list[dict[str, Any]], pacientes: list[dict[str, Any]]) -> dict:
    """
    executa todas as métricas acima e retorna um dicionário consolidado.
    """
    return {
        "concentracao_consultas_paciente_ativo":                concentracao_consultas_paciente_ativo(consultas),
        "porcentagem_consultas_concluidas":                     porcentagem_consultas_concluidas(consultas),
        "porcentagem_consultas_reguladas":                      porcentagem_consultas_reguladas(consultas),
        "intervalo_medio_regulada_primeiro_retorno":            intervalo_medio_regulada_primeiro_retorno(consultas),
        "intervalo_medio_retornos_consecutivos":                intervalo_medio_retornos_consecutivos(consultas),
        "media_reguladas_por_paciente":                         media_reguladas_por_paciente(consultas),
        "media_retornos_por_paciente":                          media_retornos_por_paciente(consultas),
        "media_interconsultas_por_paciente":                    media_interconsultas_por_paciente(consultas),
        "proporcao_consultas_sem_prontuario":                   porcentagem_consultas_sem_prontuario(consultas),
        "tempo_medio_criacao_prontuario_primeiro_agendamento":  tempo_medio_criacao_prontuario_primeiro_agendamento(pacientes, consultas),
        "porcentagem_faltas_profissionais":                     porcentagem_faltas_profissional(consultas),          
        "encaminhamentos_por_consulta_regulada":                encaminhamentos_por_consulta_regulada(consultas),
        "porcentagem_faltas_pacientes":                         porcentagem_faltas_pacientes(consultas),
        "tempo_medio_agendamento_realizacao":                   tempo_medio_agendamento_realizacao(consultas),
        "porcentagem_consultas_retorno":                        porcentagem_consultas_retorno(consultas),
        "media_retornos_por_paciente":                          media_retornos_por_paciente(consultas),
        "porcentagem_interconsultas":                           porcentagem_interconsultas(consultas),
        "porcentagem_pacientes_com_interconsulta":              porcentagem_pacientes_com_interconsulta(consultas),
    }
    
    

# Flatten: converte o dict de métricas em lista de {nome, valor}
# compatível com DashboardIndicadorInterface
# Mapeamento explícito: (chave_metrica, nome_display, chave_valor)
# Permite escolher exatamente qual campo de cada métrica expor aco frontend.
_METRICAS_INDICADORES: list[tuple[str, str]] = [
    ("concentracao_consultas_paciente_ativo", "Concentração de consultas por paciente ativo"),
    ("porcentagem_consultas_concluidas", "Porcentagem de consultas concluídas em relação ao total"),
    ("porcentagem_consultas_reguladas",         "Porcentagem de consultas reguladas"),
    ("porcentagem_interconsultas",              "Porcentagem de interconsultas"),
    ("porcentagem_consultas_retorno",           "Porcentagem de consultas de retorno"),
    ("media_reguladas_por_paciente", "Consultas reguladas por paciente"),
    ("media_retornos_por_paciente", "Consultas retorno por paciente"),
    ("media_interconsultas_por_paciente", "Interconsultas por paciente"),
    ("tempo_medio_criacao_prontuario_primeiro_agendamento", "Tempo medio entre a criação de prontuário e o primeiro agendamento"),
    ("encaminhamentos_por_consulta_regulada", "Encaminhamento frequente por consulta regulada"),
    ("intervalo_medio_regulada_primeiro_retorno", "Intervalo médio da consulta regulada ao primeiro retorno"),
    ("intervalo_medio_retornos_consecutivos", "Intervalo médio de retornos consecutivos"),
    ("porcentagem_faltas_profissionais",      "Porcentagem de faltas por parte do profissional"),
    ("porcentagem_faltas_pacientes",          "Porcentagem de faltas por parte do paciente"),
    ("tempo_medio_agendamento_realizacao",    "Tempo médio de agendamento até realização (horas)"),
    ("porcentagem_pacientes_com_interconsulta", "Porcentagem de pacientes com pelo menos uma interconsulta"),
    ("proporcao_consultas_sem_prontuario",      "Porcentagem de consultas sem prontuário registrado"),
]

_METRICAS_EVENTOS: list[tuple[str, str]] = [
    ("consultas_registradas", "Consultas registradas"),
    ("consultas_concluidas", "Consultas concluídas"),
    ("consultas_primeira_vez", "Consultas pela primeira vez"),
]

def dicionario_eventos(consultas):
    return {
        "consultas_registradas": len(consultas),
        "consultas_concluidas": len(consultas_concluidas(consultas=consultas)),
        "consultas_primeira_vez": len(consultas_primeira_vez(consultas=consultas))
    }

def eventos_consultas(consultas):
    eventos = dicionario_eventos(consultas=consultas)
    indicadores = []
    
    for evento, nome_display in _METRICAS_EVENTOS:
        if evento not in eventos:
            continue
        
        valor = eventos[evento]
        indicadores.append({
            "nome": nome_display,
            "valor": valor
        })    
    
    return indicadores

def metricas_consultas_como_indicadores(consultas: list[dict[str, Any]], pacientes: list) -> list[dict]:
    metricas = dicionario_metricas_consultas(consultas, pacientes)

    indicadores = []

    for metrica_key, nome in _METRICAS_INDICADORES:
        if metrica_key not in metricas:
            continue

        valor = metricas[metrica_key]

        indicadores.append({
            "nome": nome,
            "valor": valor,
        })

    return indicadores

