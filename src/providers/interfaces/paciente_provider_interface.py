from abc import ABC, abstractmethod
from typing import List, Dict, Any

class PacienteProviderInterface(ABC):
    """Interface (contrato) para provedores de dados de pacientes."""

    @abstractmethod
    async def listar_pacientes(
        self,
        page: int = 1,
        limit: int=50,
        especialidade: str | None = None,
        unidade: str | None = None,
        data_inicio: str | None = None,
        data_fim: str | None = None,
        ordenar_por: str = "nome"

        ) -> List[Dict[str, Any]]:
        """Deve retornar uma lista de pacientes com suporte a paginação e filtros"""


    @abstractmethod
    async def obter_paciente_por_codigo(self, codigo: int) -> Dict[str, Any]:
        """Deve retornar um único paciente pelo seu código."""
        pass

    # adições para o controller criar paciente
    @abstractmethod
    async def obter_paciente_por_prontuario(self, prontuario: str) -> Dict[str, Any]:
        """Deve retornar um paciente baseado no número do prontuário."""
        pass

    @abstractmethod
    async def salvar_paciente(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Deve persistir um novo paciente no banco de dados."""
        pass
