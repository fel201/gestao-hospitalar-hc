import asyncio

from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.implementations.cirurgias_csv_provider import CirurgiasCsvProvider
from ..providers.implementations.paciente_csv_provider import PacienteCsvProvider
from ..metrics.eventos_gerais import calcular_kpis_e_eventos
from ..metrics.helpers.filtrar_eventos import filtrar_eventos
from ..metrics.metricas_consultas import metricas_consultas_como_indicadores
from ..metrics.metricas_cirurgias import metricas_cirurgias, filtrar_cirurgias
from ..metrics.metricas_exames import metricas_exames
from ..metrics.metricas_entradas import metricas_entradas
from ..metrics.metricas_internacoes import metricas_internacoes
from ..providers.interfaces.metrica_provider_interface import MetricaProviderInterface


class DashboardController:
    def __init__(
        self,
        consulta_provider: ConsultasCsvProvider,
        exame_provider: ExameCsvProvider,
        internacao_provider: InternacoesCsvProvider,
        cirurgia_provider: CirurgiasCsvProvider,
        paciente_provider: PacienteCsvProvider,
        metrica_provider: MetricaProviderInterface,
    ):
        self.consulta_provider = consulta_provider
        self.exame_provider = exame_provider
        self.internacao_provider = internacao_provider
        self.cirurgia_provider = cirurgia_provider
        self.paciente_provider = paciente_provider
        self.metrica_provider = metrica_provider

    async def get_dashboard(self, especialidade, data_inicio, data_fim):
        cache = await self.metrica_provider.buscar_snapshot(especialidade, data_inicio, data_fim)
        if cache is not None:
            return cache

        consultas, exames, internacoes, cirurgias, pacientes = await asyncio.gather(
            self.consulta_provider.listar_consultas(data_inicio, data_fim),
            self.exame_provider.listar_exames(data_inicio, data_fim),
            self.internacao_provider.listar_internacoes(data_inicio, data_fim),
            self.cirurgia_provider.listar_cirurgias(data_inicio, data_fim),
            self.paciente_provider.listar_pacientes(),
        )

        # filtrando aqui para calcular os dados quantitativos de eventos
        consultas_filtradas = filtrar_eventos(evento="consulta", dados=consultas, especialidade=especialidade)
        exames_filtrados = filtrar_eventos(evento="exame", dados=exames, especialidade=especialidade)
        internacoes_filtradas = filtrar_eventos(evento="internacao", dados=internacoes, especialidade=especialidade)
        cirurgias_filtradas = filtrar_eventos(evento="cirurgia", dados=cirurgias, especialidade=especialidade)

        # todo o cálculo de kpis + eventos agora centralizado em eventos_gerais.py
        gerais = calcular_kpis_e_eventos(
            consultas=consultas_filtradas,
            exames=exames_filtrados,
            internacoes=internacoes_filtradas,
            cirurgias=cirurgias_filtradas,
        )
        kpis = gerais["kpis"]
        eventos = gerais["eventos_por_secao"]
        totais = gerais["totais"]

        # indicadores continuam calculados aqui (ou podem migrar pra metrics/ futuramente)
        m_entradas = metricas_entradas(
            consultas=consultas, exames=exames, internacoes=internacoes,
            pacientes=pacientes, cirurgias=cirurgias
        )
        m_internacoes = metricas_internacoes(
            internacoes=internacoes, especialidade=especialidade,
            data_inicio=data_inicio, data_fim=data_fim,
        )
        indicadores_consultas = metricas_consultas_como_indicadores(
            consultas=consultas, pacientes=pacientes, especialidade=especialidade,
            data_inicio=data_inicio, data_fim=data_fim,
        )
        indicadores_cirurgias = metricas_cirurgias(
            cirurgias=cirurgias, data_inicio=data_inicio, data_fim=data_fim,
            total_pacientes=totais["total_pacientes"], especialidade=especialidade,
        )
        m_exames = metricas_exames(exames, especialidade, data_inicio=data_inicio, data_fim=data_fim)

        dashboard = {
            "especialidade": especialidade,
            "kpis": kpis,
            "entrada": {
                "titulo": "Entrada",
                "total_eventos": totais["total_pacientes"],
                "eventos": eventos["entrada"],
                "indicadores": m_entradas,
            },
            "consultas": {
                "titulo": "Consultas",
                "total_eventos": totais["total_consultas"],
                "eventos": eventos["consultas"],
                "indicadores": [*indicadores_consultas],
            },
            "exames": {
                "titulo": "Exames",
                "total_eventos": totais["total_exames"],
                "eventos": eventos["exames"],
                "indicadores": m_exames,
            },
            "internacao": {
                "titulo": "Internações",
                "total_eventos": totais["total_internacoes"],
                "eventos": eventos["internacao"],
                "indicadores": m_internacoes,
            },
            "cirurgias": {
                "titulo": "Cirurgias",
                "total_eventos": totais["total_cirurgias"],
                "eventos": eventos["cirurgias"],
                "indicadores": indicadores_cirurgias,
            },
        }

        try:
            await self.metrica_provider.salvar_snapshot(
                especialidade=especialidade,
                data_inicio=data_inicio,
                data_fim=data_fim,
                dashboard=dashboard,
            )
        except Exception as e:
            print(f"Falha ao salvar snapshot de métricas: {e}")

        return dashboard