"""
Módulo de métricas de consultas para o dashboard de jornada do paciente.

Baseado nas colunas disponíveis no consultas.csv e no formato da variável
`consultas_filtradas` (lista de dicts) retornada pelo ConsultasCsvProvider.

Colunas chave utilizadas:
  - data_hora_consulta  → 'Data/Hora da Consulta'
  - data_hora_fim       → 'Data/Hora de Fim'
  - retorno             → 'Retorno'
  - condicao            → 'Condição do Atendimento'
  - cid                 → 'CID'
  - paciente_id         → 'ID do Paciente'
  - num_consulta        → 'num_consulta'
  - prontuario          → 'Prontuario'
  - especialidade       → 'especialidade'

Formato de data esperado: 'dd/m/yyyy, HH:MM'  (ex: '13/1/2025, 09:51')
"""

from __future__ import annotations

from datetime import datetime
from collections import defaultdict
from typing import Any

RETORNO_ATENDIDO   = "PACIENTE ATENDIDO"
RETORNO_FALTOU     = "PACIENTE FALTOU"
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


def _horas_entre(inicio: str, fim: str) -> float | None:
    """Diferença em horas entre duas strings de data/hora. Retorna None se inválido."""
    dt_ini = _parse_dt(inicio)
    dt_fim = _parse_dt(fim)
    if dt_ini is None or dt_fim is None:
        return None
    delta = dt_fim - dt_ini
    return delta.total_seconds() / 3600


def _dias_entre(inicio: str, fim: str) -> float | None:
    """Diferença em dias entre duas strings de data/hora."""
    h = _horas_entre(inicio, fim)
    return h / 24 if h is not None else None


# 1. proporção de consultas reguladas vs. total


def proporcao_consultas_reguladas(consultas: list[dict[str, Any]]) -> dict:
    """
    Calcula a proporção de consultas com Condição = 'CONSULTA REGULADA'
    em relação ao total.

    Retorna:
        {
            "total": int,
            "reguladas": int,
            "proporcao": float   # 0.0 – 1.0
        }
    """
    total = len(consultas)
    if total == 0:
        return {"total": 0, "reguladas": 0, "proporcao": 0.0}

    reguladas = sum(
        1 for c in consultas
        if CONDICAO_REGULADA in c.get("condicao", "")
    )
    return {
        "total": total,
        "reguladas": reguladas,
        "proporcao": round(reguladas / total, 4),
    }


# 2. taxa de não realização — faltas e cancelamentos

def taxa_nao_realizacao(consultas: list[dict[str, Any]]) -> dict:
    """
    Calcula a taxa de não realização (faltas + cancelamentos) das consultas.

    Considera como 'não realizada' qualquer consulta cujo `retorno` contenha
    'FALTOU' ou 'CANCELAD'.

    Retorna:
        {
            "total": int,
            "faltas": int,
            "taxa_faltas": float,
            "nao_realizadas": int,
            "taxa_nao_realizacao": float
        }
    """
    total = len(consultas)
    if total == 0:
        return {
            "total": 0, "faltas": 0, "taxa_faltas": 0.0,
            "nao_realizadas": 0, "taxa_nao_realizacao": 0.0,
        }

    faltas = sum(1 for c in consultas if "FALTOU" in c.get("retorno", ""))
    cancelamentos = sum(1 for c in consultas if "CANCELAD" in c.get("retorno", ""))
    nao_realizadas = faltas + cancelamentos

    return {
        "total": total,
        "faltas": faltas,
        "cancelamentos": cancelamentos,
        "taxa_faltas": round(faltas / total, 4),
        "nao_realizadas": nao_realizadas,
        "taxa_nao_realizacao": round(nao_realizadas / total, 4),
    }

# 3. tempo médio entre agendamento e realização da consulta
#    (Data/Hora da Consulta = agendado;  Data/Hora de Fim = realizado)

