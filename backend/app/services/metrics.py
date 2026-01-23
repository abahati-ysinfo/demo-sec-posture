"""AI Metrics Service for tracking costs, tokens, latency, and success rates"""

import logging
from datetime import date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ai_cache import AISectionCache
from app.models.ai_daily_metrics import AIDailyMetrics
from app.models.ai_metadata import AIGenerationMetadata

logger = logging.getLogger(__name__)


class AIMetricsService:
    """Track and aggregate AI usage metrics"""

    PRICING = {
        "gpt-4": {
            "prompt": 0.01 / 1000,  # $0.01 per 1K tokens
            "completion": 0.03 / 1000,  # $0.03 per 1K tokens
        },
        "gpt-4-turbo": {
            "prompt": 0.01 / 1000,
            "completion": 0.03 / 1000,
        },
        "gpt-3.5-turbo": {
            "prompt": 0.0005 / 1000,
            "completion": 0.0015 / 1000,
        },
    }

    @staticmethod
    def calculate_cost(
        model: str, tokens_prompt: int, tokens_completion: int
    ) -> Decimal:
        """Calculate cost for API call"""
        pricing = AIMetricsService.PRICING.get(model, AIMetricsService.PRICING["gpt-4"])

        cost = (
            tokens_prompt * pricing["prompt"]
            + tokens_completion * pricing["completion"]
        )
        return Decimal(str(round(cost, 6)))

    @staticmethod
    def record_generation(
        db: Session,
        report_id: str,
        section_id: str,
        model: str,
        tokens_prompt: int,
        tokens_completion: int,
        latency_ms: int,
        is_degraded: bool = False,
    ) -> None:
        """Record metrics for a generation"""
        cost = AIMetricsService.calculate_cost(model, tokens_prompt, tokens_completion)

        metadata = (
            db.query(AIGenerationMetadata)
            .filter(
                AIGenerationMetadata.report_id == report_id,
                AIGenerationMetadata.section_id == section_id,
            )
            .order_by(AIGenerationMetadata.created_at.desc())
            .first()
        )

        if metadata:
            metadata.total_cost_usd = cost  # type: ignore[assignment]
            metadata.is_degraded = 1 if is_degraded else 0  # type: ignore[assignment]
            db.commit()

    @staticmethod
    def aggregate_daily_metrics(
        db: Session, target_date: date | None = None
    ) -> AIDailyMetrics:
        """Aggregate metrics for a specific date"""
        if not target_date:
            target_date = date.today() - timedelta(days=1)  # Yesterday

        start_dt = datetime.combine(target_date, datetime.min.time())
        end_dt = datetime.combine(target_date, datetime.max.time())

        metrics = (
            db.query(
                func.count(func.distinct(AIGenerationMetadata.report_id)).label(
                    "total_reports"
                ),
                func.count(AIGenerationMetadata.id).label("total_sections"),
                func.sum(AIGenerationMetadata.tokens_prompt).label(
                    "total_tokens_prompt"
                ),
                func.sum(AIGenerationMetadata.tokens_completion).label(
                    "total_tokens_completion"
                ),
                func.sum(AIGenerationMetadata.total_cost_usd).label("total_cost_usd"),
                func.avg(AIGenerationMetadata.latency_ms).label("avg_latency_ms"),
                func.sum(AIGenerationMetadata.is_degraded).label("degraded_count"),
            )
            .filter(
                AIGenerationMetadata.created_at >= start_dt,
                AIGenerationMetadata.created_at <= end_dt,
            )
            .first()
        )

        cache_stats = (
            db.query(
                func.count(AISectionCache.id).label("cache_entries"),
                func.sum(AISectionCache.hit_count).label("total_hits"),
            )
            .filter(
                AISectionCache.last_used_at >= start_dt,
                AISectionCache.last_used_at <= end_dt,
            )
            .first()
        )

        cache_hit_rate = Decimal("0")
        if metrics.total_sections and cache_stats and cache_stats.total_hits:
            total_requests = metrics.total_sections + (cache_stats.total_hits or 0)
            cache_hit_rate = Decimal(
                str(round((cache_stats.total_hits / total_requests) * 100, 2))
            )

        success_rate = Decimal("100")
        degraded_rate = Decimal("0")
        if metrics.total_sections:
            degraded_count = metrics.degraded_count or 0
            degraded_rate = Decimal(
                str(round((degraded_count / metrics.total_sections) * 100, 2))
            )
            success_rate = Decimal("100") - degraded_rate

        daily_metric = AIDailyMetrics(
            date=target_date,
            total_reports=metrics.total_reports or 0,
            total_sections=metrics.total_sections or 0,
            total_tokens_prompt=metrics.total_tokens_prompt or 0,
            total_tokens_completion=metrics.total_tokens_completion or 0,
            total_cost_usd=Decimal(str(metrics.total_cost_usd or 0)),
            avg_latency_ms=int(metrics.avg_latency_ms or 0),
            cache_hit_rate=cache_hit_rate,
            success_rate=success_rate,
            degraded_rate=degraded_rate,
        )

        existing = (
            db.query(AIDailyMetrics).filter(AIDailyMetrics.date == target_date).first()
        )
        if existing:
            for key, value in daily_metric.__dict__.items():
                if not key.startswith("_"):
                    setattr(existing, key, value)
        else:
            db.add(daily_metric)

        db.commit()

        logger.info(f"Aggregated metrics for {target_date}")
        return daily_metric

    @staticmethod
    def get_report_cost(db: Session, report_id: str) -> dict:
        """Get cost breakdown for a specific report"""
        metrics = (
            db.query(AIGenerationMetadata)
            .filter(AIGenerationMetadata.report_id == report_id)
            .all()
        )

        total_cost = sum(m.total_cost_usd or 0 for m in metrics)
        total_tokens = sum(
            (m.tokens_prompt or 0) + (m.tokens_completion or 0) for m in metrics
        )

        return {
            "report_id": report_id,
            "total_sections": len(metrics),
            "total_tokens": total_tokens,
            "total_cost_usd": float(total_cost),
            "avg_cost_per_section": float(total_cost / len(metrics)) if metrics else 0,
            "sections": [
                {
                    "section_id": m.section_id,
                    "tokens": (m.tokens_prompt or 0) + (m.tokens_completion or 0),
                    "cost_usd": float(m.total_cost_usd or 0),
                    "latency_ms": m.latency_ms,
                    "is_degraded": bool(m.is_degraded),
                }
                for m in metrics
            ],
        }


metrics_service = AIMetricsService()
