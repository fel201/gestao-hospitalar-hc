from typing import Dict, Any, List
from datetime import datetime
from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.interfaces.paciente_provider_interface import PacienteProviderInterface
from ..helpers.juntar_consultas import juntar_consultas
from ..helpers.juntar_exames import juntar_exames
from ..helpers.juntar_internacoes import juntar_internacoes
from ..helpers.normalize_id import _normalize_id


class JornadaController:
    # essa função remove tudo que não for número dos IDS 
    # para melhorar compatibilidade entre as tabelas
    async def obter_jornada_paciente(
        pac_id: int,
        paciente_provider: PacienteProviderInterface,
        consultas_provider: ConsultasCsvProvider,
        exames_provider: ExameCsvProvider,
        internacoes_provider: InternacoesCsvProvider,
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
                'numero_internacoes': numero_internacoes
            }
        }
