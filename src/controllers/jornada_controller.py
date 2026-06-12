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
    @staticmethod
    async def listar_pacientes_com_jornada(
        paciente_provider: PacienteProviderInterface,
        consultas_provider: ConsultasCsvProvider,
        exames_provider: ExameCsvProvider,
        internacoes_provider: InternacoesCsvProvider
    ):
        pacientes = await paciente_provider.listar_pacientes()

        consultas = await consultas_provider.listar_consultas()
        exames = await exames_provider.listar_exames()
        internacoes = await internacoes_provider.listar_internacoes()

        ids_com_jornada = set()
        for consulta in consultas:
            ids_com_jornada.add(
                _normalize_id(consulta.get("prontuario"))
            )

        for exame in exames:
            ids_com_jornada.add(
                _normalize_id(exame.get("paciente_prontuario"))
            )

        for internacao in internacoes:
            ids_com_jornada.add(
                _normalize_id(internacao.get("prontuario"))
            )

        resultado = [
            paciente
            for paciente in pacientes
            if _normalize_id(paciente["prontuario"]) in ids_com_jornada
        ]
        prontuarios_pacientes = {
            _normalize_id(p["prontuario"])
            for p in pacientes
            if p["prontuario"]
        }

        print("Prontuários pacientes:",
            len(prontuarios_pacientes))

        print("Prontuários jornada:",
            len(ids_com_jornada))

        print("Interseção:",
            len(prontuarios_pacientes & ids_com_jornada))
        return resultado
        
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
        print(eventos)
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