def tempo_medio_agendamento_realizacao(consultas: list[dict[str, Any]]) -> dict:
    """
    Tempo médio (em horas) entre o horário agendado da consulta
    e o momento em que ela foi finalizada.

    Considera apenas consultas com Retorno = 'PACIENTE ATENDIDO' e
    com ambas as datas preenchidas.

    Retorna:
        {
            "n_consultas": int,
            "media_horas": float,
            "media_minutos": float
        }
    """
    deltas = []
    for c in consultas:
        if RETORNO_ATENDIDO not in c.get("retorno", ""):
            continue
        h = _horas_entre(c.get("data_hora_consulta", ""), c.get("data_hora_fim", ""))
        if h is not None and h >= 0:
            deltas.append(h)

    if not deltas:
        return {"n_consultas": 0, "media_horas": 0.0, "media_minutos": 0.0}

    media_h = sum(deltas) / len(deltas)
    return {
        "n_consultas": len(deltas),
        "media_horas": round(media_h, 4),
        "media_minutos": round(media_h * 60, 2),
    }


# 4. Proporção de consultas de retorno vs. total

def proporcao_consultas_retorno(consultas: list[dict[str, Any]]) -> dict:
    """
    Proporção de consultas com Condição = 'RETORNO' sobre o total.

    Retorna:
        {
            "total": int,
            "retornos": int,
            "proporcao": float
        }
    """
    total = len(consultas)
    if total == 0:
        return {"total": 0, "retornos": 0, "proporcao": 0.0}

    retornos = sum(1 for c in consultas if CONDICAO_RETORNO in c.get("condicao", ""))
    return {
        "total": total,
        "retornos": retornos,
        "proporcao": round(retornos / total, 4),
    }


# 5. Número médio de retornos por paciente

def media_retornos_por_paciente(consultas: list[dict[str, Any]]) -> dict:
    """
    Calcula o número médio de consultas de retorno por paciente.

    Retorna:
        {
            "total_pacientes": int,
            "total_retornos": int,
            "media_retornos_por_paciente": float
        }
    """
    retornos_por_paciente: dict[str, int] = defaultdict(int)

    for c in consultas:
        if CONDICAO_RETORNO in c.get("condicao", ""):
            pid = c.get("paciente_id", "")
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

    return {
        "total_pacientes": total_pacientes,
        "total_retornos": total_retornos,
        "media_retornos_por_paciente": round(total_retornos / total_pacientes, 2),
    }



# 6. intervalo médio entre consulta regulada e primeiro retorno (por paciente)
# métrica geral
# não foi utilizada
def intervalo_medio_regulada_primeiro_retorno(consultas: list[dict[str, Any]]) -> dict:
    """
    Para cada paciente, encontra a consulta regulada mais antiga e o primeiro
    retorno posterior. Calcula a média desses intervalos em dias.

    Retorna:
        {
            "n_pacientes": int,
            "media_dias": float
        }
    """
    # Agrupa por paciente
    por_paciente: dict[str, list[dict]] = defaultdict(list)
    for c in consultas:
        pid = c.get("paciente_id", "")
        if pid:
            por_paciente[pid].append(c)

    intervalos = []
    for pid, eventos in por_paciente.items():
        reguladas = sorted(
            [e for e in eventos if CONDICAO_REGULADA in e.get("condicao", "")],
            key=lambda e: _parse_dt(e.get("data_hora_consulta", "")) or datetime.max,
        )
        retornos = sorted(
            [e for e in eventos if CONDICAO_RETORNO in e.get("condicao", "")],
            key=lambda e: _parse_dt(e.get("data_hora_consulta", "")) or datetime.max,
        )

        if not reguladas or not retornos:
            continue

        dt_reg = _parse_dt(reguladas[0].get("data_hora_consulta", ""))
        if dt_reg is None:
            continue

        # Primeiro retorno APÓS a consulta regulada
        primeiro_retorno = next(
            (
                r for r in retornos
                if (_parse_dt(r.get("data_hora_consulta", "")) or datetime.min) > dt_reg
            ),
            None,
        )
        if primeiro_retorno is None:
            continue

        dias = _dias_entre(
            reguladas[0].get("data_hora_consulta", ""),
            primeiro_retorno.get("data_hora_consulta", ""),
        )
        if dias is not None and dias >= 0:
            intervalos.append(dias)

    if not intervalos:
        return {"n_pacientes": 0, "media_dias": 0.0}

    return {
        "n_pacientes": len(intervalos),
        "media_dias": round(sum(intervalos) / len(intervalos), 2),
    }


