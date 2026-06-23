from fastapi import APIRouter, Depends

from ..controllers.dashboard_controller import DashboardController
from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.implementations.paciente_csv_provider import PacienteCsvProvider


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


def get_dashboard_controller() -> DashboardController:
    return DashboardController(
        consulta_provider=ConsultasCsvProvider(),
        exame_provider=ExameCsvProvider(),
        internacao_provider=InternacoesCsvProvider(),
        paciente_provider=PacienteCsvProvider(),
    )

@router.get("", response_model=dict)
async def get_dashboard(
    especialidade: str,
    data_inicio: str,
    data_fim: str,
    controller: DashboardController = Depends(
        get_dashboard_controller
    ),
):
    data = await controller.get_dashboard(
        especialidade=especialidade,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )
    print(data)
    return data