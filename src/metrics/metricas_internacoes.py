from collections import defaultdict
SUMARIO_ALTA_INFORMATIZADO = "INFORMATIZADO"

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

def porcentagem_sumario_altas_informatizados(internacoes):
    concluidas = internacoes_concluidas(internacoes)
    informatizados = 0
    for c in concluidas:
        if SUMARIO_ALTA_INFORMATIZADO in c["situacao_sumario_alta"]:
            informatizados += 1
    porcentagem = round((informatizados/len(concluidas))*100, 2)
    print(porcentagem)
    return porcentagem
    
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
    print(tempo_medio_por_especialidade)
    return tempo_medio_por_especialidade


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
    porcentagens = []

    for especialidade, pacientes in pacientes_por_especialidade.items():
        porcentagem = len(pacientes) / total * 100

        porcentagens.append({
            "especialidade": especialidade,
            "porcentagem": porcentagem
        })
    
    top5 = sorted(
        porcentagens,
        key=lambda x: x["porcentagem"],
        reverse=True
    )[:5]
    print(top5)    

