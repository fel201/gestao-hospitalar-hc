from ..helpers.jornada_utils import calcular_diferenca_horas, _mes_anterior
from .helpers.filtrar_eventos import filtrar_eventos
from ..helpers.formatacao import remover_acentos, padronizar_casas_decimais
from datetime import datetime
from typing import Any
import re

ESPECIALIDADE_AMBULATORIAL = "AMBULATORIO"
ESPECIALIDADE_UTI = "UTI"
ESPECIALIDADE_URGENCIA = "URGENCIA"
ESPECIALIDADE_CIRURGIA = "CIRUR"
CONDICAO_REGULADO = "REGULADO"
SITUACAO_CANCELADO = "CANCELADO"
SITUACAO_LIBERADO = "LIBERADO"
SITUACAO_A_COLETAR = "A COLETAR"

GRUPO_NAO_CLASSIFICADO = "Não classificado"

# Classificação dos exames por grupo de executor (unidade_executora_nome),
# conforme "HC4 T3 Exames - classificação". Bem mais granular que o antigo
# corte binário ambulatorial/emergencial-preoperatório, que olhava para a
# especialidade solicitante em vez de quem efetivamente executa o exame.
_TABELA_GRUPOS_EXECUTORES: dict[str, list[str]] = {
    "Análises Clínicas": [
        "UAC: BIOQUÍMICA",
        "UAC: SOROLOGIA",
        "UAC: HEMATOLOGIA",
        "UAC: BACTERIOLOGIA",
        "UAC: HEMOSTASIA",
        "UAC: UROANÁLISE",
        "UAC: GASOMETRIA",
        "UAC: EXAMES EXTERNOS",
        "UAC: EXAMES DA REDE",
    ],
    "Diagnóstico por Imagem": [
        "UDI: ULTRASSONOGRAFIA",
        "UDI: RADIOLOGIA CONVENCIONAL",
        "UDI: TOMOGRAFIA COMPUTADORIZADA",
        "UDI: DENSITOMETRIA ÓSSEA",
        "UDI: RESSONÂNCIA MAGNÉTICA",
        "UDI: MEDICINA NUCLEAR",
        "UDI: MAMOGRAFIA",
        "UNIDADE DE DIAGNÓSTICO POR IMAGEM",
    ],
    "Anatomia Patológica": [
        "UAP: HISTOPATOLÓGICO",
        "UAP: CITOLOGIA CÉRVICO-VAGINAL",
        "UAP: CITOLOGIA GERAL",
        "UAP: IMUNOHISTOQUÍMICA",
        "UAP: CONGELAÇÃO",
    ],
    "Procedimental": [
        "AGÊNCIA TRANSFUSIONAL",
        "ENDOSCOPIA",
        "HEMODINÂMICA-PDT",
        "BLOCO DERMATO",
        "NEFROLOGIA - PROCEDIMENTOS",
        "CENTRO OBSTÉTRICO",
    ],
    "Ambulatorial": [
        "OBSTETRÍCIA (AMBULATÓRIO)",
        "CARDIOLOGIA (AMBULATÓRIO)",
        "PNEUMOLOGIA (AMBULATÓRIO)",
        "GINECOLOGIA (AMBULATÓRIO)",
        "GASTROENTEROLOGIA (AMBULATÓRIO)",
        "NEUROLOGIA (AMBULATÓRIO)",
        "UROLOGIA (AMBULATÓRIO)",
        "INFECTOLOGIA (AMBULATÓRIO)",
        "HEMATOLOGIA (AMBULATÓRIO)",
        "OFTALMO GERAL",
        "OFTALMO ESPECIALIZADOS",
        "FONOAUDIOLOGIA",
    ],
    "Internação": [
        "8º SUL",
    ],
}


