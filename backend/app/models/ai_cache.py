import uuid

from sqlalchemy import DECIMAL, Column, DateTime, Index, Integer, String, Text
from sqlalchemy.sql import func

from app.core.database import Base
from app.db.types import JSONBCompat


class AISectionCache(Base):
    """Cache for AI section analysis to avoid redundant API calls"""

    __tablename__ = "ai_section_cache"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    section_id = Column(String(100), nullable=False)
    answers_hash = Column(String(64), nullable=False)
    prompt_version = Column(String(20), nullable=False)
    schema_version = Column(String(20), nullable=False)
    model = Column(String(50), nullable=False)
    artifact_json = Column(JSONBCompat, nullable=False)
    storage_uri = Column(Text, nullable=True)
    tokens_prompt = Column(Integer, nullable=True)
    tokens_completion = Column(Integer, nullable=True)
    total_cost_usd: Column[DECIMAL] = Column(DECIMAL(10, 6), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used_at = Column(DateTime(timezone=True), server_default=func.now())
    hit_count = Column(Integer, default=1, nullable=False)

    __table_args__ = (
        Index(
            "idx_cache_lookup",
            "section_id",
            "answers_hash",
            "prompt_version",
            "model",
            unique=True,
        ),
    )
