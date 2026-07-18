import asyncio
from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.implementations.cirurgias_csv_provider import CirurgiasCsvProvider
from ..providers.implementations.paciente_csv_provider import PacienteCsvProvider
from ..helpers.jornada_utils import calcular_diferenca_horas
from ..helpers.filtrar_eventos import filtrar_eventos
from ..helpers.total_pacientes_eventos import total_pacientes_eventos
from ..metrics.metricas_entradas import tempo_medio_cadastro_evento, taxa_prontuarios_inertes
from ..metrics.metricas_consultas import metricas_consultas_como_indicadores
from ..metrics.metricas_cirurgias import metricas_cirurgias
from ..metrics.metricas_exames import tempo_medio_solicitacao_realizacao, proporcao_exames, exames_por_paciente

class DashboardController:
    def __init__(
        self,
        consulta_provider: ConsultasCsvProvider,
        exame_provider: ExameCsvProvider,
        internacao_provider: InternacoesCsvProvider,
        cirurgia_provider: CirurgiasCsvProvider,
        paciente_provider: PacienteCsvProvider
    ):
        self.consulta_provider = consulta_provider
        self.exame_provider = exame_provider
        self.internacao_provider = internacao_provider
        self.cirurgia_provider = cirurgia_provider
        self.paciente_provider = paciente_provider

    async def get_dashboard(
        self,
        especialidade,
        data_inicio,
        data_fim,
    ):
        consultas, exames, internacoes, cirurgias, pacientes = await asyncio.gather(
            self.consulta_provider.listar_consultas(),
            self.exame_provider.listar_exames(),
            self.internacao_provider.listar_internacoes(),
            self.cirurgia_provider.listar_cirurgias(),
            self.paciente_provider.listar_pacientes()
        )
        #  filtros por especialidade 
        consultas_filtradas   = filtrar_eventos(evento='consulta',   dados=consultas,   especialidade=especialidade)
        exames_filtrados      = filtrar_eventos(evento='exame',      dados=exames,      especialidade=especialidade)
        internacoes_filtradas = filtrar_eventos(evento='internacao',  dados=internacoes, especialidade=especialidade)
        cirurgias_filtradas =   filtrar_eventos(evento="cirurgia", dados=cirurgias, especialidade=especialidade,
)
        # consultas 
        consultas_primeira_vez = [
            c for c in consultas_filtradas
            if "PRIMEIRA CONSULTA" in c["condicao"]
        ]
        consultas_concluidas = [
            c for c in consultas_filtradas
            if "PACIENTE ATENDIDO" in c["retorno"]
        ]
        consultas_com_diagnostico = [
            c for c in consultas_concluidas
            if c["cid"] != ""
        ]

        # exames 
        exames_concluidos = [
            c for c in exames_filtrados
            if "liberado" in c["situacao"].lower()
        ]

        # internações
        internacoes_concluidas = [
            i for i in internacoes_filtradas
            if i["ind_saida_pac"] == 'S'
        ]

        tempo_medio_permanencia_internacao = 0
        if internacoes_concluidas:
            tempo_medio_permanencia_internacao = round(
                sum(int(i["tempo_permanencia_dias"]) for i in internacoes_concluidas)
                / len(internacoes_concluidas)
            )

        # totais e KPIs 
        total_pacientes  = total_pacientes_eventos(
            consultas=consultas_filtradas,
            exames=exames_filtrados,
            internacoes=internacoes_filtradas,
            cirurgias=cirurgias_filtradas
        )
        
        
        total_cirurgias = len(cirurgias_filtradas)
        total_consultas  = len(consultas_filtradas)
        total_exames     = len(exames_filtrados)
        total_internacoes = len(internacoes_filtradas)
        total_eventos    = total_consultas + total_exames + total_internacoes + total_cirurgias

        taxa_conclusao = (
            (len(consultas_concluidas) + len(exames_concluidos) + len(internacoes_concluidas))
            / (total_eventos or 1)
        )
        
        consultas_por_paciente = round(total_consultas / max(total_pacientes, 1), 2)
        # métricas de entrada
        
        tempo_medio_cad_evento = tempo_medio_cadastro_evento(
            consultas=consultas,
            exames=exames,
            internacoes=internacoes,
            pacientes=pacientes,
            cirurgias=cirurgias
        )
        taxa_prontuarios_ausentes = taxa_prontuarios_inertes(
            consultas=consultas,
            exames=exames,
            internacoes=internacoes,
            pacientes=pacientes,
            cirurgias=cirurgias
        )
        # métricas de consultas calculadas
        indicadores_consultas = metricas_consultas_como_indicadores(consultas_filtradas)
        indicadores_cirurgias = metricas_cirurgias(cirurgias_filtradas, total_pacientes)
        #proporção de exames regulados
        exames_regulados = [
            c 
            for c in exames_filtrados
            if c["condicao"].split()[0] == "Regulado"
        ]

        
        tempo_medio_soli_real = tempo_medio_solicitacao_realizacao(exames_filtrados) 
        
        proporcao_exames_ambulatoriais = \
            (proporcao_exames(exames=exames_filtrados, tipo="ambulatorial"))["proporcao_exames"]
            
        exames_amb_por_pacientes = \
            (exames_por_paciente(exames=exames_filtrados, tipo="ambulatorial"))["exames_por_pac"]
        
        exames_pendentes_proporcao = round((len(exames_filtrados) - len(exames_concluidos))/len(exames_filtrados), 2)
        proporcao_exames_regulados = len(exames_regulados)/len(exames_filtrados)
        
        # Dashboard 
        dashboard = {
            "especialidade": especialidade,

            "kpis": {
                "total_pacientes":    total_pacientes,
                "total_eventos":      total_eventos,
                "tempo_medio_jornada": tempo_medio_permanencia_internacao,
                "taxa_conclusao":     taxa_conclusao,
            },

            "entrada": {
                "titulo":       "Entrada",
                "total_eventos": total_pacientes,
                "eventos": [
                    {"nome": "Pacientes cadastrados", "valor": total_pacientes},
                ],
                "indicadores": [
                    tempo_medio_cad_evento,
                    taxa_prontuarios_ausentes
                ],
            },

            "consultas": {
                "titulo":       "Consultas",
                "total_eventos": total_consultas,
                "eventos": [
                    {"nome": "Consultas", "valor": total_consultas},
                    {"nome": "Primeiras consultas", "valor": len(consultas_primeira_vez)}
                ],
                "indicadores": [
                    {"nome": "Consultas por paciente",  "valor": consultas_por_paciente},
                    {"nome": "Consultas concluídas",    "valor": len(consultas_concluidas)},
                    *indicadores_consultas,
                ],
            },

            "exames": {
                "titulo":       "Exames",
                "total_eventos": total_exames,
                "eventos": [
                    {"nome": "Exames", "valor": total_exames},
                    {"nome": "Diagnósticos registrados", "valor": len(consultas_com_diagnostico)},
                ],
                "indicadores": [
                    {"nome": "Proporção de exames regulados", "valor": proporcao_exames_regulados},
                    {"nome": "Tempo médio de solicitação até realização", "valor": tempo_medio_soli_real},
                    {"nome": "Proporção de exames pendentes", "valor": exames_pendentes_proporcao},
                    {"nome": "Exames ambulatoriais por paciente", "valor": exames_amb_por_pacientes},
                    {"nome": "Proporção de exames ambulatoriais", "valor": proporcao_exames_ambulatoriais}
                ],
            },

            "internacao": {
                "titulo":       "Internações",
                "total_eventos": total_internacoes,
                "eventos": [
                    {"nome": "Internações", "valor": total_internacoes},
                ],
                "indicadores": [
                    {"nome": "Tempo médio de permanência (dias)", "valor": tempo_medio_permanencia_internacao},
                ],
            },
            "cirurgias": {
                "titulo": "Cirurgias",
                "total_eventos": total_cirurgias,
                "eventos": [
                    {
                        "nome": "Cirurgias",
                        "valor": total_cirurgias,
                    },
                ],
                "indicadores": indicadores_cirurgias,
            },
        }

        return dashboard
