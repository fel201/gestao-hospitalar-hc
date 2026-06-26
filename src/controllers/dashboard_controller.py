from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.interfaces.paciente_provider_interface import PacienteProviderInterface
from ..helpers.jornada_utils import calcular_diferenca_horas
from ..helpers.filtrar_eventos import filtrar_eventos
from ..helpers.total_pacientes_eventos import total_pacientes_eventos    
    
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
        print("numero de consultas: ", len(consultas))
        print("numero de exames: ", len(exames))
        print("numero de internacoes: ", len(internacoes))
        print("numero de pacientes: ", len(pacientes))
        consultas_filtradas = filtrar_eventos(evento='consulta', dados=consultas, especialidade=especialidade)
        
        consultas_primeira_vez = [
            c 
            for c in consultas_filtradas
            if "PRIMEIRA CONSULTA" in c["condicao"]
        ]
        
        consultas_concluidas = [
            c
            for c in consultas_filtradas
            if "PACIENTE ATENDIDO" in c["retorno"]
        ]
        
        consultas_com_diagnostico = [
            c 
            for c in consultas_concluidas
            if c["cid"] != ""
        ]
        for c in consultas_concluidas:
            if c["cid"] != "":
                print(c["cid"])
                
        print(len(consultas_primeira_vez))
        print(len(consultas_concluidas))
        print(len(consultas_com_diagnostico))
        exames_filtrados = filtrar_eventos(evento='exame', dados=exames, especialidade=especialidade)

        exames_concluidos = [
            c 
            for c in exames_filtrados
            if "liberado" in c["situacao"].lower() 
        ]
        
        internacoes_filtradas = filtrar_eventos(evento='internacao', dados=internacoes, especialidade=especialidade)
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

        total_pacientes = total_pacientes_eventos(consultas=consultas_filtradas,
                                                  exames=exames_filtrados,
                                                  internacoes=internacoes_filtradas)
        
        taxa_conclusao = \
        (len(consultas_concluidas) + len(exames_concluidos) + len(internacoes_concluidas))\
        /(len(consultas_filtradas) + len(exames_filtrados) + len(internacoes_filtradas))
        
        total_consultas = len(consultas_filtradas)
        total_exames = len(exames_filtrados)
        total_internacoes = len(internacoes_filtradas)
        total_eventos = total_consultas + total_exames + total_internacoes
        
        consultas_por_paciente = round(len(consultas_filtradas)/max(total_pacientes, 1), 2)
        dashboard = {
            "especialidade": especialidade,

            "kpis": {
                "total_pacientes": total_pacientes,
                "total_eventos": total_eventos,
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
                            "valor": total_consultas
                        }
                    ],

                    "indicadores": [
                        {
                            "nome":
                                "Consultas por paciente",
                            "valor": consultas_por_paciente
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