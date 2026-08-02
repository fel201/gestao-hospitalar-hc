import asyncio

from src.metrics.metricas_consultas import dicionario_metricas_consultas
from src.providers.csv_file_provider import CsvFileProvider


def test_provider_supports_rename_integer_columns_and_lookup(tmp_path):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("paciente_id,nome\n1,Alice\n2,Bob\n1,Alice\n", encoding="utf-8")

    provider = CsvFileProvider(
        csv_path=str(csv_path),
        primary_key="paciente_id",
        rename={"nome": "nome_paciente"},
        integer_columns=["paciente_id"],
    )

    rows = asyncio.run(provider.get_rows())

    assert len(rows) == 2
    assert rows[0]["nome_paciente"] == "Alice"
    assert rows[0]["paciente_id"] == 1

    found = asyncio.run(provider.get_by_id("1"))
    assert found is not None
    assert found["nome_paciente"] == "Alice"


def test_metricas_consultas_inclui_primeira_consulta_nas_proporcoes():
    consultas = [
        {"prontuario": "1", "condicao": "PRIMEIRA CONSULTA", "retorno": "PACIENTE ATENDIDO"},
        {"prontuario": "2", "condicao": "CONSULTA REGULADA", "retorno": "PACIENTE ATENDIDO"},
        {"prontuario": "3", "condicao": "RETORNO", "retorno": "PACIENTE ATENDIDO"},
        {"prontuario": "4", "condicao": "INTERCONSULTA", "retorno": "PACIENTE ATENDIDO"},
    ]

    metricas = dicionario_metricas_consultas(
        consultas=consultas,
        pacientes=[],
        especialidade="Cardiologia",
        data_inicio="2025-01-01",
        data_fim="2025-01-31",
    )

    proporcoes = metricas["porcentagem_tipos_consulta"]
    assert proporcoes["Primeira consulta"] == "25.0%"
    assert proporcoes["Reguladas"] == "25.0%"
    assert proporcoes["Retornos"] == "25.0%"
    assert proporcoes["Interconsultas"] == "25.0%"
