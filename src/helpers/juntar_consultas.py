from datetime import datetime
from ..helpers.normalize_id import _normalize_id
date_format = '%d/%m/%Y %H:%M'


def juntar_consultas(eventos, consultas_raw, pac_id):
    numero_consultas = 0
    for item in consultas_raw:
        if _normalize_id(item.get('paciente_id')) != pac_id:
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
        numero_consultas += 1
        
    return numero_consultas