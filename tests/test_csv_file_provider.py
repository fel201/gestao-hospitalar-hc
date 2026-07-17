import asyncio

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
