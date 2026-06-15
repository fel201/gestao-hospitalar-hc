from datetime import datetime
from typing import List


def calculate_time_intervals(eventos: List[dict]) -> None:
    """Preenche o campo `tempo_intervalo_horas` entre eventos consecutivos.

    A função espera que a lista `eventos` já esteja ordenada por
    `data_evento` em ordem cronológica.
    """
    previous_timestamp = None

    for evento in eventos:
        timestamp = evento.get('data_evento')
        if not isinstance(timestamp, datetime):
            evento['tempo_intervalo_horas'] = None
            continue

        if previous_timestamp is None:
            evento['tempo_intervalo_horas'] = None
        else:
            delta = timestamp - previous_timestamp
            evento['tempo_intervalo_horas'] = round(delta.total_seconds() / 3600.0, 2)

        previous_timestamp = timestamp
