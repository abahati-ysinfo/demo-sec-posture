import uuid

from sqlalchemy import (
    DECIMAL,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.sql import func

from app.core.database import Base


class AIGenerationMetadata(Base):
    """Tracks AI generation metadata for versioning and cost tracking"""

    __tablename__ = "ai_generation_metadata"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    report_id = Column(
        String(36), ForeignKey("reports.id", ondelete="CASCADE"), nullable=False
    )
    section_id = Column(String(100), nullable=True)  # NULL for synthesis
    prompt_version = Column(String(20), nullable=False)
    schema_version = Column(String(20), nullable=False)
    model = Column(String(50), nullable=False)
    temperature = Column(Float, nullable=False)
    max_tokens = Column(Integer, nullable=False)
    tokens_prompt = Column(Integer, nullable=True)
    tokens_completion = Column(Integer, nullable=True)
    finish_reason = Column(
        String(50), nullable=True
    )  # stop, length, content_filter, etc.
    total_cost_usd: Column[DECIMAL] = Column(DECIMAL(10, 6), nullable=True)
    latency_ms = Column(Integer, nullable=True)
    attempt_count = Column(Integer, default=1, nullable=False)
    error_code = Column(String(50), nullable=True)
    error_message = Column(String, nullable=True)
    fallback_model = Column(String(50), nullable=True)
    is_degraded = Column(
        Integer, default=0, nullable=False
    )  # SQLite compatible boolean
    last_retry_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_ai_metadata_report_section", "report_id", "section_id"),
    )
