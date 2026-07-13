from ..helpers.jornada_utils import calcular_diferenca_horas
def tempo_medio_solicitacao_realizacao(exames: list[dict, any]) -> dict:
    if len(exames) == 0: return {"tempo_medio_solic_realiz": 0}
    
    tempos = []
    for c in exames:
        tempos.append(calcular_diferenca_horas(c["data_hora_solicitacao"], c["data_hora_realizacao"]))
        tempo_medio_solicitacao_realizacao = (
            sum(tempos)/len(tempos)
            if tempos else 0
        )
        tempo_medio_solicitacao_realizacao *= 60 
        tempo_medio_solicitacao_realizacao = round(tempo_medio_solicitacao_realizacao, 2)
    
    return tempo_medio_solicitacao_realizacao