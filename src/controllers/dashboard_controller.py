from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.interfaces.paciente_provider_interface import PacienteProviderInterface
from ..helpers.jornada_utils import calcular_diferenca_horas

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
        data_fim
    ):

        consultas = await self.consulta_provider.listar_consultas()
        exames = await self.exame_provider.listar_exames()
        internacoes = await self.internacao_provider.listar_internacoes()
        pacientes = await self.paciente_provider.listar_pacientes()
        for c in consultas:
            print(c["especialidade"])
        
        consultas_filtradas = [
            c
            for c in consultas
            if especialidade.lower() in c["especialidade"].lower()
        ]
        print(len(consultas_filtradas))        
        consultas_primeira_vez = [
            c 
            for c in consultas_filtradas
            if "PRIMEIRA VEZ" in c["condicao"].lower()
        ]
        
        consultas_conluidas = [
            c
            for c in consultas_filtradas
            if "PACIENTE ATENDIDO" in c["retorno"].lower()
        ]

        consultas_com_diagnostico = [
            c 
            for c in consultas_conluidas
            if c["cid"] != ""
        ]

        exames_filtrados = [
            c
            for c in exames
            if especialidade.lower() in c["especialidade_solicitante_nome"].lower() 
        ]

        exames_concluidos = [
            c 
            for c in exames_filtrados
            if "liberado" in c["situacao"].lower() 
        ]

        internacoes_filtradas = [
            i
            for i in internacoes
            if especialidade.lower() in i["especialidade"].lower()
        ]
        
        internacoes_concluidas = [
            i 
            for i in internacoes_filtradas
            if i["ind_saida_pac"] == 'S'
        ]

        tempo_medio_permanencia_internacao = 0

        for i in internacoes_concluidas:
            tempo_medio_permanencia_internacao += int(i["tempo_permanencia_dias"])
            
        if len(internacoes_concluidas) != 0:
            tempo_medio_permanencia_internacao = round(tempo_medio_permanencia_internacao/len(internacoes_concluidas))

        pacientes_unicos = set()
        for consulta in consultas_filtradas:
            pacientes_unicos.add(
                consulta["paciente_id"]
            )

        total_pacientes = len(
            pacientes_unicos
        )
        print(total_pacientes)
        taxa_conclusao = \
        (len(consultas_conluidas) + len(exames_concluidos) + len(internacoes_concluidas))\
        /(len(consultas_filtradas) + len(exames_filtrados) + len(internacoes_filtradas))
        dashboard = {
            "especialidade": especialidade,

            "kpis": {
                "total_pacientes": total_pacientes,

                "total_eventos":
                    len(consultas_filtradas)
                    + len(exames)
                    + len(internacoes_filtradas),

                # dados placeholders, pq eu ainda não calculei essas taxas
                "tempo_medio_jornada": tempo_medio_permanencia_internacao,
                "taxa_conclusao": taxa_conclusao
            },

            "etapas": [
                {
                    "id": "entrada",
                    "titulo": "Entrada",
                    "total_eventos": len(consultas_primeira_vez),

                    "eventos": [
                        {
                            "nome": "Pacientes cadastrados",
                            "valor": total_pacientes
                        }
                    ],

                    "indicadores": [
                        {
                            "nome": "Pacientes novos",
                            "valor": len(consultas_primeira_vez)
                        }
                    ]
                },

                {
                    "id": "consultas",
                    "titulo": "Consultas",
                    "total_eventos": len(
                        consultas_filtradas
                    ),

                    "eventos": [
                        {
                            "nome": "Consultas",
                            "valor": len(
                                consultas_filtradas
                            )
                        }
                    ],

                    "indicadores": [
                        {
                            "nome":
                                "Consultas por paciente",

                            "valor":
                                round(
                                    len(
                                        consultas_filtradas
                                    )
                                    /
                                    max(
                                        total_pacientes,
                                        1
                                    ),
                                    2
                                )
                        }
                    ]
                },

                {
                    "id": "diagnostico",
                    "titulo": "Diagnóstico",
                    "total_eventos": len(consultas_com_diagnostico),

                    "eventos": [

                    ]
                },

                {
                    "id": "internacao",
                    "titulo": "Internação"
                }
            ]
        }

        return dashboard