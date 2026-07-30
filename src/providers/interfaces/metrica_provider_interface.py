# src/providers/interfaces/metrica_provider_interface.py
from abc import ABC, abstractmethod

class MetricaProviderInterface(ABC):
    @abstractmethod
    async def salvar_snapshot(self, especialidade: str | None, data_inicio: str, data_fim: str, dashboard: dict) -> None:
        ...

    @abstractmethod
    async def buscar_snapshot(self, especialidade: str | None, data_inicio: str, data_fim: str) -> list[dict]:
        ...