# 7. Intervalo médio entre retornos consecutivos (por paciente)
# ainda não foi utilizado, pois é uma métrica geral

def intervalo_medio_retornos_consecutivos(consultas: list[dict[str, Any]]) -> dict:
    """
    Para cada paciente com mais de um retorno, calcula os intervalos entre
    retornos consecutivos. Retorna a média global em dias.

    Retorna:
        {
            "n_intervalos": int,
            "media_dias": float
        }
    """
    por_paciente: dict[str, list[dict]] = defaultdict(list)
    for c in consultas:
        pid = c.get("paciente_id", "")
        if pid and CONDICAO_RETORNO in c.get("condicao", ""):
            por_paciente[pid].append(c)

    intervalos = []
    for pid, retornos in por_paciente.items():
        retornos_ord = sorted(
            retornos,
            key=lambda e: _parse_dt(e.get("data_hora_consulta", "")) or datetime.max,
        )
        for i in range(1, len(retornos_ord)):
            dias = _dias_entre(
                retornos_ord[i - 1].get("data_hora_consulta", ""),
                retornos_ord[i].get("data_hora_consulta", ""),
            )
            if dias is not None and dias >= 0:
                intervalos.append(dias)

    if not intervalos:
        return {"n_intervalos": 0, "media_dias": 0.0}

    return {
        "n_intervalos": len(intervalos),
        "media_dias": round(sum(intervalos) / len(intervalos), 2),
    }



# 8. Tipos de encaminhamento mais gerados por consulta regulada
# (usa o campo `condicao` das consultas relacionadas ao mesmo paciente)
# essa é uma métrica mais geral, não deve estar dentro do módulo consultas.
# ainda não foi utilizada

def encaminhamentos_por_consulta_regulada(consultas: list[dict[str, Any]]) -> dict:
    """
    Após cada consulta regulada, verifica qual o próximo tipo de evento
    do mesmo paciente (retorno, interconsulta, etc.) e conta as ocorrências.

    Retorna:
        {
            "total_reguladas": int,
            "encaminhamentos": {tipo: contagem, ...}   # ordenado por contagem desc
        }
    """
    por_paciente: dict[str, list[dict]] = defaultdict(list)
    for c in consultas:
        pid = c.get("paciente_id", "")
        if pid:
            por_paciente[pid].append(c)

    encaminhamentos: dict[str, int] = defaultdict(int)
    total_reguladas = 0

    for pid, eventos in por_paciente.items():
        eventos_ord = sorted(
            eventos,
            key=lambda e: _parse_dt(e.get("data_hora_consulta", "")) or datetime.max,
        )
        for i, ev in enumerate(eventos_ord):
            if CONDICAO_REGULADA not in ev.get("condicao", ""):
                continue
            total_reguladas += 1
            # Próximo evento do mesmo paciente
            if i + 1 < len(eventos_ord):
                proximo = eventos_ord[i + 1].get("condicao", "SEM SEGUIMENTO").strip()
                encaminhamentos[proximo] += 1
            else:
                encaminhamentos["SEM SEGUIMENTO"] += 1

    return {
        "total_reguladas": total_reguladas,
        "encaminhamentos": dict(
            sorted(encaminhamentos.items(), key=lambda x: x[1], reverse=True)
        ),
    }



# 9. Proporção de interconsultas vs. total de consultas

def proporcao_interconsultas(consultas: list[dict[str, Any]]) -> dict:
    """
    Proporção de consultas com Condição = 'INTERCONSULTA' sobre o total.

    Retorna:
        {
            "total": int,
            "interconsultas": int,
            "proporcao": float
        }
    """
    total = len(consultas)
    if total == 0:
        return {"total": 0, "interconsultas": 0, "proporcao": 0.0}

    interconsultas = sum(
        1 for c in consultas if CONDICAO_INTERCON in c.get("condicao", "")
    )
    return {
        "total": total,
        "interconsultas": interconsultas,
        "proporcao": round(interconsultas / total, 4),
    }