def _normalizar_executor(valor: str) -> str:
    """
    Normaliza o nome da unidade executora para comparação: remove acentos,
    coloca em maiúsculas e substitui pontuação (":", "(", ")", "-") por
    espaço, para casar "UAC: Bioquímica" com "UAC BIOQUIMICA" etc.
    """
    texto = remover_acentos(valor).upper()
    texto = re.sub(r"[():\-]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


_MAPA_EXECUTOR_GRUPO: dict[str, str] = {
    _normalizar_executor(nome): grupo
    for grupo, nomes in _TABELA_GRUPOS_EXECUTORES.items()
    for nome in nomes
}


def classificar_grupo_executor(unidade_executora_nome: str) -> str:
    """
    Classifica o exame em um dos grupos de executor (Análises Clínicas,
    Diagnóstico por Imagem, Anatomia Patológica, Procedimental, Ambulatorial,
    Internação), a partir do campo `unidade_executora_nome`. Valores que não
    batem com a tabela caem em GRUPO_NAO_CLASSIFICADO — útil para detectar
    unidades novas/não mapeadas que apareçam na base.
    """
    chave = _normalizar_executor(unidade_executora_nome)
    return _MAPA_EXECUTOR_GRUPO.get(chave, GRUPO_NAO_CLASSIFICADO)


def distribuicao_exames_por_grupo_executor(exames: list[dict]) -> dict[str, str]:
    """
    Retorna a porcentagem de exames por grupo de executor em relação ao
    total, ordenado do grupo com mais exames para o com menos. Retorna {} se
    não houver exames.
    """
    if not exames:
        return {}

    contagem: dict[str, int] = {}
    for e in exames:
        grupo = classificar_grupo_executor(e["unidade_executora_nome"])
        contagem[grupo] = contagem.get(grupo, 0) + 1

    total = len(exames)
    ordenado = sorted(contagem.items(), key=lambda item: item[1], reverse=True)

    return {grupo: _formatar_percentual(qtd, total) for grupo, qtd in ordenado}


_METRICAS_INDICADORES: list[tuple[str, str]] = [
    ("tempo_medio_solicitacao_realizacao_mensal", "Tempo médio de solicitação até a realização do exame por mês"),
    ("distribuicao_exames_por_grupo_executor", "Distribuição de exames por grupo de executor"),
    ("distribuicao_exames_por_grupo_executor_global", "Distribuição de exames por grupo de executor (global)"),
    ("porcentagem_exames_regulados", "Porcentagem de exames regulados"),
    ("porcentagem_global_exames_regulados", "Porcentagem global de exames regulados"),
    ("porcentagem_exames_concluidos", "Porcentagem de exames concluídos"),
    ("porcentagem_global_exames_concluidos", "Porcentagem global de exames concluídos"),
    ("porcentagem_exames_cancelados", "Porcentagem de exames marcados como pendentes"),
    ("porcentagem_global_exames_cancelados", "Porcentagem global de exames marcados como pendentes"),
]

# exames com umas das maiores taxas de conclusão
#


def qtd_exames_tipo(exames, tipo):
    total_exames_condicao = 0

    for e in exames:
        especialidade = remover_acentos(e["especialidade_solicitante_nome"])
        if tipo == "ambulatorial":
            if ESPECIALIDADE_AMBULATORIAL in especialidade:
                total_exames_condicao += 1
        elif tipo == "emergencial-preoperatorio" and (
            ESPECIALIDADE_UTI in especialidade
            or ESPECIALIDADE_URGENCIA in especialidade
            or ESPECIALIDADE_CIRURGIA in especialidade
        ):
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
    if not exames:
        return "0%"
    tamanho_exames_c = len(exames_cancelados(exames=exames))
    taxa = round((tamanho_exames_c / len(exames)) * 100, 2)
    return f"{taxa}%"


def porcentagem_exames_regulados(exames):
    if not exames:
        return "0%"
    p_exames_regulados = round(len(exames_regulados(exames=exames)) / len(exames) * 100, 2)
    return f"{p_exames_regulados}%"


def porcentagem_exames_concluidos(exames):
    if not exames:
        return "0%"
    n_exames_concluidos = len(exames_concluidos(exames=exames))
    p_exames_concluidos = round((n_exames_concluidos / len(exames)) * 100, 2)
    return f"{p_exames_concluidos}%"


def tempo_medio_solicitacao_realizacao(exames):
    if not exames:
        return 0

    soma = 0
    for exame in exames:
        soma += calcular_diferenca_horas(
            exame["data_hora_solicitacao"],
            exame["data_hora_realizacao"],
        )

    tempo_medio = soma / len(exames)
    res = padronizar_casas_decimais(tempo_medio) + " horas"
    return res


def porcentagem_exames_do_tipo(exames: list[dict], tipo: str):
    total_exames = len(exames)
    if total_exames == 0:
        return "0%"

    qtd_exames = qtd_exames_tipo(exames=exames, tipo=tipo)
    proporcao = round((qtd_exames / total_exames) * 100, 2)
    return f"{proporcao}%"


# total de exames realizados / numero de pacientes atendidos
# paciente ativo: aquele que já realizou pelo menos um exame no hospital
def concentracao_exames_por_paciente_ativo(exames: list[dict], tipo: str):
    if not exames:
        return 0

    pacientes = set()
    for e in exames:
        pacientes.add(e["prontuario"])

    qtd = qtd_exames_tipo(exames=exames, tipo=tipo)
    exames_amb_por_pac = round(qtd / len(pacientes), 2)
    print(exames_amb_por_pac)
    return exames_amb_por_pac


def _contadores_globais(exames: list[dict]) -> dict[str, int]:
    contadores = {
        "total": len(exames),
        "cancelados": 0,
        "concluidos": 0,
        "regulados": 0,
        "ambulatorial": 0,
        "emergencial_preoperatorio": 0,
    }

    for e in exames:
        if SITUACAO_CANCELADO in e["situacao"].upper():
            contadores["cancelados"] += 1
        if SITUACAO_LIBERADO in e["situacao"].upper():
            contadores["concluidos"] += 1
        if CONDICAO_REGULADO in e["condicao"].upper():
            contadores["regulados"] += 1

        especialidade = remover_acentos(e["especialidade_solicitante_nome"])
        if (
            ESPECIALIDADE_UTI in especialidade
            or ESPECIALIDADE_URGENCIA in especialidade
            or ESPECIALIDADE_CIRURGIA in especialidade
        ):
            contadores["emergencial_preoperatorio"] += 1
        if ESPECIALIDADE_AMBULATORIAL in especialidade:
            contadores["ambulatorial"] += 1

    return contadores

def _formatar_percentual(qtd: int, total: int) -> str:
    if total == 0:
        return "0%"
    return f"{round((qtd / total) * 100, 2)}%"


def _calcular_meses_alvo(data_inicio: str, data_fim: str, quantidade: int = 5) -> list[tuple[int, int]]:
    dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    dt_fim = datetime.strptime(data_fim, "%Y-%m-%d")

    ano_inicio, mes_inicio = dt_inicio.year, dt_inicio.month
    ano_atual, mes_atual = dt_fim.year, dt_fim.month

    meses_alvo = []
    while len(meses_alvo) < quantidade:
        meses_alvo.append((ano_atual, mes_atual))
        if (ano_atual, mes_atual) == (ano_inicio, mes_inicio):
            break
        ano_atual, mes_atual = _mes_anterior(ano_atual, mes_atual)

    meses_alvo.reverse()
    return meses_alvo


def _agrupar_exames_por_mes(
    exames: list[dict], meses_alvo: list[tuple[int, int]]
) -> dict[tuple[int, int], list[dict]]:
    meses_validos = set(meses_alvo)
    grupos: dict[tuple[int, int], list[dict]] = {chave: [] for chave in meses_alvo}

    for e in exames:
        data_exame = datetime.strptime(e["data_hora_realizacao"], "%d/%m/%Y, %H:%M")
        chave = (data_exame.year, data_exame.month)
        if chave in meses_validos:
            grupos[chave].append(e)

    return grupos


def tempo_medio_solicitacao_realizacao_mensal(
    exames: list[dict],
    data_inicio: str,
    data_fim: str,
    _grupos: dict[tuple[int, int], list[dict]] | None = None,
) -> dict:
    """
    Calcula o tempo médio entre solicitação e realização, mês a mês, olhando
    para os últimos 5 meses (ou menos, se o intervalo for menor).
    """
    meses_alvo = _calcular_meses_alvo(data_inicio, data_fim)
    grupos = _grupos if _grupos is not None else _agrupar_exames_por_mes(exames, meses_alvo)

    resultado = {}
    for ano, mes in meses_alvo:
        chave = f"{mes:02d}/{ano}"
        exames_do_mes = grupos.get((ano, mes), [])
        resultado[chave] = tempo_medio_solicitacao_realizacao(exames_do_mes) if exames_do_mes else 0

    return resultado


def concentracao_exames_por_paciente_ativo_mensal(
    exames: list[dict],
    tipo: str,
    data_inicio: str,
    data_fim: str,
    _grupos: dict[tuple[int, int], list[dict]] | None = None,
) -> dict:
    meses_alvo = _calcular_meses_alvo(data_inicio, data_fim)
    grupos = _grupos if _grupos is not None else _agrupar_exames_por_mes(exames, meses_alvo)

    resultado = {}
    for ano, mes in meses_alvo:
        chave = f"{mes:02d}/{ano}"
        exames_do_mes = grupos.get((ano, mes), [])
        resultado[chave] = (
            concentracao_exames_por_paciente_ativo(exames=exames_do_mes, tipo=tipo) if exames_do_mes else 0
        )

    return resultado


def dicionario_metricas_exames(exames, especialidade, data_inicio, data_fim):
    exames_filtrados = filtrar_eventos(evento="exame", dados=exames, especialidade=especialidade)
    meses_alvo = _calcular_meses_alvo(data_inicio=data_inicio, data_fim=data_fim)
    grupos = _agrupar_exames_por_mes(exames=exames_filtrados, meses_alvo=meses_alvo)
    contadores = _contadores_globais(exames=exames_filtrados)
    contadores_sem_filtro = _contadores_globais(exames=exames)
    return {
        "tempo_medio_solicitacao_realizacao_mensal": tempo_medio_solicitacao_realizacao_mensal(
            exames=exames, data_inicio=data_inicio, data_fim=data_fim, _grupos=grupos
        ),
        "distribuicao_exames_por_grupo_executor": distribuicao_exames_por_grupo_executor(
            exames=exames_filtrados
        ),
        "distribuicao_exames_por_grupo_executor_global": distribuicao_exames_por_grupo_executor(
            exames=exames
        ),
        "porcentagem_exames_regulados": _formatar_percentual(contadores["regulados"], contadores["total"]),
        "porcentagem_global_exames_regulados": _formatar_percentual(contadores_sem_filtro["regulados"], contadores_sem_filtro["total"]),
        "porcentagem_exames_concluidos": _formatar_percentual(contadores["concluidos"], contadores["total"]),
        "porcentagem_global_exames_concluidos": _formatar_percentual(contadores_sem_filtro["concluidos"], contadores_sem_filtro["total"]),
        "porcentagem_exames_cancelados": _formatar_percentual(contadores["cancelados"], contadores["total"]),
        "porcentagem_global_exames_cancelados": _formatar_percentual(contadores_sem_filtro["cancelados"], contadores_sem_filtro["total"])
    }

def metricas_exames(exames, especialidade, data_inicio, data_fim):
    metricas_key = dicionario_metricas_exames(exames, especialidade, data_inicio, data_fim)
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