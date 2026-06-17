from datetime import datetime
from typing import List, Optional


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


def filter_by_specification(eventos: List[dict], especificacao: Optional[List[str]] = None) -> List[dict]:
    """Filtra eventos da jornada por tipos especificados e preserva a ordem cronológica."""
    if not especificacao:
        return eventos

    tipos_aceitos = {tipo.strip().lower() for tipo in especificacao if tipo}
    if not tipos_aceitos:
        return eventos

    return [
        evento
        for evento in eventos
        if str(evento.get('tipo', '')).strip().lower() in tipos_aceitos
    ]
