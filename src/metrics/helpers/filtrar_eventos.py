from datetime import datetime

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

_CAMPOS_ESPECIALIDADE = {
    "consulta": "especialidade",
    "internacao": "especialidade",
    "cirurgia": "especialidade",
    "exame": "especialidade_solicitante_nome",
}

_DATE_FMT = "%d/%m/%Y, %H:%M"

def _formatar_data_iso_para_padrao(data_iso: str, fim_do_dia: bool = False) -> str:
    """
    Converte uma data ISO 'YYYY-MM-DD' (recebida via query params da API)
    para o formato 'DD/MM/YYYY, HH:MM' usado pelos helpers de jornada.
    """
    data = datetime.strptime(data_iso, "%Y-%m-%d")
    hora = "23:59" if fim_do_dia else "00:00"
    return f"{data.strftime('%d/%m/%Y')}, {hora}"


def _parse_dt(s: str) -> datetime | None:
    """Parse simples e local, usado só para a comparação de período."""
    if not s:
        return None
    try:
        return datetime.strptime(s.strip(), _DATE_FMT)
    except ValueError:
        return None




def filtrar_eventos(evento: str, dados, especialidade):
    campo = _CAMPOS_ESPECIALIDADE[evento]

    palavra = GRUPOS_ESPECIALIDADE.get(
        especialidade.lower(),
        especialidade.upper()
    )

    return [
        d
        for d in dados
        if _deve_incluir_evento(d, campo, palavra)
    ]


def _deve_incluir_evento(dados_evento: dict, campo: str, palavra: str) -> bool:
    valor = dados_evento.get(campo)
    if valor is None:
        return True
    return palavra in str(valor).upper()
    
    
def filtrar_eventos_por_periodo(eventos: list[dict], data_inicio: str, data_fim: str) -> list[dict]:
    """
    filtra uma lista de eventos (consultas, exames, internações, cirurgias)
    mantendo apenas os que possuem 'data_hora_realizacao' dentro do período
    """
    inicio_formatado = _formatar_data_iso_para_padrao(data_inicio, fim_do_dia=False)
    fim_formatado = _formatar_data_iso_para_padrao(data_fim, fim_do_dia=True)

    inicio_dt = _parse_dt(inicio_formatado)
    fim_dt = _parse_dt(fim_formatado)

    if inicio_dt is None or fim_dt is None:
        return []

    eventos_filtrados = []
    for evento in eventos:
        data_evento = evento.get("data_hora_realizacao")
        if not data_evento:
            continue

        evento_dt = _parse_dt(data_evento)
        if evento_dt is None:
            continue

        if inicio_dt <= evento_dt <= fim_dt:
            eventos_filtrados.append(evento)

    return eventos_filtrados