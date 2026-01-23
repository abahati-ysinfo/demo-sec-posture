from sqlalchemy.orm import relationship

from app.models.ai_artifacts import AISectionArtifact, AISynthesisArtifact
from app.models.ai_cache import AISectionCache
from app.models.ai_daily_metrics import AIDailyMetrics
from app.models.ai_metadata import AIGenerationMetadata
from app.models.assessment import AdminAuditLog, Assessment, AssessmentResponse, Report
from app.models.openai_key import OpenAIAPIKey
from app.models.user import User

User.assessments = relationship(
    "Assessment", back_populates="user", cascade="all, delete-orphan"
)

__all__ = [
    "User",
    "Assessment",
    "AssessmentResponse",
    "Report",
    "AdminAuditLog",
    "OpenAIAPIKey",
    "AIGenerationMetadata",
    "AISectionArtifact",
    "AISynthesisArtifact",
    "AISectionCache",
    "AIDailyMetrics",
]
