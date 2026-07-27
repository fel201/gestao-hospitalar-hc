# Formato de data esperado: 'dd/m/yyyy, HH:MM'  (ex: '13/1/2025, 09:51')

from functools import lru_cache
from ..helpers.jornada_utils import calcular_diferenca_horas, dias_entre
from ..helpers.math_utils import divisao_segura
from .helpers.filtrar_eventos import filtrar_eventos, filtrar_eventos_por_periodo
from datetime import datetime
from collections import defaultdict
from typing import Any
RETORNO_ATENDIDO             = "PACIENTE ATENDIDO"
RETORNO_PACIENTE_FALTOU      = "PACIENTE FALTOU"
RETORNO_PROFISSIONAL_FALTOU  = "PROFISSIONAL FALTOU"
RETORNO_AGENDADO             = "PACIENTE AGENDADO"

CONDICAO_PRIMEIRA  = "PRIMEIRA CONSULTA"
CONDICAO_RETORNO   = "RETORNO"
CONDICAO_REGULADA  = "CONSULTA REGULADA"
CONDICAO_INTERCON  = "INTERCONSULTA"

DATE_FMT = "%d/%m/%Y, %H:%M"


# helpers internos

def _parse_dt_uncached(s: str) -> datetime | None:
    """Converte string de data/hora para datetime; retorna None se inválida."""
    if not s:
        return None
    try:
        return datetime.strptime(s.strip(), DATE_FMT)
    except ValueError:
        return None


@lru_cache(maxsize=None)
def _parse_dt_cached(s: str) -> datetime | None:
    return _parse_dt_uncached(s)


def _parse_dt(s: str) -> datetime | None:
    if not s:
        return None
    return _parse_dt_cached(s.strip())


# agregação única, evita N passagens separadas sobre consultas