# 10. Proporção de pacientes com pelo menos uma interconsulta

def proporcao_pacientes_com_interconsulta(consultas: list[dict[str, Any]]) -> dict:
    """
    Calcula a proporção de pacientes únicos que possuem ao menos uma
    consulta com Condição = 'INTERCONSULTA'.

    Retorna:
        {
            "total_pacientes": int,
            "pacientes_com_interconsulta": int,
            "proporcao": float
        }
    """
    todos = {c.get("paciente_id") for c in consultas if c.get("paciente_id")}
    com_intercon = {
        c.get("paciente_id")
        for c in consultas
        if CONDICAO_INTERCON in c.get("condicao", "") and c.get("paciente_id")
    }

    total = len(todos)
    if total == 0:
        return {"total_pacientes": 0, "pacientes_com_interconsulta": 0, "proporcao": 0.0}

    return {
        "total_pacientes": total,
        "pacientes_com_interconsulta": len(com_intercon),
        "proporcao": round(len(com_intercon) / total, 4),
    }



# função de conveniência: roda todas as métricas de uma vez
def calcular_todas_metricas_consultas(consultas: list[dict[str, Any]]) -> dict:
    """
    Executa todas as métricas acima e retorna um dicionário consolidado.

    Exemplo de uso:
        consultas = await consulta_provider.listar_consultas()
        resultado = calcular_todas_metricas_consultas(consultas)
    """
    return {
        "proporcao_consultas_reguladas":            proporcao_consultas_reguladas(consultas),
        "taxa_nao_realizacao":                      taxa_nao_realizacao(consultas),
        "tempo_medio_agendamento_realizacao":       tempo_medio_agendamento_realizacao(consultas),
        "proporcao_consultas_retorno":              proporcao_consultas_retorno(consultas),
        "media_retornos_por_paciente":              media_retornos_por_paciente(consultas),
        "proporcao_interconsultas":                 proporcao_interconsultas(consultas),
        "proporcao_pacientes_com_interconsulta":    proporcao_pacientes_com_interconsulta(consultas),
    }
    
    

# Flatten: converte o dict de métricas em lista de {nome, valor}
# compatível com DashboardIndicadorInterface
# Mapeamento explícito: (chave_metrica, nome_display, chave_valor)
# Permite escolher exatamente qual campo de cada métrica expor ao frontend.
_METRICAS_INDICADORES: list[tuple[str, str, str]] = [
    ("proporcao_consultas_reguladas",         "Proporção de consultas reguladas",       "proporcao"),
    ("taxa_nao_realizacao",                   "Taxa de faltas",                          "taxa_faltas"),
    ("taxa_nao_realizacao",                   "Taxa de não realização",                  "taxa_nao_realizacao"),
    ("tempo_medio_agendamento_realizacao",    "Tempo médio até realização (min)",        "media_minutos"),
    ("proporcao_consultas_retorno",           "Proporção de consultas de retorno",       "proporcao"),
    ("media_retornos_por_paciente",           "Média de retornos por paciente",          "media_retornos_por_paciente"),
    ("proporcao_interconsultas",              "Proporção de interconsultas",             "proporcao"),
    ("proporcao_pacientes_com_interconsulta", "Pacientes com interconsulta",         "proporcao"),
]
# só pra não repetir isso dentro da função dnv
_METRICAS_PERCENTUAIS = {
    "Proporção de consultas reguladas",
    "Taxa de faltas",
    "Taxa de não realização",
    "Proporção de consultas de retorno",
    "Proporção de interconsultas",
    "Pacientes com interconsulta",
}

def metricas_consultas_como_indicadores(consultas: list[dict[str, Any]]) -> list[dict]:
    metricas = calcular_todas_metricas_consultas(consultas)

    indicadores = []

    for metrica_key, nome, valor_key in _METRICAS_INDICADORES:
        if metrica_key not in metricas:
            continue

        valor = metricas[metrica_key][valor_key]

        if nome in _METRICAS_PERCENTUAIS:
            valor = f"{valor * 100:.2f}%"

        indicadores.append({
            "nome": nome,
            "valor": valor,
        })

    return indicadores

    return indicadores
