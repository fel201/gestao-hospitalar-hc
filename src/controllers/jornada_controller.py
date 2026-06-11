from typing import Dict, Any, List
from datetime import datetime
from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.interfaces.paciente_provider_interface import PacienteProviderInterface

date_format = '%d/%m/%Y %H:%M'
class JornadaController:
    @staticmethod
    # essa função remove tudo que não for número dos IDS 
    # para melhorar compatibilidade entre as tabelas
    def _normalize_id(value: Any) -> str:
        return ''.join(ch for ch in str(value) if ch.isdigit())

    @classmethod
    async def obter_jornada_paciente(
        cls,
        pac_id: int,
        paciente_provider: PacienteProviderInterface,
        consultas_provider: ConsultasCsvProvider,
        exames_provider: ExameCsvProvider,
        internacoes_provider: InternacoesCsvProvider,
    ) -> Dict[str, Any]:
        paciente = await paciente_provider.obter_paciente_por_codigo(pac_id)

        pac_id_normalized = cls._normalize_id(pac_id)

        eventos = []
        consultas_raw = await consultas_provider.listar_consultas()
        for item in consultas_raw:
            if cls._normalize_id(item.get('paciente_id')) != pac_id_normalized:
                continue
            eventos.append({
                'tipo': 'consulta',
                'consulta_id': item.get('id'),
                'pac_id': pac_id,
                'cid': item.get('CID', item.get('cid', '')),
                'data_evento': datetime.strptime(item.get('data_hora_consulta'), date_format),
                'data_hora_fim': item.get('Data/Hora de Fim', item.get('data_hora_fim', '')),
                'justificativa': item.get('Justificativa', ''),
                'justificativa_falta': item.get('Justificativa da Falta', ''),
                'tipo_consulta': item.get('tipo', item.get('tipo_consulta', '')),
                'especialidade': item.get('especialidade'),
                'procedimento': item.get('procedimento'),
                'data_procedimento': item.get('data_procedimento', ''),
                'indica_retorno': item.get('Retorno', '') or item.get('indica_retorno', ''),
            })
        exames_raw = await exames_provider.listar_exames()
        for item in exames_raw:
            if cls._normalize_id(item.get('paciente_id')) != pac_id_normalized:
                continue
            eventos.append({
                'tipo': 'exame',
                'exame_id': item.get('exame_id'),
                'pac_id': pac_id,
                'atendimento_id': item.get('atendimento_id'),
                'nome_exame': item.get('nome_exame'),
                'tipo_exame': item.get('tipo_exame'),
                'data_hora_solicitacao': item.get('data_hora_solicitacao'),
                'data_evento': datetime.strptime(item.get('data_hora_realizacao'), date_format),
                'data_hora_liberacao': item.get('data_hora_liberacao'),
                'situacao_exame': item.get('situacao', item.get('situacao_exame', '')),
                'especialidade_solicitante_nome': item.get('especialidade_solicitante_nome'),
                'unidade_executora_id': item.get('unidade_executora_id'),
            })
        internacoes_raw = await internacoes_provider.listar_internacoes()
        for item in internacoes_raw:
            if cls._normalize_id(item.get('codigo_paciente')) != pac_id_normalized:
                continue
            eventos.append({
                'tipo': 'internacao',
                'internacao_id': item.get('id_internacao'),
                'pac_id': pac_id,
                'atendimento_id': item.get('atendimento'),
                'data_evento': datetime.strptime(item.get('dthr_inicio'), date_format),
                'dthr_fim': item.get('dthr_fim'),
                'tempo_permanencia_dias': item.get('tempo_permanencia_dias'),
                'situacao_sumario_alta': item.get('Indica situação do sumário de alta', item.get('situacao_sumario_alta', '')),
                'descricao_origem_evento': item.get('descricao_origem_evento'),
                'descricao_tipo_alta_medica': item.get('descricao_tipo_alta_medica'),
                'especialidade': item.get('esp_nome_especialidade')
            })
        # ordenando cronologicamente com base na data de inicio de cada evento
        eventos.sort(key=lambda evento: evento['data_evento'])
        return {
            'paciente': {
                'pac_id': paciente.get('codigo'),
                'prontuario': paciente.get('prontuario'),
                'nome': paciente.get('nome'),
            },
            'eventos': eventos
        }
