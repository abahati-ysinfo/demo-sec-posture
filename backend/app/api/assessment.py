from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.assessment_tiers import ASSESSMENT_TIERS, get_tier_sections
from app.core.config import settings
from app.core.database import get_db
from app.middleware.rate_limit import limiter
from app.models.assessment import Assessment, Report
from app.models.assessment import AssessmentResponse as AssessmentResponseModel
from app.models.user import User
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentResponse,
    AssessmentResponseResponse,
    AssessmentStructure,
    ConsultationRequest,
    SaveProgressRequest,
)
from app.schemas.user import CurrentUserResponse
from app.services.question_parser import (
    filter_structure_by_sections,
    load_assessment_structure_cached,
)
from app.services.report_generator import generate_standard_report

router = APIRouter()


@router.get("/structure", response_model=AssessmentStructure)
async def get_assessment_structure(request: Request) -> AssessmentStructure:
    """Get the complete assessment structure with all questions"""
    return load_assessment_structure_cached()


@router.get("/{assessment_id}/filtered-structure", response_model=AssessmentStructure)
async def get_filtered_assessment_structure(
    request: Request,
    assessment_id: str,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AssessmentStructure:
    """Get the assessment structure filtered by selected sections for this assessment"""
    assessment = (
        db.query(Assessment)
        .filter(
            and_(Assessment.id == assessment_id, Assessment.user_id == current_user.id)
        )
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
        )

    structure = load_assessment_structure_cached()

    if assessment.selected_section_ids:
        structure = filter_structure_by_sections(
            structure,
            list(assessment.selected_section_ids),  # type: ignore[arg-type]
        )

    return structure


@router.post("/start", response_model=AssessmentResponse)
async def start_assessment(
    request: Request,
    assessment_data: AssessmentCreate | None = None,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AssessmentResponse:
    """Start a new assessment for the current user"""

    if (
        hasattr(current_user, "email")
        and current_user.email == "testuser@assessment.com"
    ):
        existing_test_user = db.query(User).filter(User.id == current_user.id).first()
        if not existing_test_user:
            test_user_db = User(
                id=current_user.id,
                email=current_user.email,
                full_name=current_user.full_name,
                company_name=current_user.company_name,
                password_hash="$2b$12$dummy_hash_for_test_user_only",
                is_active=True,
            )
            db.add(test_user_db)
            db.commit()
            db.refresh(test_user_db)

    existing_assessment = (
        db.query(Assessment)
        .filter(
            and_(
                Assessment.user_id == current_user.id,
                Assessment.status == "in_progress",
            )
        )
        .first()
    )

    if existing_assessment:
        return AssessmentResponse.model_validate(existing_assessment)

    total_assessments = (
        db.query(Assessment).filter(Assessment.user_id == current_user.id).count()
    )

    if total_assessments >= 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have reached the maximum limit of 3 assessments. No more assessments can be taken.",
        )

    next_attempt_number = total_assessments + 1

    selected_section_ids = None
    if assessment_data and assessment_data.selected_section_ids:
        selected_section_ids = assessment_data.selected_section_ids
        structure = load_assessment_structure_cached()
        valid_section_ids = {section.id for section in structure.sections}
        invalid_ids = set(selected_section_ids) - valid_section_ids
        if invalid_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid section IDs: {', '.join(invalid_ids)}",
            )

    expires_at = datetime.now(UTC) + timedelta(days=settings.ASSESSMENT_EXPIRY_DAYS)

    assessment = Assessment(
        user_id=current_user.id,
        attempt_number=next_attempt_number,
        status="in_progress",
        started_at=datetime.now(UTC),
        expires_at=expires_at,
        last_saved_at=datetime.now(UTC),
        progress_percentage=0.0,
        selected_section_ids=selected_section_ids,
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return AssessmentResponse.model_validate(assessment)


@router.get("/current", response_model=AssessmentResponse)
async def get_current_assessment(
    request: Request,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AssessmentResponse:
    """Get the current assessment for the user"""

    assessment = (
        db.query(Assessment)
        .filter(
            and_(
                Assessment.user_id == current_user.id,
                Assessment.status == "in_progress",
            )
        )
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No active assessment found"
        )

    if assessment.expires_at and datetime.now(UTC) > assessment.expires_at.replace(
        tzinfo=UTC
    ):
        assessment.status = "expired"  # type: ignore[assignment]
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail="Assessment has expired"
        )

    return AssessmentResponse.model_validate(assessment)


@router.get("/latest", response_model=AssessmentResponse)
async def get_latest_assessment(
    request: Request,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AssessmentResponse:
    """Get the latest assessment for the user (in-progress if exists, else most recent completed)"""

    in_progress_assessment = (
        db.query(Assessment)
        .filter(
            and_(
                Assessment.user_id == current_user.id,
                Assessment.status == "in_progress",
            )
        )
        .first()
    )

    if in_progress_assessment:
        if in_progress_assessment.expires_at and datetime.now(
            UTC
        ) > in_progress_assessment.expires_at.replace(tzinfo=UTC):
            in_progress_assessment.status = "expired"  # type: ignore[assignment]
            db.commit()
        else:
            return AssessmentResponse.model_validate(in_progress_assessment)

    completed_assessment = (
        db.query(Assessment)
        .filter(
            and_(
                Assessment.user_id == current_user.id,
                Assessment.status == "completed",
            )
        )
        .order_by(Assessment.completed_at.desc())
        .first()
    )

    if completed_assessment:
        return AssessmentResponse.model_validate(completed_assessment)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No assessment found"
    )


@router.get("/history", response_model=list[AssessmentResponse])
async def get_assessment_history(
    request: Request,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[AssessmentResponse]:
    """Get all assessments for the current user, ordered by attempt number"""

    assessments = (
        db.query(Assessment)
        .filter(Assessment.user_id == current_user.id)
        .order_by(Assessment.attempt_number.asc())
        .all()
    )

    return [AssessmentResponse.model_validate(assessment) for assessment in assessments]


@router.get("/can-retake")
async def can_retake_assessment(
    request: Request,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, bool | int]:
    """Check if the user can retake the assessment"""

    total_assessments = (
        db.query(Assessment).filter(Assessment.user_id == current_user.id).count()
    )

    in_progress_assessment = (
        db.query(Assessment)
        .filter(
            and_(
                Assessment.user_id == current_user.id,
                Assessment.status == "in_progress",
            )
        )
        .first()
    )

    can_retake = total_assessments < 3 and not in_progress_assessment
    attempts_remaining = max(0, 3 - total_assessments)

    return {
        "can_retake": can_retake,
        "total_attempts": total_assessments,
        "attempts_remaining": attempts_remaining,
        "has_in_progress": in_progress_assessment is not None,
    }


@router.get(
    "/{assessment_id}/responses", response_model=list[AssessmentResponseResponse]
)
async def get_assessment_responses(
    request: Request,
    assessment_id: str,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[AssessmentResponseResponse]:
    """Get all responses for an assessment"""

    assessment = (
        db.query(Assessment)
        .filter(
            and_(Assessment.id == assessment_id, Assessment.user_id == current_user.id)
        )
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
        )

    responses = (
        db.query(AssessmentResponseModel)
        .filter(AssessmentResponseModel.assessment_id == assessment_id)
        .all()
    )

    return [
        AssessmentResponseResponse.model_validate(response) for response in responses
    ]


@router.post("/{assessment_id}/save-progress")
@limiter.limit(
    "10/minute",
    exempt_when=lambda *args, **kwargs: not settings.ENABLE_SAVE_PROGRESS_RATE_LIMIT,
)
async def save_assessment_progress(
    request: Request,
    assessment_id: str,
    progress_data: SaveProgressRequest,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str | float]:
    """Save assessment progress"""

    assessment = (
        db.query(Assessment)
        .filter(
            and_(
                Assessment.id == assessment_id,
                Assessment.user_id == current_user.id,
                Assessment.status == "in_progress",
            )
        )
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found or not in progress",
        )

    if assessment.expires_at and datetime.now(UTC) > assessment.expires_at.replace(
        tzinfo=UTC
    ):
        assessment.status = "expired"  # type: ignore[assignment]
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail="Assessment has expired"
        )

    question_ids = [r.question_id for r in progress_data.responses]
    existing_responses = (
        db.query(AssessmentResponseModel)
        .filter(
            and_(
                AssessmentResponseModel.assessment_id == assessment_id,
                AssessmentResponseModel.question_id.in_(question_ids),
            )
        )
        .all()
    )

    existing_by_question = {str(r.question_id): r for r in existing_responses}

    new_responses_count = 0

    for response_data in progress_data.responses:
        existing_response = existing_by_question.get(str(response_data.question_id))

        if existing_response:
            existing_response.answer_value = response_data.answer_value  # type: ignore[assignment]
            existing_response.comment = response_data.comment  # type: ignore[assignment]
            existing_response.updated_at = datetime.now(UTC)  # type: ignore[assignment]
        else:
            new_response = AssessmentResponseModel(
                assessment_id=assessment_id,
                section_id=response_data.section_id,
                question_id=response_data.question_id,
                answer_value=response_data.answer_value,
                comment=response_data.comment,
            )
            db.add(new_response)
            new_responses_count += 1

    assessment.last_saved_at = datetime.now(UTC)  # type: ignore[assignment]

    total_responses = (
        db.query(AssessmentResponseModel)
        .filter(AssessmentResponseModel.assessment_id == assessment_id)
        .count()
    )

    structure = load_assessment_structure_cached()

    if assessment.selected_section_ids:
        structure = filter_structure_by_sections(
            structure,
            list(assessment.selected_section_ids),  # type: ignore[arg-type]
        )

    total_questions = structure.total_questions

    if total_questions > 0:
        assessment.progress_percentage = (total_responses / total_questions) * 100  # type: ignore[assignment]

    db.commit()

    return {
        "message": "Progress saved successfully",
        "progress_percentage": float(assessment.progress_percentage),
    }


@router.post("/{assessment_id}/complete")
async def complete_assessment(
    request: Request,
    assessment_id: str,
    background_tasks: BackgroundTasks,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Complete an assessment and automatically generate standard report"""

    assessment = (
        db.query(Assessment)
        .filter(
            and_(
                Assessment.id == assessment_id,
                Assessment.user_id == current_user.id,
                Assessment.status == "in_progress",
            )
        )
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found or not in progress",
        )

    if assessment.expires_at and datetime.now(UTC) > assessment.expires_at.replace(
        tzinfo=UTC
    ):
        assessment.status = "expired"  # type: ignore[assignment]
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail="Assessment has expired"
        )

    assessment.status = "completed"  # type: ignore[assignment]
    assessment.completed_at = datetime.now(UTC)  # type: ignore[assignment]
    assessment.progress_percentage = 100.0  # type: ignore[assignment]

    db.commit()

    existing_report = (
        db.query(Report)
        .filter(
            and_(
                Report.assessment_id == assessment_id, Report.report_type == "standard"
            )
        )
        .first()
    )

    if not existing_report:
        report = Report(
            assessment_id=assessment_id, report_type="standard", status="generating"
        )

        db.add(report)
        try:
            db.commit()
            db.refresh(report)
            background_tasks.add_task(generate_standard_report, str(report.id))
        except IntegrityError:
            db.rollback()
            existing_report = (
                db.query(Report)
                .filter(
                    and_(
                        Report.assessment_id == assessment_id,
                        Report.report_type == "standard",
                    )
                )
                .first()
            )

    return {
        "message": "Assessment completed successfully. Your report is being generated."
    }


@router.post("/{assessment_id}/consultation")
async def save_consultation_interest(
    request: Request,
    assessment_id: str,
    consultation_data: ConsultationRequest,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Save consultation interest and details"""

    assessment = (
        db.query(Assessment)
        .filter(
            and_(Assessment.id == assessment_id, Assessment.user_id == current_user.id)
        )
        .first()
    )

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment.consultation_interest = consultation_data.consultation_interest  # type: ignore[assignment]
    assessment.consultation_details = consultation_data.consultation_details  # type: ignore[assignment]

    db.commit()
    return {"message": "Consultation preferences saved"}


@router.get("/tiers")
async def get_assessment_tiers() -> dict[str, dict[str, dict[str, str | int]]]:
    """Get available assessment tiers"""
    return {
        "tiers": {
            tier_id: {
                "name": tier_info["name"],
                "description": tier_info["description"],
                "duration": tier_info["duration"],
                "total_questions": tier_info["total_questions"],
            }
            for tier_id, tier_info in ASSESSMENT_TIERS.items()
        }
    }


@router.post("/start-with-tier")
async def start_assessment_with_tier(
    request: Request,
    tier_request: dict[str, str],
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, dict[str, object]]:
    """Start assessment with selected tier"""

    tier = tier_request.get("tier")
    if tier not in ASSESSMENT_TIERS:
        raise HTTPException(status_code=400, detail="Invalid tier")

    selected_sections = get_tier_sections(tier)

    assessment = Assessment(
        user_id=current_user.id,
        status="in_progress",
        started_at=datetime.now(UTC),
        expires_at=datetime.now(UTC) + timedelta(days=30),
        selected_section_ids=selected_sections,
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    assessment_response = AssessmentResponse.model_validate(assessment)
    assessment_dict = assessment_response.model_dump()
    assessment_dict["metadata"] = {"tier": tier}
    return {"data": assessment_dict}
