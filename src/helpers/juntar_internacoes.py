from datetime import datetime
from ..helpers.normalize_id import _normalize_id

date_format = '%d/%m/%Y, %H:%M'


def juntar_internacoes(eventos, internacoes_raw, pac_id):
    numero_internacoes = 0
    for item in internacoes_raw:
        if _normalize_id(item.get('codigo_paciente')) != pac_id:
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
        numero_internacoes += 1
    return numero_internacoes