def _agregar_consultas(consultas: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Uma única varredura de `consultas` que acumula todos os contadores e
    agrupamentos usados pelas métricas abaixo. As funções de métrica passam
    a ler diretamente desse agregado em vez de re-percorrer a lista.
    """
    total = len(consultas)

    atendidas = 0
    faltas_paciente = 0
    faltas_profissional = 0
    reguladas = 0
    retornos = 0
    interconsultas = 0
    sem_prontuario = 0
    primeira_vez = 0

    pacientes: set[str] = set()
    retornos_por_paciente: dict[str, int] = defaultdict(int)
    interconsultas_por_paciente: dict[str, int] = defaultdict(int)
    reguladas_por_paciente: dict[str, int] = defaultdict(int)
    eventos_por_prontuario: dict[str, list[dict]] = defaultdict(list)

    for c in consultas:
        retorno = c.get("retorno", "")
        condicao = c.get("condicao", "")
        prontuario = c.get("prontuario", "")

        if RETORNO_ATENDIDO in retorno:
            atendidas += 1
        if RETORNO_PACIENTE_FALTOU in retorno:
            faltas_paciente += 1
        if RETORNO_PROFISSIONAL_FALTOU in retorno:
            faltas_profissional += 1
        if CONDICAO_REGULADA in condicao:
            reguladas += 1
        if CONDICAO_RETORNO in condicao:
            retornos += 1
        if CONDICAO_INTERCON in condicao:
            interconsultas += 1
        if CONDICAO_PRIMEIRA in condicao:
            primeira_vez += 1
        if prontuario == "":
            sem_prontuario += 1

        if prontuario:
            pacientes.add(prontuario)
            eventos_por_prontuario[prontuario].append(c)
            if CONDICAO_RETORNO in condicao:
                retornos_por_paciente[prontuario] += 1
            if CONDICAO_INTERCON in condicao:
                interconsultas_por_paciente[prontuario] += 1
            if CONDICAO_REGULADA in condicao:
                reguladas_por_paciente[prontuario] += 1

    return {
        "total": total,
        "atendidas": atendidas,
        "faltas_paciente": faltas_paciente,
        "faltas_profissional": faltas_profissional,
        "reguladas": reguladas,
        "retornos": retornos,
        "interconsultas": interconsultas,
        "primeira_vez": primeira_vez,
        "sem_prontuario": sem_prontuario,
        "pacientes": pacientes,
        "retornos_por_paciente": retornos_por_paciente,
        "interconsultas_por_paciente": interconsultas_por_paciente,
        "reguladas_por_paciente": reguladas_por_paciente,
        "eventos_por_prontuario": eventos_por_prontuario,
    }


def _pacientes_com_intercon(agg: dict) -> set[str]:
    return set(agg["interconsultas_por_paciente"].keys())



def concentracao_consultas_paciente_ativo(
    consultas: list[dict],
    data_inicio: str,
    data_fim: str
) -> dict[str, float]:

    formato_consulta = "%d/%m/%Y, %H:%M"
    formato_api = "%Y-%m-%d"

    inicio = datetime.strptime(data_inicio, formato_api)
    fim = datetime.strptime(data_fim, formato_api)

    consultas_por_mes = defaultdict(int)
    pacientes_por_mes = defaultdict(set)

    # agrupa consultas que estiverem dentro do intervalo
    for consulta in consultas:
        data_str = consulta.get("data_hora_realizacao")
        prontuario = consulta.get("prontuario")

        if not data_str or not prontuario:
            continue

        try:
            data = datetime.strptime(data_str, formato_consulta)
        except ValueError:
            continue

        if not (inicio <= data <= fim):
            continue

        chave_mes = data.strftime("%m/%Y")

        consultas_por_mes[chave_mes] += 1
        pacientes_por_mes[chave_mes].add(prontuario)

    meses = []

    ano = fim.year
    mes = fim.month

    while True:
        primeiro_dia_mes = datetime(ano, mes, 1)

        if primeiro_dia_mes < datetime(inicio.year, inicio.month, 1):
            break

        meses.append(f"{mes:02d}/{ano}")

        if len(meses) == 5:
            break

        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1

    meses.reverse()

    resultado = {}

    for mes in meses:
        resultado[mes] = round(
            divisao_segura(
                consultas_por_mes.get(mes, 0),
                len(pacientes_por_mes.get(mes, set()))
            ),
            2
        )

    return resultado

def consultas_primeira_vez(consultas):
    return [c for c in consultas if CONDICAO_PRIMEIRA in c["condicao"]]


def consultas_concluidas(consultas):
    return [c for c in consultas if RETORNO_ATENDIDO in c["retorno"]]


def porcentagem_consultas_concluidas(consultas):
    consultas_con = consultas_concluidas(consultas=consultas)
    taxa = round(divisao_segura(len(consultas_con), len(consultas)) * 100, 2)
    return f"{taxa}%"


def porcentagem_consultas_reguladas(consultas: list[dict[str, Any]]) -> str:
    total = len(consultas)
    reguladas = sum(1 for c in consultas if CONDICAO_REGULADA in c.get("condicao", ""))
    proporcao = round(divisao_segura(reguladas, total) * 100, 2)
    return f"{proporcao}%"


def porcentagem_faltas_pacientes(consultas: list[dict[str, Any]]) -> str:
    total = len(consultas)
    faltas = sum(1 for c in consultas if RETORNO_PACIENTE_FALTOU in c.get("retorno", ""))
    porcentagem = round(divisao_segura(faltas, total) * 100, 2)
    return f"{porcentagem}%"


def porcentagem_faltas_profissional(consultas: list[dict[str, Any]]) -> str:
    total = len(consultas)
    faltas = sum(1 for c in consultas if RETORNO_PROFISSIONAL_FALTOU in c.get("retorno", ""))
    porcentagem = round(divisao_segura(faltas, total) * 100, 2)
    return f"{porcentagem}%"


def tempo_medio_agendamento_realizacao(consultas: list[dict[str, Any]]) -> dict:
    """
    Tempo médio (em horas) entre o horário agendado da consulta
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
    return round(media, 4)


def porcentagem_consultas_sem_prontuario(consultas: list[dict[str, Any]]) -> str:
    total = len(consultas)
    consultas_sem_prontuario = [c for c in consultas if c["prontuario"] == ""]
    proporcao = round(divisao_segura(len(consultas_sem_prontuario), total) * 100, 2)
    return f"{proporcao}%"


def porcentagem_consultas_retorno(consultas: list[dict[str, Any]]) -> str:
    total = len(consultas)
    retornos = sum(1 for c in consultas if CONDICAO_RETORNO in c.get("condicao", ""))
    proporcao = round(divisao_segura(retornos, total) * 100, 2)
    return f"{proporcao}%"


def media_retornos_por_paciente(consultas: list[dict[str, Any]]) -> float:
    retornos_por_paciente: dict[str, int] = defaultdict(int)
    for c in consultas:
        if CONDICAO_RETORNO in c.get("condicao", ""):
            pid = c.get("prontuario", "")
            if pid:
                retornos_por_paciente[pid] += 1

    total_pacientes = len(retornos_por_paciente)
    total_retornos = sum(retornos_por_paciente.values())
    return round(divisao_segura(total_retornos, total_pacientes), 2)


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
    return round(total_interconsultas / total_pacientes, 2)


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
    return round(total_reguladas / total_pacientes, 2)


def intervalo_medio_regulada_primeiro_retorno(consultas: list[dict[str, Any]]) -> dict:
    """
    Para cada paciente, encontra a consulta regulada mais antiga e o primeiro
    retorno posterior. Calcula a média desses intervalos em dias.
    """
    por_paciente: dict[str, list[dict]] = defaultdict(list)
    for c in consultas:
        prontuario = c.get("prontuario", "")
        if prontuario:
            por_paciente[prontuario].append(c)

    intervalos = []
    for prontuario, eventos in por_paciente.items():
        reguladas = sorted(
            (e for e in eventos if CONDICAO_REGULADA in e.get("condicao", "")),
            key=lambda e: _parse_dt(e.get("data_hora_realizacao", "")) or datetime.max,
        )
        retornos = sorted(
            (e for e in eventos if CONDICAO_RETORNO in e.get("condicao", "")),
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
    return round(sum(intervalos) / len(intervalos), 2)


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


def tempo_medio_criacao_prontuario_primeiro_agendamento(pacientes, consultas):
    primeira_consulta_por_prontuario: dict[str, dict] = {}

    for consulta in consultas:
        prontuario = consulta["prontuario"]
        data_hora = _parse_dt(consulta["data_hora_realizacao"])
        if data_hora is None:
            continue

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

        if primeiro_evento is None:
            continue

        data_cadastro = f'{paciente["data_cadastro"]}, 00:00'

        tempo_total += dias_entre(data_cadastro, primeiro_evento["data_hora_realizacao"])
        quantidade += 1

    if quantidade == 0:
        return 0
    media = round(tempo_total / quantidade, 2) 
    return f"{media} dias"


def encaminhamentos_por_consulta_regulada(consultas: list[dict[str, Any]]) -> dict:
    por_paciente: dict[str, list[dict]] = defaultdict(list)
    for c in consultas:
        pid = c.get("prontuario", "")
        if pid:
            por_paciente[pid].append(c)

    encaminhamentos: dict[str, int] = defaultdict(int)
    encaminhamentos["SEM SEGUIMENTO"] = 0
    encaminhamentos[CONDICAO_RETORNO] = 0
    encaminhamentos[CONDICAO_INTERCON] = 0

    for pid, eventos in por_paciente.items():
        eventos_ord = sorted(
            eventos,
            key=lambda e: _parse_dt(e.get("data_hora_realizacao", "")) or datetime.max,
        )
        for i, ev in enumerate(eventos_ord):
            if CONDICAO_REGULADA not in ev.get("condicao", ""):
                continue
            if i + 1 < len(eventos_ord):
                proximo = eventos_ord[i + 1].get("condicao", "SEM SEGUIMENTO").strip()
                encaminhamentos[proximo] += 1
            else:
                encaminhamentos["SEM SEGUIMENTO"] += 1

    return dict(sorted(encaminhamentos.items(), key=lambda x: x[1], reverse=True))


def porcentagem_interconsultas(consultas: list[dict[str, Any]]) -> str:
    total = len(consultas)
    interconsultas = sum(1 for c in consultas if CONDICAO_INTERCON in c.get("condicao", ""))
    proporcao = round(divisao_segura(interconsultas, total) * 100, 2)
    return f"{proporcao}%"


def porcentagem_pacientes_com_interconsulta(consultas: list[dict[str, Any]]) -> str:
    todos = {c.get("prontuario") for c in consultas if c.get("prontuario")}
    com_intercon = {
        c.get("prontuario")
        for c in consultas
        if CONDICAO_INTERCON in c.get("condicao", "") and c.get("prontuario")
    }
    proporcao = round(divisao_segura(len(com_intercon), len(todos)) * 100, 2)
    return f"{proporcao}%"



def filtrar_consultas(consultas, especialidade, data_inicio, data_fim):
    return filtrar_eventos_por_periodo(
        filtrar_eventos(evento="consulta", dados=consultas, especialidade=especialidade),
        data_inicio,
        data_fim,
    )


def dicionario_metricas_consultas(
    consultas: list[dict[str, Any]],
    pacientes: list[dict[str, Any]],
    especialidade: str,
    data_inicio: str,
    data_fim: str,
) -> dict:
    consultas_filtradas = filtrar_consultas(consultas, especialidade, data_inicio, data_fim)
    agg = _agregar_consultas(consultas_filtradas)
    total = agg["total"]
    n_pacientes = len(agg["pacientes"])

    porcentagem_concluidas = round(divisao_segura(agg["atendidas"], total) * 100, 2)
    porcentagem_reguladas = round(divisao_segura(agg["reguladas"], total) * 100, 2)
    porcentagem_retorno = round(divisao_segura(agg["retornos"], total) * 100, 2)
    porcentagem_intercon = round(divisao_segura(agg["interconsultas"], total) * 100, 2)
    porcentagem_falta_pac = round(divisao_segura(agg["faltas_paciente"], total) * 100, 2)
    porcentagem_falta_prof = round(divisao_segura(agg["faltas_profissional"], total) * 100, 2)
    porcentagem_sem_prontuario = round(divisao_segura(agg["sem_prontuario"], total) * 100, 2)

    total_retornos_pac = sum(agg["retornos_por_paciente"].values())
    n_pac_com_retorno = len(agg["retornos_por_paciente"])
    media_retornos = round(divisao_segura(total_retornos_pac, n_pac_com_retorno), 2)

    total_intercon_pac = sum(agg["interconsultas_por_paciente"].values())
    n_pac_com_intercon = len(agg["interconsultas_por_paciente"])
    media_intercon = (
        round(total_intercon_pac / n_pac_com_intercon, 2) if n_pac_com_intercon else 0.0
    )
    media_reguladas = media_intercon

    porcentagem_pac_com_intercon = round(
        divisao_segura(n_pac_com_intercon, n_pacientes) * 100, 2
    )

    return {
        "concentracao_consultas_paciente_ativo": concentracao_consultas_paciente_ativo(consultas=consultas_filtradas, data_inicio=data_inicio, data_fim=data_fim),
        "porcentagem_consultas_concluidas": f"{porcentagem_concluidas}%",
        "porcentagem_consultas_reguladas": f"{porcentagem_reguladas}%",
        "intervalo_medio_regulada_primeiro_retorno": intervalo_medio_regulada_primeiro_retorno(consultas=consultas_filtradas),
        "intervalo_medio_retornos_consecutivos": intervalo_medio_retornos_consecutivos(consultas=consultas_filtradas),
        "media_reguladas_por_paciente": media_reguladas,
        "media_retornos_por_paciente": media_retornos,
        "media_interconsultas_por_paciente": media_intercon,
        "proporcao_consultas_sem_prontuario": f"{porcentagem_sem_prontuario}%",
        "tempo_medio_criacao_prontuario_primeiro_agendamento_global": tempo_medio_criacao_prontuario_primeiro_agendamento(pacientes=pacientes, consultas=consultas),
        "porcentagem_faltas_profissionais": f"{porcentagem_falta_prof}%",
        "encaminhamentos_por_consulta_regulada": encaminhamentos_por_consulta_regulada(consultas=consultas_filtradas),
        "porcentagem_faltas_pacientes": f"{porcentagem_falta_pac}%",
        "tempo_medio_agendamento_realizacao": tempo_medio_agendamento_realizacao(consultas),
        "porcentagem_consultas_retorno": f"{porcentagem_retorno}%",
        "porcentagem_interconsultas": f"{porcentagem_intercon}%",
        "porcentagem_pacientes_com_interconsulta": f"{porcentagem_pac_com_intercon}%",
    }



# flatten: converte o dict de métricas em lista de {nome, valor}

_METRICAS_INDICADORES: list[tuple[str, str]] = [
    ("concentracao_consultas_paciente_ativo", "Concentração de consultas por paciente ativo"),
    ("porcentagem_consultas_concluidas", "Porcentagem de consultas concluídas em relação ao total"),
    ("porcentagem_consultas_reguladas", "Porcentagem de consultas reguladas"),
    ("porcentagem_interconsultas", "Porcentagem de interconsultas"),
    ("porcentagem_consultas_retorno", "Porcentagem de consultas de retorno"),
    ("media_reguladas_por_paciente", "Consultas reguladas por paciente"),
    ("media_retornos_por_paciente", "Consultas retorno por paciente"),
    ("media_interconsultas_por_paciente", "Interconsultas por paciente"),
    ("encaminhamentos_por_consulta_regulada", "Encaminhamento frequente por consulta regulada"),
    ("intervalo_medio_regulada_primeiro_retorno", "Intervalo médio da consulta regulada ao primeiro retorno"),
    ("intervalo_medio_retornos_consecutivos", "Intervalo médio de retornos consecutivos"),
    ("porcentagem_faltas_profissionais", "Porcentagem de faltas por parte do profissional"),
    ("porcentagem_faltas_pacientes", "Porcentagem de faltas por parte do paciente"),
    ("tempo_medio_agendamento_realizacao", "Tempo médio de agendamento até realização (horas)"),
    ("porcentagem_pacientes_com_interconsulta", "Porcentagem de pacientes com pelo menos uma interconsulta"),
    ("proporcao_consultas_sem_prontuario", "Porcentagem de consultas sem prontuário registrado"),
    ("tempo_medio_criacao_prontuario_primeiro_agendamento_global", "Tempo medio global entre a criação de prontuário e o primeiro agendamento")
]

_METRICAS_EVENTOS: list[tuple[str, str]] = [
    ("consultas_registradas", "Consultas registradas"),
    ("consultas_concluidas", "Consultas concluídas"),
    ("consultas_primeira_vez", "Consultas pela primeira vez"),
]


def dicionario_eventos(consultas):
    agg = _agregar_consultas(consultas)
    return {
        "consultas_registradas": agg["total"],
        "consultas_concluidas": agg["atendidas"],
        "consultas_primeira_vez": agg["primeira_vez"],
    }


def eventos_consultas(consultas):
    eventos = dicionario_eventos(consultas=consultas)
    indicadores = []

    for evento, nome_display in _METRICAS_EVENTOS:
        if evento not in eventos:
            continue
        indicadores.append({"nome": nome_display, "valor": eventos[evento]})

    return indicadores


def metricas_consultas_como_indicadores(consultas: list[dict[str, Any]], pacientes: list, data_inicio: str, data_fim: str, especialidade: str) -> list[dict]:
    metricas = dicionario_metricas_consultas(
        consultas=consultas,
        pacientes=pacientes,
        especialidade=especialidade,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

    indicadores = []
    for metrica_key, nome in _METRICAS_INDICADORES:
        if metrica_key not in metricas:
            continue
        indicadores.append({"nome": nome, "valor": metricas[metrica_key]})

    return indicadores