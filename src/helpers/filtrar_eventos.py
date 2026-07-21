GRUPOS_ESPECIALIDADE = {
    "acupuntura": "ACUPUNTURA",
    "alergia": "ALERGIA",
    "cardiologia": "CARDIO",
    "cirurgia": "CIRURGIA",
    "endocrino": "ENDOCRINO",
    "gastroenterologia": "GASTRO",
    "ginecologia": "GINECO",
    "hematologia": "HEMATO",
    "mastologia": "MASTOLOGIA",
    "nefrologia": "NEFRO",
    "neurologia": "NEURO",
    "nutricao": "NUTRI",
    "oftalmo": "OFTALMO",
    "ortopedia": "ORTOP",
    "proctologia": "PROCTO",
    "reumato": "REUMATO",
    "urologia": "UROLOGIA",
    "servico_social": "SERVIÇO SOCIAL",
    "enfermagem": "ENFERMAGEM",
}

def filtrar_eventos(evento: str, dados, especialidade):
    campos = {
        "consulta": "especialidade",
        "internacao": "especialidade",
        "cirurgia": "especialidade",
        "exame": "especialidade_solicitante_nome",
    }

    campo = campos[evento]

    palavra = GRUPOS_ESPECIALIDADE.get(
        especialidade.lower(),
        especialidade.upper()
    )

    return [
        d
        for d in dados
        if palavra in d[campo].upper()
    ]

from datetime import datetime
from .jornada_utils import dias_entre


def _formatar_data_iso_para_padrao(data_iso: str, fim_do_dia: bool = False) -> str:
    """
    Converte uma data ISO 'YYYY-MM-DD' (recebida via query params da API)
    para o formato 'DD/MM/YYYY, HH:MM' usado pelos helpers de jornada.
    """
    data = datetime.strptime(data_iso, "%Y-%m-%d")
    hora = "23:59" if fim_do_dia else "00:00"
    return f"{data.strftime('%d/%m/%Y')}, {hora}"


def filtrar_eventos_por_periodo(eventos: list[dict], data_inicio: str, data_fim: str) -> list[dict]:
    """
    Filtra uma lista de eventos (consultas, exames, internações, cirurgias)
    mantendo apenas os que possuem 'data_hora_realizacao' dentro do período
    [data_inicio, data_fim].

    data_inicio e data_fim: strings no formato ISO 'YYYY-MM-DD',
    como recebidas via query params (ex: '2024-01-01').
    """
    inicio_formatado = _formatar_data_iso_para_padrao(data_inicio, fim_do_dia=False)
    fim_formatado = _formatar_data_iso_para_padrao(data_fim, fim_do_dia=True)

    eventos_filtrados = []
    for evento in eventos:
        data_evento = evento.get("data_hora_realizacao")
        if not data_evento:
            continue
        try:
            dias_desde_inicio = dias_entre(inicio_formatado, data_evento)
            dias_ate_fim = dias_entre(data_evento, fim_formatado)
        except ValueError:
            # data do evento em formato inválido/inesperado -> ignora o evento
            continue
        
        print(data_evento if "2024" in data_evento else "")
        if dias_desde_inicio >= 0 and dias_ate_fim >= 0:
            eventos_filtrados.append(evento)

    return eventos_filtrados