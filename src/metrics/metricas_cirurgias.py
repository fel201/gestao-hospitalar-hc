from collections import defaultdict
_METRICAS_INDICADORES: list[tuple[str, str]] = [
    ("taxa_cirurgias_concluidas", "Taxa de cirurgias concluídas"),
    ("pacientes_operados", "Pacientes únicos operados"),
    ("proporcao_pacientes_operados", "Proporção de pacientes operados"),
    ("tempo_medio_cirurgia", "Tempo médio de cirurgia (min)"),
    ("cirurgias_concluidas", "Número de cirurgias concluídas"),
    ("cirurgias_por_especialidade", "Cirurgias por especialidade")
]

def cirurgias_concluidas(cirurgias):
    if len(cirurgias) == 0: return
     
    cirurgias_concluidas = [
        c for c in cirurgias
        if c["situacao"] == 'RZDA'
    ]
    return cirurgias_concluidas

def taxa_cirurgias_concluidas(cirurgias):
    c_concluidas = cirurgias_concluidas(cirurgias=cirurgias)
    taxa = len(c_concluidas)/len(cirurgias)
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

    return round(sum(tempos) / len(tempos), 2)


def proporcao_pacientes_operados(cirurgias, total_pacientes):
    if total_pacientes == 0:
        return 0

    return round(
        pacientes_operados(cirurgias) / total_pacientes,
        4,
    )


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
        "cirurgias_por_especialidade": cirurgias_por_especialidade(cirurgias=cirurgias)
    }
    
def metricas_cirurgias(cirurgias, total_pacientes):
    metricas_key = dicionario_metricas_cirurgias(cirurgias=cirurgias, numero_pacientes=total_pacientes)
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