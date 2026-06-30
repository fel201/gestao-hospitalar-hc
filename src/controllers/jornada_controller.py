from typing import Dict, Any, List
from datetime import datetime
from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.interfaces.paciente_provider_interface import PacienteProviderInterface
from ..helpers.juntar_consultas import juntar_consultas
from ..helpers.juntar_exames import juntar_exames
from ..helpers.juntar_internacoes import juntar_internacoes
from ..helpers.jornada_utils import calculate_time_intervals, filter_by_specification
from ..helpers.normalize_id import _normalize_id
from datetime import datetime

class JornadaController:
    @staticmethod
    async def listar_pacientes_com_jornada(
        paciente_provider: PacienteProviderInterface,
        consultas_provider: ConsultasCsvProvider,
        exames_provider: ExameCsvProvider,
        internacoes_provider: InternacoesCsvProvider,
        page: int = 1,
        page_size: int = 50,
    ):  
        pacientes = await paciente_provider.listar_pacientes() 

        consultas = await consultas_provider.listar_consultas()
        exames = await exames_provider.listar_exames()
        internacoes = await internacoes_provider.listar_internacoes()

        ids_com_jornada = set()

        for consulta in consultas:
            ids_com_jornada.add(_normalize_id(consulta.get("prontuario")))

        for exame in exames:
            ids_com_jornada.add(_normalize_id(exame.get("paciente_prontuario")))

        for internacao in internacoes:
            ids_com_jornada.add(_normalize_id(internacao.get("prontuario")))

        pacientes_com_jornada = [
            paciente
            for paciente in pacientes
            if _normalize_id(paciente["prontuario"]) in ids_com_jornada
        ]

        total = len(pacientes_com_jornada)

        inicio = (page - 1) * page_size
        fim = inicio + page_size

        return {
            "items": pacientes_com_jornada[inicio:fim],
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
        }
        
    async def obter_jornada_paciente( 
        pac_id: int,
        paciente_provider: PacienteProviderInterface,
        consultas_provider: ConsultasCsvProvider,
        exames_provider: ExameCsvProvider,
        internacoes_provider: InternacoesCsvProvider,
        especificacao: List[str] = None,
    ) -> Dict[str, Any]:
        paciente = await paciente_provider.obter_paciente_por_codigo(pac_id)

        pac_id_normalized = _normalize_id(pac_id)
        eventos = []
        
        consultas_raw = await consultas_provider.listar_consultas()
        numero_consultas = juntar_consultas(eventos, consultas_raw, pac_id=pac_id_normalized)
        
        exames_raw = await exames_provider.listar_exames()
        numero_exames = juntar_exames(eventos, exames_raw, pac_id=pac_id_normalized)
        
        internacoes_raw = await internacoes_provider.listar_internacoes()
        numero_internacoes = juntar_internacoes(eventos, internacoes_raw, pac_id_normalized)
        # ordenando cronologicamente com base na data de inicio de cada evento
        
        eventos.sort(key=lambda evento: evento['data_evento'])
        eventos = filter_by_specification(eventos, especificacao)
        calculate_time_intervals(eventos)
        return {
            'paciente': {
                'pac_id': paciente.get('codigo'),
                'prontuario': paciente.get('prontuario'),
                'nome': paciente.get('nome'),
            },
            'eventos': eventos,
            'metricas': {
                'numero_eventos': len(eventos),
                'numero_consultas': numero_consultas,
                'numero_exames': numero_exames,
                'numero_internacoes': numero_internacoes,
                'numero_eventos_exibidos': len(eventos),
                'filtro_especificacao': especificacao or []
            }
        }