from collections import defaultdict
from ..helpers.math_utils import divisao_segura
from .helpers.filtrar_eventos import filtrar_eventos, filtrar_eventos_por_periodo

_METRICAS_INDICADORES: list[tuple[str, str]] = [
    ("taxa_cirurgias_concluidas", "Taxa de cirurgias concluídas"),
    ("pacientes_operados", "Pacientes únicos operados"),
    ("proporcao_pacientes_operados", "Proporção de pacientes operados"),
    ("tempo_medio_cirurgia", "Tempo médio de cirurgia (min)"),
    ("cirurgias_concluidas", "Número de cirurgias concluídas"),
    ("cirurgias_por_especialidade", "Cirurgias por especialidade"),
    ("porcentagem_cirurgias_origem_internacao", "Porcentagem de cirurgias que tiveram sua origem na internação")
]
ORIGEM_INTERNACAO = "INTERNAÇÃO"


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
    taxa = divisao_segura(len(c_concluidas), len(cirurgias))
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
    media = round(divisao_segura(sum(tempos), len(tempos)), 2)
    return media


def proporcao_pacientes_operados(cirurgias, total_pacientes):
    if total_pacientes == 0:
        return 0

    proporcao = round(divisao_segura(pacientes_operados(cirurgias), total_pacientes), 4)
    return proporcao

def porcentagem_cirurgias_origem_internacao(cirurgias):
    total_cirurgias = len(cirurgias)

    if total_cirurgias == 0:
        return 0

    cirurgias_internacao = sum(
        1
        for cirurgia in cirurgias
        if ORIGEM_INTERNACAO in cirurgia["origem"] 
    )
    taxa = round((divisao_segura(cirurgias_internacao, total_cirurgias))*100, 2)
    return f"{taxa}%"

def cirurgias_por_especialidade(cirurgias):
    resultado = defaultdict(int)

    for c in cirurgias:
        if str(c["cancelada"]).upper() == "S":
            continue

        resultado[c["especialidade"]] += 1
    return dict(resultado)

def dicionario_metricas_cirurgias(cirurgias, numero_pacientes):
    return {
        "taxa_cirurgias_concluidas": taxa_cirurgias_concluidas(cirurgias=cirurgias),
        "pacientes_operados": pacientes_operados(cirurgias=cirurgias),
        "proporcao_pacientes_operados": proporcao_pacientes_operados(cirurgias=cirurgias, total_pacientes=numero_pacientes),
        "tempo_medio_cirurgia": tempo_medio_cirurgia(cirurgias=cirurgias),
        "cirurgias_concluidas": len(cirurgias_concluidas(cirurgias=cirurgias)),
        "cirurgias_por_especialidade": cirurgias_por_especialidade(cirurgias=cirurgias),
        "porcentagem_cirurgias_origem_internacao": porcentagem_cirurgias_origem_internacao(cirurgias=cirurgias)
    }
    
def metricas_cirurgias(cirurgias, especialidade, data_inicio, data_fim, total_pacientes):
    cirurgias_filtradas = filtrar_cirurgias(cirurgias, especialidade, data_inicio, data_fim)
    metricas_key = dicionario_metricas_cirurgias(cirurgias=cirurgias_filtradas, numero_pacientes=total_pacientes)
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