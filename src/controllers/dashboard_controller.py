from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.interfaces.paciente_provider_interface import PacienteProviderInterface
from ..helpers.jornada_utils import calcular_diferenca_horas
from ..helpers.filtrar_eventos import filtrar_eventos
from ..helpers.total_pacientes_eventos import total_pacientes_eventos
from ..helpers.metricas_consultas import metricas_consultas_como_indicadores


class DashboardController:
    def __init__(
        self,
        consulta_provider: ConsultasCsvProvider,
        exame_provider: ExameCsvProvider,
        internacao_provider: InternacoesCsvProvider,
        paciente_provider: PacienteProviderInterface,
    ):
        self.consulta_provider = consulta_provider
        self.exame_provider = exame_provider
        self.internacao_provider = internacao_provider
        self.paciente_provider = paciente_provider

    async def get_dashboard(
        self,
        especialidade,
        data_inicio,
        data_fim,
    ):
        consultas    = await self.consulta_provider.listar_consultas()
        exames       = await self.exame_provider.listar_exames()
        internacoes  = await self.internacao_provider.listar_internacoes()
        pacientes    = await self.paciente_provider.listar_pacientes()

        #  filtros por especialidade 
        consultas_filtradas   = filtrar_eventos(evento='consulta',   dados=consultas,   especialidade=especialidade)
        exames_filtrados      = filtrar_eventos(evento='exame',      dados=exames,      especialidade=especialidade)
        internacoes_filtradas = filtrar_eventos(evento='internacao',  dados=internacoes, especialidade=especialidade)

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
        )
        total_consultas  = len(consultas_filtradas)
        total_exames     = len(exames_filtrados)
        total_internacoes = len(internacoes_filtradas)
        total_eventos    = total_consultas + total_exames + total_internacoes

        taxa_conclusao = (
            (len(consultas_concluidas) + len(exames_concluidos) + len(internacoes_concluidas))
            / (total_eventos or 1)
        )
        consultas_por_paciente = round(total_consultas / max(total_pacientes, 1), 2)

        # métricas de consultas calculadas
        indicadores_metricas = metricas_consultas_como_indicadores(consultas_filtradas)

        #proporção de exames regulados
        exames_regulados = [
            c 
            for c in exames_filtrados
            if c["condicao"].split()[0] == "Regulado"
        ]

        #tempo médio entre solicitação e realização de exames
        tempos = []
        for c in exames_filtrados:
            tempos.append(calcular_diferenca_horas(c["data_hora_solicitacao"], c["data_hora_realizacao"]))
        tempo_medio_solicitacao_realizacao = (
            sum(tempos)/len(tempos)
            if tempos else 0
        )
        tempo_medio_solicitacao_realizacao *= 60

        #proporção de exames pendentes
        exames_pendentes_proporcao = (len(exames_filtrados) - len(exames_concluidos))/len(exames_filtrados)

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
                "total_eventos": len(consultas_primeira_vez),
                "eventos": [
                    {"nome": "Pacientes cadastrados", "valor": total_pacientes},
                ],
                "indicadores": [
                    {"nome": "Pacientes novos", "valor": len(consultas_primeira_vez)},
                ],
            },

            "consultas": {
                "titulo":       "Consultas",
                "total_eventos": total_consultas,
                "eventos": [
                    {"nome": "Consultas", "valor": total_consultas},
                ],
                "indicadores": [
                    {"nome": "Consultas por paciente",  "valor": consultas_por_paciente},
                    {"nome": "Consultas concluídas",    "valor": len(consultas_concluidas)},
                    *indicadores_metricas,
                ],
            },

            "diagnostico": {
                "titulo":       "Diagnósticos",
                "total_eventos": len(consultas_com_diagnostico),
                "eventos": [
                    {"nome": "Diagnósticos registrados", "valor": len(consultas_com_diagnostico)},
                ],
                "indicadores": [
                    {"nome": "Proporção de exames regulados", "valor": len(exames_regulados)/len(exames_filtrados)},
                    {"nome": "Tempo médio solicitação -> realização", "valor": tempo_medio_solicitacao_realizacao},
                    {"nome": "Proporção de exames pendentes", "valor": exames_pendentes_proporcao},
                ],
            },

            "internacao": {
                "titulo":       "Internações",
                "total_eventos": total_internacoes,
                "eventos": [
                    {"nome": "Internações", "valor": total_internacoes},
                ],
                "indicadores": [
                    {"nome": "Tempo médio de permanência", "valor": tempo_medio_permanencia_internacao},
                ],
            },
        }

        return dashboard
