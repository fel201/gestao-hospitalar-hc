from typing import Any, Dict, List

from .helpers.total_pacientes_eventos import total_pacientes_eventos
from ..metrics.metricas_consultas import eventos_consultas
from ..helpers.filtrar_eventos import filtrar_eventos
from ..helpers.math_utils import divisao_segura
        # consultas = filtrar_consultas(consultas, especialidade, data_inicio=None, data_fim=None)
        # exames = filtrar_exames(exames, especialidade, data_inicio=None, data_fim=None)
        # internacoes = filtrar_internacoes(internacoes, especialidade, data_inicio=None, data_fim=None)
        # cirurgias = filtrar_cirurgias(cirurgias, especialidade, data_inicio=None, data_fim=None)

def calcular_kpis_e_eventos(
    consultas: List[Dict[str, Any]],
    exames: List[Dict[str, Any]],
    internacoes: List[Dict[str, Any]],
    cirurgias: List[Dict[str, Any]],
) -> Dict[str, Any]:
    
    exames_concluidos = sum(1 for c in exames if "liberado" in c["situacao"].lower())
    internacoes_concluidas = sum(1 for i in internacoes if i["ind_saida_pac"] == 'S')
    consultas_concluidas = sum(1 for c in consultas if "PACIENTE ATENDIDO" in c["retorno"])
    cirurgias_concluidas = sum(1 for c in cirurgias if c["situacao"] == 'RZDA')
    

    total_pacientes = total_pacientes_eventos(
        consultas=consultas, exames=exames,
        internacoes=internacoes, cirurgias=cirurgias
    )

    total_cirurgias = len(cirurgias)
    total_consultas = len(consultas)
    total_exames = len(exames)
    total_internacoes = len(internacoes)
    total_eventos_concluidos = cirurgias_concluidas + consultas_concluidas + internacoes_concluidas + exames_concluidos
    
    total_eventos = total_consultas + total_exames + total_internacoes + total_cirurgias 
    
    taxa_conclusao = divisao_segura(total_eventos_concluidos, total_eventos)
    
    print(taxa_conclusao)
    kpis = {
        "total_pacientes": total_pacientes,
        "total_eventos": total_eventos,
        "taxa_conclusao": taxa_conclusao
    }

    eventos_por_secao = {
        "consultas": eventos_consultas(consultas=consultas),
        "exames": [
            {"nome": "Exames concluídos", "valor": exames_concluidos},
        ],
        "internacao": [
            {"nome": "Internações concluidas", "valor": internacoes_concluidas},
        ],
        "cirurgias": [
            {"nome": "Cirurgias concluídas", "valor": cirurgias_concluidas},
        ],
    }

    totais = {
        "total_pacientes": total_pacientes,
        "total_consultas": total_consultas,
        "total_exames": total_exames,
        "total_internacoes": total_internacoes,
        "total_cirurgias": total_cirurgias,
        "total_eventos": total_eventos,
    }

    return {
        "kpis": kpis,
        "eventos_por_secao": eventos_por_secao,
        "totais": totais,
    }