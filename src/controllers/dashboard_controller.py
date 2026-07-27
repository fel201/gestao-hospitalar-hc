import asyncio
from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.implementations.cirurgias_csv_provider import CirurgiasCsvProvider
from ..providers.implementations.paciente_csv_provider import PacienteCsvProvider
from ..helpers.total_pacientes_eventos import total_pacientes_eventos
from ..metrics.metricas_consultas import metricas_consultas_como_indicadores, eventos_consultas, filtrar_consultas
from ..metrics.metricas_cirurgias import metricas_cirurgias, filtrar_cirurgias
from ..metrics.metricas_exames import metricas_exames, filtrar_exames
from ..metrics.metricas_entradas import metricas_entradas
from ..metrics.metricas_internacoes import metricas_internacoes, filtrar_internacoes
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

    async def get_dashboard(self, especialidade, data_inicio, data_fim):
        consultas, exames, internacoes, cirurgias, pacientes = await asyncio.gather(
            self.consulta_provider.listar_consultas(),
            self.exame_provider.listar_exames(),
            self.internacao_provider.listar_internacoes(),
            self.cirurgia_provider.listar_cirurgias(),
            self.paciente_provider.listar_pacientes(),
        )

        # filtragem aqui é só para os totais/eventos exibidos no dashboard,
        # não para decidir o que cada métrica usa — isso agora é responsabilidade
        # de cada dicionario_metricas_X
        consultas_filtradas = filtrar_consultas(consultas, especialidade, data_inicio, data_fim)
        exames_filtrados = filtrar_exames(exames, especialidade, data_inicio, data_fim)
        internacoes_filtradas = filtrar_internacoes(internacoes, especialidade, data_inicio, data_fim)
        cirurgias_filtradas = filtrar_cirurgias(cirurgias, especialidade, data_inicio, data_fim)

        exames_concluidos = [c for c in exames_filtrados if "liberado" in c["situacao"].lower()]
        internacoes_concluidas = [i for i in internacoes_filtradas if i["ind_saida_pac"] == 'S']

        tempo_medio_permanencia_internacao = 0
        if internacoes_concluidas:
            tempo_medio_permanencia_internacao = round(
                sum(int(i["tempo_permanencia_dias"]) for i in internacoes_concluidas)
                / len(internacoes_concluidas)
            )

        total_pacientes = total_pacientes_eventos(
            consultas=consultas_filtradas, exames=exames_filtrados,
            internacoes=internacoes_filtradas, cirurgias=cirurgias_filtradas
        )

        total_cirurgias = len(cirurgias_filtradas)
        total_consultas = len(consultas_filtradas)
        total_exames = len(exames_filtrados)
        total_internacoes = len(internacoes_filtradas)
        total_eventos = total_consultas + total_exames + total_internacoes + total_cirurgias

        # metricas 
        m_entradas = metricas_entradas(
            consultas=consultas,
            exames=exames,
            internacoes=internacoes,
            pacientes=pacientes,
            cirurgias=cirurgias
        )
        m_internacoes = metricas_internacoes(
            internacoes=internacoes,
            especialidade=especialidade,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        indicadores_consultas = metricas_consultas_como_indicadores(
            consultas=consultas,
            pacientes=pacientes,
            especialidade=especialidade,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        ev_consultas = eventos_consultas(
            consultas=consultas_filtradas,
        )
        indicadores_cirurgias = metricas_cirurgias(
            cirurgias=cirurgias,
            data_inicio=data_inicio,
            data_fim=data_fim,
            total_pacientes=total_pacientes,
            especialidade=especialidade,
        )
        m_exames = metricas_exames(
            exames,
            especialidade,
            data_inicio,
            data_fim
        )

        dashboard = {
            "especialidade": especialidade,

            "kpis": {
                "total_pacientes": total_pacientes,
                "total_eventos": total_eventos,
                "tempo_medio_jornada": tempo_medio_permanencia_internacao,
            },

            "entrada": {
                "titulo": "Entrada",
                "total_eventos": total_pacientes,
                "eventos": [
                    {"nome": "Pacientes cadastrados", "valor": total_pacientes},
                ],
                "indicadores": m_entradas
            },

            "consultas": {
                "titulo": "Consultas",
                "total_eventos": total_consultas,
                "eventos": ev_consultas,
                "indicadores": [*indicadores_consultas],
            },

            "exames": {
                "titulo": "Exames",
                "total_eventos": total_exames,
                "eventos": [
                    {"nome": "Exames registrados", "valor": total_exames},
                    {"nome": "Exames concluídos", "valor": len(exames_concluidos)}
                ],
                "indicadores": m_exames,
            },

            "internacao": {
                "titulo": "Internações",
                "total_eventos": total_internacoes,
                "eventos": [
                    {"nome": "Internações registradas", "valor": total_internacoes},
                    {"nome": "Internações concluidas", "valor": len(internacoes_concluidas)}
                ],
                "indicadores": m_internacoes
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