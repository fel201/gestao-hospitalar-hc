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
from ..metrics.metricas_consultas import metricas_consultas_como_indicadores, eventos_consultas
from ..metrics.metricas_cirurgias import metricas_cirurgias
from ..metrics.metricas_exames import metricas_exames
from ..metrics.metricas_internacoes import tempo_medio_permanencia_por_especialidade
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

        # consultas_com_diagnostico = [
        #     c for c in consultas_concluidas
        #     if c["cid"] != ""
        # ]

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
        taxa_conclusao_exames = len(exames_concluidos)/len(exames_filtrados)
        taxa_conclusao_internacoes = len(internacoes_concluidas)/len(internacoes_filtradas)
        # taxa_conclusao = 
        #     (len(consultas_concluidas) + len(exames_concluidos) + len(internacoes_concluidas)
        #     / (total_eventos or 1)
        # )
        
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
        # métricas e eventos de consultas calculados
        indicadores_consultas = metricas_consultas_como_indicadores(consultas_filtradas, pacientes=pacientes)
        ev_consultas = eventos_consultas(consultas=consultas_filtradas)
        indicadores_cirurgias = metricas_cirurgias(cirurgias_filtradas, total_pacientes)
        #proporção de exames regulados

        m_exames = metricas_exames(exames=exames)        
        
        exames_pendentes_proporcao = round((len(exames_filtrados) - len(exames_concluidos))/len(exames_filtrados), 2)
        
        # Dashboard 
        dashboard = {
            "especialidade": especialidade,

            "kpis": {
                "total_pacientes":    total_pacientes,
                "total_eventos":      total_eventos,
                "tempo_medio_jornada": tempo_medio_permanencia_internacao,
                # "taxa_conclusao":     taxa_conclusao,
            },

            "entrada": {
                "titulo":       "Entrada",
                "total_eventos": total_pacientes,
                "eventos": [
                    {"nome": "Pacientes cadastrados", "valor": total_pacientes},
                ],
                "indicadores": [
                    tempo_medio_cad_evento,
                    taxa_prontuarios_ausentes,
                ],
            },

            "consultas": {
                "titulo":       "Consultas",
                "total_eventos": total_consultas,
                "eventos": ev_consultas,
                "indicadores": [*indicadores_consultas],
            },

            "exames": {
                "titulo":       "Exames",
                "total_eventos": total_exames,
                "eventos": [
                    {"nome": "Exames registrados", "valor": total_exames},
                    {"nome": "Exames concluídos", "valor": len(exames_concluidos)}
                ],
                "indicadores": m_exames
                    # {"nome": "Proporção de exames pendentes", "valor": exames_pendentes_proporcao}
            },

            "internacao": {
                "titulo":       "Internações",
                "total_eventos": total_internacoes,
                "eventos": [
                    {"nome": "Internações registradas", "valor": total_internacoes},
                    {"nome": "Internações concluidas", "valor": len(internacoes_concluidas)}
                ],
                "indicadores": [
                    {"nome": "Tempo médio de permanência (dias)", "valor": tempo_medio_permanencia_internacao},
                                
                ],
            },
            "cirurgias": {
                "titulo": "Cirurgias",
                "total_eventos": total_cirurgias,
                "eventos": [
                    {"nome": "Cirurgias registradas", "valor": total_cirurgias},
                ],
                "indicadores": indicadores_cirurgias
            },
        }

        return dashboard
