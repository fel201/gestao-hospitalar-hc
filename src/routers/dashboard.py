# routers/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..controllers.dashboard_controller import DashboardController
from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.implementations.paciente_csv_provider import PacienteCsvProvider
from ..providers.implementations.cirurgias_csv_provider import CirurgiasCsvProvider
from ..providers.implementations.metricas_sql_provider import MetricaSqliteProvider
from ..resources.database import get_app_db_session   # <-- import que faltava

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


def get_dashboard_controller(
    session: AsyncSession = Depends(get_app_db_session),   
) -> DashboardController:
    return DashboardController(
        consulta_provider=ConsultasCsvProvider(),
        exame_provider=ExameCsvProvider(),
        internacao_provider=InternacoesCsvProvider(),
        cirurgia_provider=CirurgiasCsvProvider(),
        paciente_provider=PacienteCsvProvider(),
        metrica_provider=MetricaSqliteProvider(session=session),  
    )


@router.get("", response_model=dict)
async def get_dashboard(
    especialidade: str | None = None,
    data_inicio: str = ...,
    data_fim: str = ...,
    controller: DashboardController = Depends(get_dashboard_controller),
):
    return await controller.get_dashboard(
        especialidade=especialidade,
        data_inicio=data_inicio,
        data_fim=data_fim
    )