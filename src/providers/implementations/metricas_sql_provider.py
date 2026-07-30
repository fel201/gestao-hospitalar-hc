# providers/implementations/metricas_sql_provider.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..interfaces.metrica_provider_interface import MetricaProviderInterface
from ...models.metrica_historico import MetricaHistorico

class MetricaSqliteProvider(MetricaProviderInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def salvar_snapshot(self, especialidade, data_inicio, data_fim, dashboard):
        registro = MetricaHistorico(
            especialidade=especialidade,
            data_inicio=data_inicio,
            data_fim=data_fim,
            dashboard=dashboard,
        )
        self.session.add(registro)
        await self.session.commit()

    async def buscar_snapshot(self, especialidade, data_inicio, data_fim):
        stmt = (
            select(MetricaHistorico)
            .where(
                MetricaHistorico.especialidade == especialidade,
                MetricaHistorico.data_inicio == data_inicio,
                MetricaHistorico.data_fim == data_fim,
            )
            .order_by(MetricaHistorico.calculado_em.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        registro = result.scalar_one_or_none()
        return registro.dashboard if registro else None