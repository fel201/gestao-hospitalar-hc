from datetime import datetime
from ..helpers.normalize_id import _normalize_id
date_format = '%d/%m/%Y %H:%M'
def juntar_exames(eventos, exames_raw, pac_id):
    numero_exames = 0
    for item in exames_raw:
        if _normalize_id(item.get('paciente_id')) != pac_id:
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
        numero_exames += 1
    return numero_exames
