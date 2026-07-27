from collections import defaultdict
from ..helpers.math_utils import divisao_segura
from .helpers.filtrar_eventos import filtrar_eventos, filtrar_eventos_por_periodo
from ..helpers.formatacao import remover_acentos
_METRICAS_INDICADORES: list[tuple[str, str]] = [
    ("taxa_cirurgias_concluidas", "Porcentagem de cirurgias concluídas"),
    ("porcentagem_global_cirurgias_concluidas", "Porcentagem global de cirurgias concluidas"),
    ("tempo_medio_cirurgia_por_especialidade", "Tempo médio de cirurgia por especialidade"),
    ("pacientes_operados", "Pacientes únicos operados"),
    ("porcentagem_pacientes_operados", "Porcentagem de pacientes operados"),
    ("tempo_medio_cirurgia", "Tempo médio de cirurgia"),
    ("cirurgias_concluidas", "Número de cirurgias concluídas"),
    ("cirurgias_por_especialidade", "Cirurgias por especialidade"),
    ("porcentagem_cirurgias_origem_internacao", "Porcentagem de cirurgias que tiveram sua origem na internação"),
    ("porcentagem_cirurgias_por_origem", "Porcentagem de cirurgias por origem"),
    ("porcentagem_global_cirurgias_por_origem", "Porcentagem global de cirurgias por origem")
]
ORIGEM_INTERNACAO = "INTERNACAO"
ORIGEM_AMBULATORIO = "AMBULATORIO"

def filtrar_cirurgias(cirurgias, especialidade, data_inicio, data_fim):
    return filtrar_eventos_por_periodo(
        filtrar_eventos(evento="cirurgia", dados=cirurgias, especialidade=especialidade),
        data_inicio,
        data_fim,
    )


def cirurgias_concluidas(cirurgias):
    if len(cirurgias) == 0: return []
     
    cirurgias_concluidas = [
        c for c in cirurgias
        if c["situacao"] == 'RZDA'
    ]
    return cirurgias_concluidas

def taxa_cirurgias_concluidas(cirurgias):
    c_concluidas = cirurgias_concluidas(cirurgias=cirurgias)
    taxa = round(divisao_segura(len(c_concluidas), len(cirurgias))*100, 1)
    return taxa

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
    media = round(divisao_segura(sum(tempos), len(tempos)), 1)
    return media


def porcentagem_pacientes_operados(cirurgias, total_pacientes):
    if total_pacientes == 0:
        return 0

    proporcao = round(divisao_segura(pacientes_operados(cirurgias), total_pacientes)*100, 1)
    return proporcao



def tempo_medio_cirurgia_por_especialidade(cirurgias):
    cirurgias_por_especialidade = defaultdict(list)

    for cirurgia in cirurgias:
        if str(cirurgia["cancelada"]).upper() == "S":
            continue

        especialidade = cirurgia.get("especialidade")

        if especialidade:
            cirurgias_por_especialidade[especialidade].append(cirurgia)

    medias = {}

    for especialidade, cirurgias_esp in cirurgias_por_especialidade.items():
        medias[especialidade] = tempo_medio_cirurgia(cirurgias_esp)

    return dict(
        sorted(
            medias.items(),
            key=lambda item: item[1],
            reverse=True
        )[:5]
    )

def porcentagem_cirurgias_por_origem(cirurgias):
    """Retorna {"INTERNACAO": "valor%", "AMBULATORIO": "valor%"} com a
    porcentagem de cirurgias por origem, padronizando o campo via
    remover_acentos para lidar com INTERNAÇÃO/AMBULATÓRIO."""
    total = len(cirurgias)
    contagem_por_origem = defaultdict(int)

    for c in cirurgias:
        origem = remover_acentos(c["origem"]).upper()
        contagem_por_origem[origem] += 1

    def _pct(origem):
        return round((contagem_por_origem.get(origem, 0) / total) * 100, 2) if total else 0

    return {
        ORIGEM_INTERNACAO: f"{_pct(ORIGEM_INTERNACAO)}%",
        ORIGEM_AMBULATORIO: f"{_pct(ORIGEM_AMBULATORIO)}%",
    }

def porcentagem_cirurgias_origem_internacao(cirurgias):
    total_cirurgias = len(cirurgias)

    if total_cirurgias == 0:
        return 0

    cirurgias_internacao = sum(
        1
        for cirurgia in cirurgias
        if ORIGEM_INTERNACAO in cirurgia["origem"] 
    )
    taxa = round((divisao_segura(cirurgias_internacao, total_cirurgias))*100, 1)
    return f"{taxa}%"

def cirurgias_por_especialidade(cirurgias):
    resultado = defaultdict(int)

    for c in cirurgias:
        if str(c["cancelada"]).upper() == "S":
            continue

        especialidade = c.get("especialidade")

        if especialidade:
            resultado[especialidade] += 1

    total = sum(resultado.values())

    if total == 0:
        return {}

    return dict(
        (
            especialidade,
            f"{round((quantidade / total) * 100, 2)}%"
        )
        for especialidade, quantidade in sorted(
            resultado.items(),
            key=lambda item: item[1],
            reverse=True
        )[:5]
    )

def dicionario_metricas_cirurgias(cirurgias, especialidade, data_inicio, data_fim, numero_pacientes):
    cirurgias_filtradas = filtrar_cirurgias(cirurgias, especialidade, data_inicio, data_fim)
    return {
        "taxa_cirurgias_concluidas": taxa_cirurgias_concluidas(cirurgias=cirurgias),
        "porcentagem_cirurgias_concluidas": taxa_cirurgias_concluidas(cirurgias=cirurgias_filtradas),
        "porcentagem_global_cirurgias_concluidas": taxa_cirurgias_concluidas(cirurgias=cirurgias),
        "tempo_medio_cirurgia_por_especialidade": tempo_medio_cirurgia_por_especialidade(cirurgias=cirurgias),
        "tempo_medio_cirurgia": tempo_medio_cirurgia(cirurgias=cirurgias_filtradas),
        "cirurgias_concluidas": len(cirurgias_concluidas(cirurgias=cirurgias)),
        "cirurgias_por_especialidade": cirurgias_por_especialidade(cirurgias=cirurgias),
        "porcentagem_cirurgias_origem_internacao": porcentagem_cirurgias_origem_internacao(cirurgias=cirurgias),
        "porcentagem_cirurgias_por_origem": porcentagem_cirurgias_por_origem(cirurgias=cirurgias_filtradas),
        "porcentagem_global_cirurgias_por_origem": porcentagem_cirurgias_por_origem(cirurgias=cirurgias)
    }
    
def metricas_cirurgias(cirurgias, especialidade, data_inicio, data_fim, total_pacientes):
    
    metricas_key = dicionario_metricas_cirurgias(
        cirurgias=cirurgias,
        numero_pacientes=total_pacientes,
        especialidade=especialidade,
        data_inicio=data_inicio,
        data_fim=data_fim
    )
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