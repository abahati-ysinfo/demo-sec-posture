import uuid

from sqlalchemy import DECIMAL, Column, Date, Index, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


class AIDailyMetrics(Base):
    """Aggregated daily metrics for AI usage tracking"""

    __tablename__ = "ai_daily_metrics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(Date, nullable=False)
    total_reports = Column(Integer, default=0, nullable=False)
    total_sections = Column(Integer, default=0, nullable=False)
    total_tokens_prompt = Column(Integer, default=0, nullable=False)
    total_tokens_completion = Column(Integer, default=0, nullable=False)
    total_cost_usd: Column[DECIMAL] = Column(DECIMAL(10, 2), default=0, nullable=False)
    avg_latency_ms = Column(Integer, default=0, nullable=False)
    cache_hit_rate: Column[DECIMAL] = Column(DECIMAL(5, 2), default=0, nullable=False)
    success_rate: Column[DECIMAL] = Column(DECIMAL(5, 2), default=0, nullable=False)
    degraded_rate: Column[DECIMAL] = Column(DECIMAL(5, 2), default=0, nullable=False)
    created_at = Column(Date, server_default=func.current_date())

    __table_args__ = (Index("idx_daily_metrics_date", "date", unique=True),)
