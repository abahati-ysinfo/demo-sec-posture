"""AI caching service for intelligent caching of AI section analysis"""

import hashlib
import json
import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.ai_cache import AISectionCache
from app.schemas.ai_artifacts import SectionAIArtifact

logger = logging.getLogger(__name__)


class AICacheService:
    """Intelligent caching for AI section analysis"""

    @staticmethod
    def compute_answers_hash(section_responses: list[dict]) -> str:
        """Compute deterministic hash of normalized answers, comments, and context"""
        normalized = sorted(
            [
                {
                    "q": resp["question"][:100],
                    "a": str(resp["answer"]).strip().lower(),
                    "w": resp["weight"],
                    "c": str(resp.get("comment", "")).strip().lower()
                    if resp.get("comment")
                    else "",
                    "ctx": str(resp.get("context", "")).strip().lower()
                    if resp.get("context")
                    else "",
                }
                for resp in section_responses
            ],
            key=lambda x: x["q"],
        )

        canonical_json = json.dumps(normalized, sort_keys=True)
        return hashlib.sha256(canonical_json.encode()).hexdigest()

    @staticmethod
    def get_cached_artifact(
        db: Session, section_id: str, answers_hash: str, prompt_version: str, model: str
    ) -> SectionAIArtifact | None:
        """Retrieve cached artifact if exists"""
        cache_entry = (
            db.query(AISectionCache)
            .filter(
                AISectionCache.section_id == section_id,
                AISectionCache.answers_hash == answers_hash,
                AISectionCache.prompt_version == prompt_version,
                AISectionCache.model == model,
            )
            .first()
        )

        if cache_entry:
            cache_entry.last_used_at = datetime.utcnow()  # type: ignore[assignment]
            cache_entry.hit_count += 1  # type: ignore[assignment]
            db.commit()

            logger.info(
                f"Cache HIT for section {section_id} (hits: {cache_entry.hit_count})"
            )
            return SectionAIArtifact(**cache_entry.artifact_json)

        logger.info(f"Cache MISS for section {section_id}")
        return None

    @staticmethod
    def store_artifact(
        db: Session,
        section_id: str,
        answers_hash: str,
        prompt_version: str,
        schema_version: str,
        model: str,
        artifact: SectionAIArtifact,
        tokens_prompt: int,
        tokens_completion: int,
        cost_usd: float,
    ) -> None:
        """Store artifact in cache"""
        cache_entry = AISectionCache(
            section_id=section_id,
            answers_hash=answers_hash,
            prompt_version=prompt_version,
            schema_version=schema_version,
            model=model,
            artifact_json=artifact.model_dump(),
            tokens_prompt=tokens_prompt,
            tokens_completion=tokens_completion,
            total_cost_usd=cost_usd,
        )
        db.add(cache_entry)
        db.commit()
        logger.info(f"Cached artifact for section {section_id}")
