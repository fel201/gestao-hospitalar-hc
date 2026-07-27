from collections import defaultdict
from .helpers.filtrar_eventos import filtrar_eventos, filtrar_eventos_por_periodo
SUMARIO_ALTA_INFORMATIZADO = "INFORMATIZADO"
from .metricas_consultas import _parse_dt
from datetime import datetime

_METRICAS_INDICADORES: list[tuple[str, str]] = [
    (
        "tempo_medio_permanencia_internacao",
        "Tempo médio de permanência da internação",
    ),
    (
        "porcentagem_sumario_altas_informatizados_mes",
        "Porcentagem de sumários de alta informatizados",
    ),
    (
        "porcentagem_global_sumario_altas_informatizados_mes",
        "Porcentagem global de sumários de alta informatizados",
    ),
    (
        "tempo_medio_permanencia_por_especialidade",
        "Tempo médio de permanência por especialidade",
    ),
    (
        "porcentagem_pacientes_internados_especialidade_clinica",
        "Porcentagem de registros de pacientes internados por especialidade clínica"
    )
]


def filtrar_internacoes(internacoes, especialidade, data_inicio, data_fim):
    return filtrar_eventos_por_periodo(
        filtrar_eventos(evento="internacao", dados=internacoes, especialidade=especialidade),
        data_inicio,
        data_fim,
    )


def internacoes_concluidas(internacoes):
    i_concluidas = [
        i for i in internacoes
        if i["ind_saida_pac"] == 'S'
    ]
    return i_concluidas

def tempo_medio_permanencia_internacao(internacoes):
    concluidas = internacoes_concluidas(internacoes=internacoes)
    tempo_medio = 0
    if concluidas:
        tempo_medio = round(
            sum(int(i["tempo_permanencia_dias"]) for i in concluidas)
            / len(concluidas)
        )    
    return tempo_medio


def _parse_data_limite(data):
    """Faz o parse de data_inicio/data_fim, que chegam no formato 'YYYY-MM-DD'.
    Aceita também objetos datetime/date, retornando-os diretamente."""
    if isinstance(data, str):
        return datetime.strptime(data, "%Y-%m-%d")
    return data


def _gerar_meses_periodo(data_inicio, data_fim):
    """Gera a lista de (mes, ano) dos últimos 5 meses contando com data_fim,
    em ordem decrescente (mais recente primeiro). Caso o intervalo entre
    data_inicio e data_fim seja menor que 5 meses, a lista para em data_inicio."""
    fim = _parse_data_limite(data_fim)
    inicio = _parse_data_limite(data_inicio)

    meses = []
    mes_atual, ano_atual = fim.month, fim.year

    for _ in range(5):
        meses.append((mes_atual, ano_atual))

        if (ano_atual, mes_atual) == (inicio.year, inicio.month):
            break

        mes_atual -= 1
        if mes_atual == 0:
            mes_atual = 12
            ano_atual -= 1

    return meses


def porcentagem_global_sumario_altas_informatizados_mes(internacoes):
    concluidas = internacoes_concluidas(internacoes)
    informatizados = 0
    for c in concluidas:
        if SUMARIO_ALTA_INFORMATIZADO in c["situacao_sumario_alta"]:
            informatizados += 1
    porcentagem = round((informatizados/len(concluidas))*100, 2)
    return porcentagem


def porcentagem_sumario_altas_informatizados_mes(internacoes, data_inicio, data_fim):
    """Retorna um dicionário {"mes/ano": "valor%", ...} com a porcentagem de
    sumários de alta informatizados por mês, considerando os últimos 5 meses
    a partir de data_fim (ou os meses correspondentes, caso o período filtrado
    seja menor que 5 meses)."""
    concluidas = internacoes_concluidas(internacoes)

    meses_periodo = _gerar_meses_periodo(data_inicio, data_fim)
    meses_periodo_set = set(meses_periodo)

    informatizados_por_mes = defaultdict(int)
    total_por_mes = defaultdict(int)

    for c in concluidas:
        dt = datetime.strptime(c["data_hora_realizacao"], "%d/%m/%Y, %H:%M")
        chave = (dt.month, dt.year)

        if chave in meses_periodo_set:
            total_por_mes[chave] += 1
            if SUMARIO_ALTA_INFORMATIZADO in c["situacao_sumario_alta"]:
                informatizados_por_mes[chave] += 1

    resultado = {}
    for mes, ano in meses_periodo:
        total = total_por_mes.get((mes, ano), 0)
        valor = (
            round((informatizados_por_mes.get((mes, ano), 0) / total) * 100, 2)
            if total
            else 0
        )
        resultado[f"{mes:02d}/{ano}"] = f"{valor}%"
    print(resultado)
    return resultado

def tempo_medio_permanencia_por_especialidade(internacoes):
    internacoes_por_especialidade = defaultdict(list)

    for internacao in internacoes:
        especialidade = internacao["especialidade"]

        if especialidade:
            internacoes_por_especialidade[especialidade].append(internacao)

    tempo_medio_por_especialidade = {}

    for especialidade, internacoes_esp in internacoes_por_especialidade.items():
        tempo_medio_por_especialidade[especialidade] = (
            tempo_medio_permanencia_internacao(internacoes_esp)
        )

    tempo_medio_por_especialidade = dict(
        sorted(
            tempo_medio_por_especialidade.items(),
            key=lambda item: item[1],
            reverse=True
        )[:5]
    )
    return tempo_medio_por_especialidade

from collections import defaultdict

# métrica geral
def porcentagem_pacientes_internados_especialidade_clinica(internacoes):
    pacientes_por_especialidade = defaultdict(set)

    for i in internacoes:
        especialidade = i["especialidade"]
        prontuario = i["prontuario"]

        if prontuario:
            pacientes_por_especialidade[especialidade].add(prontuario)

    todos_pacientes = set()

    for i in internacoes:
        if i["prontuario"]:
            todos_pacientes.add(i["prontuario"])

    total = len(todos_pacientes)
    porcentagens = {}

    for especialidade, pacientes in pacientes_por_especialidade.items():
        porcentagens[especialidade] = round((len(pacientes) / total) * 100, 2)

    top5 = dict(
        sorted(
            porcentagens.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
    )
    
    return top5
    
def dicionario_metricas_internacoes(internacoes, especialidade, data_inicio, data_fim):
    internacoes_filtradas = filtrar_internacoes(internacoes, especialidade, data_inicio, data_fim)
    return {
        "tempo_medio_permanencia_internacao": (
            tempo_medio_permanencia_internacao(
                internacoes=internacoes
            )
        ),
        "porcentagem_sumario_altas_informatizados_mes": (
            porcentagem_sumario_altas_informatizados_mes(
                internacoes=internacoes,
                data_inicio=data_inicio,
                data_fim=data_fim
            )
        ),
        "porcentagem_global_sumario_altas_informatizados_mes": (
            porcentagem_global_sumario_altas_informatizados_mes(
                internacoes=internacoes
            )
        ),
        "tempo_medio_permanencia_por_especialidade": (
            tempo_medio_permanencia_por_especialidade(
                internacoes=internacoes
            )
        ),
        "porcentagem_pacientes_internados_especialidade_clinica": (
            porcentagem_pacientes_internados_especialidade_clinica(
                internacoes=internacoes
            )
        )
    }

    
def metricas_internacoes(internacoes, especialidade, data_inicio, data_fim):
    
    metricas_key = dicionario_metricas_internacoes(
        internacoes=internacoes,
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