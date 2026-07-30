from sqlalchemy import Column, Integer, String, JSON, DateTime, Index
from datetime import datetime
from ..resources.database import Base

class MetricaHistorico(Base):
    __tablename__ = "metricas_historico"

    id = Column(Integer, primary_key=True, autoincrement=True)
    especialidade = Column(String, nullable=True)     # None = "todas"
    data_inicio = Column(String, nullable=False)
    data_fim = Column(String, nullable=False)
    dashboard = Column(JSON, nullable=False)          
    calculado_em = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_metrica_filtro", "especialidade", "data_inicio", "data_fim"),
    )