from typing import Dict, Any, List
from datetime import datetime
from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.interfaces.paciente_provider_interface import PacienteProviderInterface
from ..helpers.juntar_consultas import juntar_consultas
from ..helpers.juntar_exames import juntar_exames
from ..helpers.juntar_internacoes import juntar_internacoes
from ..helpers.jornada_utils import calculate_time_intervals
from ..helpers.normalize_id import _normalize_id
from datetime import datetime

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
        
    async def obter_jornada_paciente( # melhor id para teste: 2000127
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

        # cálculo de intervalo e flags do gargalo
        for i, evento_atual in enumerate(eventos):
            evento_atual = eventos[i]
            
            # Padroniza a data do evento atual para objeto datetime
            data_str = evento_atual.get('data_evento', '')
            try:
                dt_atual = datetime.strptime(data_str, "%d/%m/%Y") if isinstance(data_str, str) else data_str
            except ValueError:
                dt_atual = datetime.now() # Fallback seguro
                evento_atual['data_evento'] = dt_atual

            # Se for o primeiro evento, não tem intervalo anterior
            if i == 0:
                evento_atual['dias_desde_ultimo_evento'] = 0
                evento_atual['is_gargalo'] = False
                continue
                
            # Pega o evento imediatamente anterior
            evento_anterior = eventos[i - 1]
            data_ant_str = evento_anterior.get('data_evento', '')
            try:
                dt_anterior = datetime.strptime(data_ant_str, "%d/%m/%Y") if isinstance(data_ant_str, str) else data_ant_str
            except ValueError:
                dt_anterior = dt_atual

            # diferença entre dias
            diferenca = dt_atual - dt_anterior
            dias = diferenca.days
            
            evento_atual['dias_desde_ultimo_evento'] = dias
            
            # se demorar mais de 60 dias, levanta a flag
            evento_atual['is_gargalo'] = True if dias > 60 else False

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
                'numero_internacoes': numero_internacoes
            }
        }

