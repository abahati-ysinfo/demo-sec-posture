import io
import logging
import os
import uuid
from datetime import UTC, datetime

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Query,
    Request,
    status,
)
from fastapi.responses import Response, StreamingResponse
from sqlalchemy import and_, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from starlette.background import BackgroundTask
from weasyprint import HTML

from app.api.auth import get_current_admin_user, get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.models.assessment import Assessment, AssessmentResponse, Report
from app.schemas.report import AdminReportResponse, AIReportRequest, UserReportResponse
from app.schemas.user import CurrentUserResponse
from app.services.question_parser import (
    filter_structure_by_sections,
    load_assessment_structure,
)
from app.services.report_generator import (
    calculate_assessment_scores,
    generate_ai_report,
    generate_ai_report_html,
    generate_report_html,
    generate_standard_report,
)
from app.services.storage import get_storage_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/{assessment_id}/generate", response_model=UserReportResponse)
async def generate_report(
    request: Request,
    assessment_id: str,
    background_tasks: BackgroundTasks,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserReportResponse | Response:
    """Generate a standard PDF report for a completed assessment"""

    region = os.getenv("FLY_REGION")
    primary = os.getenv("FLY_PRIMARY_REGION", "iad")
    if region and primary and region != primary:
        return Response(status_code=409, headers={"fly-replay": f"region={primary}"})

    assessment = (
        db.query(Assessment)
        .filter(
            and_(
                Assessment.id == assessment_id,
                Assessment.user_id == current_user.id,
                Assessment.status == "completed",
            )
        )
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found or not completed",
        )

    existing_report = (
        db.query(Report)
        .filter(
            and_(
                Report.assessment_id == assessment_id, Report.report_type == "standard"
            )
        )
        .first()
    )

    if existing_report:
        return UserReportResponse.model_validate(existing_report)

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
        if existing_report:
            return UserReportResponse.model_validate(existing_report)
        raise

    return UserReportResponse.model_validate(report)


@router.post("/{assessment_id}/request-ai-report")
async def request_ai_report(
    request: Request,
    assessment_id: str,
    request_data: AIReportRequest,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Request an AI-enhanced report (admin will generate it)"""

    assessment = (
        db.query(Assessment)
        .filter(
            and_(
                Assessment.id == assessment_id,
                Assessment.user_id == current_user.id,
                Assessment.status == "completed",
            )
        )
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found or not completed",
        )

    existing_report = (
        db.query(Report)
        .filter(
            and_(
                Report.assessment_id == assessment_id,
                Report.report_type == "ai_enhanced",
            )
        )
        .first()
    )

    if existing_report:
        return {
            "message": "AI report already requested",
            "status": str(existing_report.status),
            "estimated_delivery": "3-5 business days",
        }

    report = Report(
        assessment_id=assessment_id, report_type="ai_enhanced", status="pending"
    )

    db.add(report)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing_report = (
            db.query(Report)
            .filter(
                and_(
                    Report.assessment_id == assessment_id,
                    Report.report_type == "ai_enhanced",
                )
            )
            .first()
        )
        if existing_report:
            return {
                "message": "AI report already requested",
                "status": str(existing_report.status),
                "estimated_delivery": "3-5 business days",
            }
        raise

    return {
        "message": "AI report requested successfully",
        "status": "pending",
        "estimated_delivery": "3-5 business days",
    }


@router.post("/admin/{report_id}/generate-ai", response_model=AdminReportResponse)
async def admin_generate_ai_report(
    request: Request,
    report_id: str,
    background_tasks: BackgroundTasks,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> AdminReportResponse | Response:
    """Admin endpoint to generate AI-enhanced reports"""

    region = os.getenv("FLY_REGION")
    primary = os.getenv("FLY_PRIMARY_REGION", "iad")
    if region and primary and region != primary:
        return Response(status_code=409, headers={"fly-replay": f"region={primary}"})

    report = (
        db.query(Report)
        .filter(
            and_(
                Report.id == report_id,
                Report.report_type == "ai_enhanced",
                Report.status == "pending",
            )
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found or not pending",
        )

    report.status = "generating"  # type: ignore[assignment]
    db.commit()

    background_tasks.add_task(generate_ai_report, str(report.id))

    return AdminReportResponse.model_validate(report)


@router.post("/admin/{report_id}/retry-standard", response_model=AdminReportResponse)
async def admin_retry_standard_report(
    request: Request,
    report_id: str,
    background_tasks: BackgroundTasks,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> AdminReportResponse | Response:
    """Admin endpoint to retry generating a failed standard report"""

    region = os.getenv("FLY_REGION")
    primary = os.getenv("FLY_PRIMARY_REGION", "iad")
    if region and primary and region != primary:
        return Response(status_code=409, headers={"fly-replay": f"region={primary}"})

    report = (
        db.query(Report)
        .filter(
            and_(
                Report.id == report_id,
                Report.report_type == "standard",
                Report.status == "failed",
            )
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found or not in failed status",
        )

    report.status = "generating"  # type: ignore[assignment]
    report.file_path = None  # type: ignore[assignment]
    report.completed_at = None  # type: ignore[assignment]
    db.commit()

    background_tasks.add_task(generate_standard_report, str(report.id))

    return AdminReportResponse.model_validate(report)


@router.post("/admin/{report_id}/release")
async def admin_release_ai_report(
    request: Request,
    report_id: str,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Admin endpoint to release AI-enhanced reports to users"""

    report = (
        db.query(Report)
        .filter(
            and_(
                Report.id == report_id,
                Report.report_type == "ai_enhanced",
                Report.status == "completed",
            )
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found or not ready for release",
        )

    report.status = "released"  # type: ignore[assignment]
    db.commit()

    return {"message": "AI report released to user", "report_id": report_id}


@router.post("/admin/release-bulk")
async def admin_bulk_release_ai_reports(
    request: Request,
    report_ids: list[str],
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, str | int | list[str]]:
    """Admin endpoint to bulk release multiple AI-enhanced reports"""

    if not report_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No report IDs provided",
        )

    reports = (
        db.query(Report)
        .filter(
            and_(
                Report.id.in_(report_ids),
                Report.report_type == "ai_enhanced",
                Report.status == "completed",
            )
        )
        .all()
    )

    if not reports:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No reports found ready for release",
        )

    released_count = 0
    released_ids = []
    skipped_ids = []

    for report in reports:
        if report.status == "completed":
            report.status = "released"  # type: ignore[assignment]
            released_count += 1
            released_ids.append(str(report.id))
        else:
            skipped_ids.append(str(report.id))

    db.commit()

    return {
        "message": f"Released {released_count} AI reports",
        "released_count": released_count,
        "released_ids": released_ids,
        "skipped_ids": skipped_ids,
    }


@router.post("/admin/{report_id}/retry-ai", response_model=AdminReportResponse)
async def admin_retry_ai_report(
    request: Request,
    report_id: str,
    background_tasks: BackgroundTasks,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> AdminReportResponse | Response:
    """Admin endpoint to retry generating a failed AI-enhanced report"""

    region = os.getenv("FLY_REGION")
    primary = os.getenv("FLY_PRIMARY_REGION", "iad")
    if region and primary and region != primary:
        return Response(status_code=409, headers={"fly-replay": f"region={primary}"})

    report = (
        db.query(Report)
        .filter(
            and_(
                Report.id == report_id,
                Report.report_type == "ai_enhanced",
                Report.status == "failed",
            )
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found or not in failed status",
        )

    report.status = "generating"  # type: ignore[assignment]
    report.file_path = None  # type: ignore[assignment]
    report.completed_at = None  # type: ignore[assignment]
    db.commit()

    background_tasks.add_task(generate_ai_report, str(report.id))

    return AdminReportResponse.model_validate(report)


@router.post("/admin/{report_id}/regenerate-pdf", response_model=None)
async def admin_regenerate_pdf_from_artifacts(
    request: Request,
    report_id: str,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, str] | Response:
    """Admin endpoint to regenerate PDF from existing AI artifacts without re-calling OpenAI"""

    region = os.getenv("FLY_REGION")
    primary = os.getenv("FLY_PRIMARY_REGION", "iad")
    if region and primary and region != primary:
        return Response(status_code=409, headers={"fly-replay": f"region={primary}"})

    report = (
        db.query(Report)
        .filter(
            and_(
                Report.id == report_id,
                Report.report_type == "ai_enhanced",
            )
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    from app.models.ai_artifacts import AISectionArtifact as AISectionArtifactModel
    from app.schemas.ai_artifacts import SectionAIArtifact

    section_artifacts_db = (
        db.query(AISectionArtifactModel)
        .filter(AISectionArtifactModel.report_id == report_id)
        .all()
    )

    if not section_artifacts_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No AI artifacts found for this report. Cannot regenerate PDF without artifacts.",
        )

    assessment = (
        db.query(Assessment).filter(Assessment.id == report.assessment_id).first()
    )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    responses = (
        db.query(AssessmentResponse)
        .filter(AssessmentResponse.assessment_id == assessment.id)
        .all()
    )

    structure = load_assessment_structure()
    if assessment.selected_section_ids:
        structure = filter_structure_by_sections(
            structure,
            list(assessment.selected_section_ids),  # type: ignore[arg-type]
        )

    scores = calculate_assessment_scores(responses, structure)

    ai_insights = {}
    for artifact_db in section_artifacts_db:
        ai_insights[str(artifact_db.section_id)] = SectionAIArtifact.model_validate(
            artifact_db.artifact_json
        )

    html_content = generate_ai_report_html(
        assessment, responses, scores, structure, ai_insights
    )

    filename = f"ai_report_{report_id}_{uuid.uuid4().hex[:8]}.pdf"
    storage_service = get_storage_service()

    pdf_bytes = HTML(string=html_content, url_fetcher=None).write_pdf()

    storage_location = storage_service.save(pdf_bytes, filename)

    if not storage_service.exists(storage_location):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save regenerated PDF",
        )

    report.file_path = storage_location  # type: ignore[assignment]
    report.completed_at = datetime.now(UTC)  # type: ignore[assignment]
    if report.status == "failed":
        report.status = "completed"  # type: ignore[assignment]
    db.commit()

    return {
        "status": "success",
        "message": "PDF regenerated from existing AI artifacts",
        "report_id": report_id,
        "file_path": storage_location,
    }


@router.get("/{report_id}/download", response_model=None)
async def download_report(
    request: Request,
    report_id: str,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> StreamingResponse | Response:
    """Download a completed report"""

    region = os.getenv("FLY_REGION")
    primary = os.getenv("FLY_PRIMARY_REGION", "iad")
    if region and primary and region != primary:
        return Response(status_code=409, headers={"fly-replay": f"region={primary}"})

    report = db.query(Report).join(Assessment).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    if not current_user.is_admin and report.assessment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    if report.status not in ["completed", "released"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not ready for download",
        )

    if current_user.is_admin:
        from app.api.admin import log_admin_action
        from app.models.user import User

        user = (
            db.query(User)
            .join(Assessment)
            .filter(Assessment.id == report.assessment_id)
            .first()
        )
        await log_admin_action(
            admin_email=current_user.email,
            action="download_report",
            target_user_id=str(user.id) if user else None,
            details={
                "report_id": str(report_id),
                "report_type": report.report_type,
                "user_email": user.email if user else "unknown",
            },
            db=db,
        )

    filename = f"security_assessment_report_{report.report_type}_{report_id}.pdf"
    storage_service = get_storage_service()

    file_exists = report.file_path and storage_service.exists(str(report.file_path))

    if not file_exists:
        fly_region = os.getenv("FLY_REGION", "unknown")
        fly_primary = os.getenv("FLY_PRIMARY_REGION", "unknown")
        storage_backend = getattr(settings, "STORAGE_BACKEND", "local")

        logger.warning(
            f"Report file not found for report_id {report_id} "
            f"(type={report.report_type}, file_path={report.file_path}, "
            f"region={fly_region}, primary={fly_primary}, backend={storage_backend})"
        )

        if report.report_type != "standard":
            logger.error(
                f"Cannot regenerate {report.report_type} report on-demand for report_id {report_id}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report file not found and cannot be regenerated",
            )

        try:
            assessment = (
                db.query(Assessment)
                .filter(Assessment.id == report.assessment_id)
                .first()
            )
            if not assessment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Assessment not found",
                )

            responses = (
                db.query(AssessmentResponse)
                .filter(AssessmentResponse.assessment_id == assessment.id)
                .all()
            )

            structure = load_assessment_structure()
            if assessment.selected_section_ids:
                structure = filter_structure_by_sections(
                    structure,
                    list(assessment.selected_section_ids),  # type: ignore[arg-type]
                )

            scores = calculate_assessment_scores(responses, structure)
            html_content = generate_report_html(
                assessment, responses, scores, structure
            )

            pdf_bytes = HTML(string=html_content, url_fetcher=None).write_pdf()

            new_filename = f"report_{report_id}_{uuid.uuid4().hex[:8]}.pdf"
            storage_location = storage_service.save(pdf_bytes, new_filename)
            report.file_path = storage_location  # type: ignore[assignment]
            db.commit()

            logger.info(
                f"Successfully regenerated report file for report_id {report_id}"
            )

            pdf_stream = io.BytesIO(pdf_bytes)
            headers = {
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "application/pdf",
            }
            return StreamingResponse(
                pdf_stream,
                media_type="application/pdf",
                headers=headers,
            )

        except Exception as e:
            logger.error(
                f"Failed to regenerate report for report_id {report_id}: {str(e)}",
                exc_info=True,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to regenerate report file",
            )

    try:
        file_handle = storage_service.open(str(report.file_path))
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report file not found"
        )

    if hasattr(file_handle, "seek"):
        file_handle.seek(0)

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "application/pdf",
    }

    background = None
    if hasattr(file_handle, "close"):
        background = BackgroundTask(file_handle.close)

    return StreamingResponse(
        file_handle,
        media_type="application/pdf",
        headers=headers,
        background=background,
    )


@router.get("/user/reports")
async def get_user_reports(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, list[dict[str, object]] | int]:
    """Get all reports for the current user with pagination"""

    query = (
        db.query(Report)
        .join(Assessment)
        .filter(Assessment.user_id == current_user.id)
        .options(joinedload(Report.assessment).joinedload(Assessment.user))
    )

    total = query.count()
    reports = query.order_by(desc(Report.requested_at)).offset(skip).limit(limit).all()

    from app.utils.pagination import paginate

    paginated = paginate(
        items=[UserReportResponse.model_validate(report) for report in reports],
        total=total,
        skip=skip,
        limit=limit,
    )

    return paginated.model_dump()


@router.get("/{report_id}/status", response_model=UserReportResponse)
async def get_report_status(
    request: Request,
    report_id: str,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserReportResponse:
    """Get the status of a specific report"""

    report = db.query(Report).join(Assessment).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    if not current_user.is_admin and report.assessment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    return UserReportResponse.model_validate(report)
