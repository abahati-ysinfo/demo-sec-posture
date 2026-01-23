from datetime import UTC, datetime, timedelta
from typing import Any, cast

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import and_, desc, func
from sqlalchemy.orm import Session, joinedload

from app.api.auth import get_current_admin_user
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.assessment import AdminAuditLog, Assessment, AssessmentResponse, Report
from app.models.user import User
from app.schemas.assessment import AssessmentResponse as AssessmentResponseSchema
from app.schemas.report import AdminReportResponse
from app.schemas.user import (
    BulkDeleteUsersRequest,
    BulkUpdateUserStatusRequest,
    CurrentUserResponse,
    UserResponse,
)
from app.services.cache import cache_service
from app.utils.datetime_utils import to_utc_aware
from app.utils.pagination import PaginatedResponse

router = APIRouter()


@router.get("/users")
async def get_all_users(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: str | None = Query(None),
    sort_by: str = Query(
        "created_at", regex="^(full_name|email|company_name|created_at|is_active)$"
    ),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> PaginatedResponse[UserResponse]:
    """Get all users with pagination, search, and sorting"""

    query = db.query(User)

    if search:
        search_param = f"%{search}%"
        query = query.filter(
            User.full_name.ilike(search_param)
            | User.email.ilike(search_param)
            | User.company_name.ilike(search_param)
        )

    sort_column = getattr(User, sort_by)
    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(sort_column)

    total = query.count()
    users = query.offset(skip).limit(limit).all()

    await log_admin_action(
        admin_email=current_admin.email,
        action="view_users",
        details={"search": search, "count": len(users)},
        db=db,
    )

    from app.utils.pagination import paginate

    return paginate(
        items=[UserResponse.model_validate(user) for user in users],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    request: Request,
    user_id: str,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> UserResponse:
    """Get a specific user by ID"""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await log_admin_action(
        admin_email=current_admin.email,
        action="view_user",
        target_user_id=user_id,
        db=db,
    )

    return UserResponse.model_validate(user)


@router.get(
    "/users/{user_id}/assessments", response_model=list[AssessmentResponseSchema]
)
async def get_user_assessments(
    request: Request,
    user_id: str,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> list[AssessmentResponseSchema]:
    """Get all assessments for a specific user"""

    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        assessments = (
            db.query(Assessment)
            .filter(Assessment.user_id == user_id)
            .order_by(desc(Assessment.created_at))
            .all()
        )

        await log_admin_action(
            admin_email=current_admin.email,
            action="view_user_assessments",
            target_user_id=user_id,
            details={"assessment_count": len(assessments)},
            db=db,
        )

        return [
            AssessmentResponseSchema.model_validate(assessment)
            for assessment in assessments
        ]

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_user_assessments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user assessments",
        )


@router.get("/assessments")
async def get_all_assessments(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: str | None = Query(None),
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> PaginatedResponse[AssessmentResponseSchema]:
    """Get all assessments with filtering"""

    try:
        query = db.query(Assessment).options(joinedload(Assessment.user)).join(User)

        if status_filter:
            query = query.filter(Assessment.status == status_filter)

        total = query.count()
        assessments = (
            query.order_by(desc(Assessment.created_at)).offset(skip).limit(limit).all()
        )

        await log_admin_action(
            admin_email=current_admin.email,
            action="view_assessments",
            details={"status_filter": status_filter, "count": len(assessments)},
            db=db,
        )

        from app.utils.pagination import paginate

        return paginate(
            items=[
                AssessmentResponseSchema.model_validate(assessment)
                for assessment in assessments
            ],
            total=total,
            skip=skip,
            limit=limit,
        )

    except Exception as e:
        print(f"Error in get_all_assessments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve assessments",
        )


@router.get("/dashboard/stats")
async def get_dashboard_stats(
    request: Request,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Get dashboard statistics"""

    CACHE_KEY = "dashboard:stats"
    CACHE_TTL = 300

    cached_stats = cache_service.get(CACHE_KEY)
    if cached_stats:
        return dict(cached_stats)

    try:
        total_users = db.query(func.count(User.id)).scalar()

        active_assessments = (
            db.query(func.count(Assessment.id))
            .filter(Assessment.status == "in_progress")
            .scalar()
        )

        completed_assessments = (
            db.query(func.count(Assessment.id))
            .filter(Assessment.status == "completed")
            .scalar()
        )

        expired_assessments = (
            db.query(func.count(Assessment.id))
            .filter(Assessment.status == "expired")
            .scalar()
        )

        week_ago = datetime.now(UTC) - timedelta(days=7)
        new_users_this_week = (
            db.query(func.count(User.id)).filter(User.created_at >= week_ago).scalar()
        )

        seven_days_ago = datetime.now(UTC) - timedelta(days=7)
        stuck_assessments = (
            db.query(func.count(Assessment.id))
            .filter(
                and_(
                    Assessment.status == "in_progress",
                    Assessment.last_saved_at < seven_days_ago,
                )
            )
            .scalar()
        )

        avg_completion_time = (
            db.query(
                func.avg(
                    func.extract(
                        "epoch", Assessment.completed_at - Assessment.started_at
                    )
                    / 3600
                )
            )
            .filter(Assessment.status == "completed")
            .scalar()
        )

        stats = {
            "total_users": total_users or 0,
            "active_assessments": active_assessments or 0,
            "completed_assessments": completed_assessments or 0,
            "expired_assessments": expired_assessments or 0,
            "new_users_this_week": new_users_this_week or 0,
            "stuck_assessments": stuck_assessments or 0,
            "average_completion_hours": round(avg_completion_time or 0, 2),
        }

        cache_service.set(CACHE_KEY, stats, ttl=CACHE_TTL)

        await log_admin_action(
            admin_email=current_admin.email,
            action="view_dashboard",
            details=stats,
            db=db,
        )

        return stats

    except Exception as e:
        print(f"Error in get_dashboard_stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve dashboard statistics",
        )


@router.get("/users-progress-summary")
async def get_users_progress_summary(
    request: Request,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Get detailed progress summary for all users"""

    try:
        users_with_progress = db.query(User).options(joinedload(User.assessments)).all()

        summary = []
        for user in users_with_progress:
            assessment = None
            if user.assessments:
                assessment = max(user.assessments, key=lambda a: a.created_at)

            last_activity = assessment.last_saved_at if assessment else user.created_at
            aware_activity = to_utc_aware(cast(datetime | None, last_activity))
            days_since = (
                (datetime.now(UTC) - aware_activity).days
                if aware_activity is not None
                else 0
            )

            user_data = {
                "user_id": str(user.id),
                "full_name": user.full_name,
                "email": user.email,
                "company_name": user.company_name,
                "assessment_status": assessment.status if assessment else "not_started",
                "progress_percentage": float(assessment.progress_percentage)
                if assessment
                else 0.0,
                "last_activity": last_activity,
                "days_since_activity": days_since,
            }
            summary.append(user_data)

        await log_admin_action(
            admin_email=current_admin.email,
            action="view_users_progress",
            details={"user_count": len(summary)},
            db=db,
        )

        return {"users_progress": summary}

    except Exception as e:
        print(f"Error in get_users_progress_summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users progress summary",
        )


@router.get("/reports")
async def get_all_reports(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    report_type: str | None = Query(None),
    status_filter: str | None = Query(None),
    search: str | None = Query(None),
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> PaginatedResponse[AdminReportResponse]:
    """Get all reports with filtering and search"""

    try:
        query = (
            db.query(Report)
            .join(Assessment)
            .join(User)
            .options(joinedload(Report.assessment).joinedload(Assessment.user))
        )

        if report_type:
            query = query.filter(Report.report_type == report_type)

        if status_filter:
            query = query.filter(Report.status == status_filter)

        if search:
            search_param = f"%{search}%"
            query = query.filter(
                User.email.ilike(search_param) | User.company_name.ilike(search_param)
            )

        total = query.count()
        reports = (
            query.order_by(desc(Report.requested_at)).offset(skip).limit(limit).all()
        )

        await log_admin_action(
            admin_email=current_admin.email,
            action="view_reports",
            details={
                "type_filter": report_type,
                "status_filter": status_filter,
                "search": search,
                "count": len(reports),
            },
            db=db,
        )

        from app.utils.pagination import paginate

        return paginate(
            items=[AdminReportResponse.model_validate(report) for report in reports],
            total=total,
            skip=skip,
            limit=limit,
        )

    except Exception as e:
        print(f"Error in get_all_reports: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve reports",
        )


@router.get("/alerts")
async def get_alerts(
    request: Request,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Get system alerts for admin dashboard"""

    try:
        alerts = []

        seven_days_ago = datetime.now(UTC) - timedelta(days=7)
        stuck_assessments = (
            db.query(Assessment)
            .filter(
                and_(
                    Assessment.status == "in_progress",
                    Assessment.last_saved_at < seven_days_ago,
                )
            )
            .count()
        )

        if stuck_assessments > 0:
            alerts.append(
                {
                    "type": "warning",
                    "title": "Stuck Assessments",
                    "message": f"{stuck_assessments} assessments haven't been updated in 7+ days",
                    "count": stuck_assessments,
                }
            )

        tomorrow = datetime.now(UTC) + timedelta(days=1)
        expiring_soon = (
            db.query(Assessment)
            .filter(
                and_(
                    Assessment.status == "in_progress",
                    Assessment.expires_at <= tomorrow,
                )
            )
            .count()
        )

        if expiring_soon > 0:
            alerts.append(
                {
                    "type": "info",
                    "title": "Expiring Soon",
                    "message": f"{expiring_soon} assessments expire within 24 hours",
                    "count": expiring_soon,
                }
            )

        pending_ai_reports = (
            db.query(Report)
            .filter(
                and_(Report.report_type == "ai_enhanced", Report.status == "pending")
            )
            .count()
        )

        if pending_ai_reports > 0:
            alerts.append(
                {
                    "type": "info",
                    "title": "Pending AI Reports",
                    "message": f"{pending_ai_reports} AI reports are pending generation",
                    "count": pending_ai_reports,
                }
            )

        return {"alerts": alerts}

    except Exception as e:
        print(f"Error in get_alerts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve alerts",
        )


@router.delete("/users/{user_id}")
async def delete_user(
    request: Request,
    user_id: str,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Delete a user and all associated data"""

    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if user.is_protected:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot delete protected admin account",
            )

        assessments = db.query(Assessment).filter(Assessment.user_id == user_id).all()
        for assessment in assessments:
            db.query(AssessmentResponse).filter(
                AssessmentResponse.assessment_id == assessment.id
            ).delete()
            db.query(Report).filter(Report.assessment_id == assessment.id).delete()
        db.query(Assessment).filter(Assessment.user_id == user_id).delete()

        db.delete(user)
        db.commit()

        await log_admin_action(
            admin_email=current_admin.email,
            action="delete_user",
            target_user_id=user_id,
            db=db,
        )

        return {"message": "User deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error in delete_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user",
        )


@router.post("/users/{user_id}/reset-password")
async def reset_user_password(
    request: Request,
    user_id: str,
    request_data: dict[str, Any],
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Reset a user's password"""

    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        new_password = request_data.get("new_password")
        if not new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password is required",
            )

        user.password_hash = get_password_hash(new_password)  # type: ignore[assignment]
        db.commit()

        await log_admin_action(
            admin_email=current_admin.email,
            action="reset_password",
            target_user_id=user_id,
            db=db,
        )

        return {"message": "Password reset successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error in reset_user_password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password",
        )


@router.get("/consultations")
async def get_consultation_requests(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> PaginatedResponse[dict[str, Any]]:
    """Get all consultation requests from users"""

    try:
        query = (
            db.query(Assessment)
            .join(User)
            .filter(Assessment.consultation_interest.is_(True))
            .order_by(desc(Assessment.updated_at))
        )

        total = query.count()
        consultations = query.offset(skip).limit(limit).all()

        consultation_data = []
        for assessment in consultations:
            consultation_data.append(
                {
                    "id": assessment.id,
                    "user_name": assessment.user.full_name,
                    "user_email": assessment.user.email,
                    "company_name": assessment.user.company_name,
                    "consultation_details": assessment.consultation_details,
                    "assessment_completed_at": assessment.completed_at,
                    "created_at": assessment.created_at,
                }
            )

        from app.utils.pagination import paginate

        return paginate(items=consultation_data, total=total, skip=skip, limit=limit)

    except Exception as e:
        print(f"Error in get_consultation_requests: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve consultation requests",
        )


@router.post("/users/bulk-update-status")
async def bulk_update_user_status(
    request: Request,
    request_data: BulkUpdateUserStatusRequest,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Bulk activate/deactivate users"""

    try:
        updated_count = (
            db.query(User)
            .filter(User.id.in_(request_data.user_ids))
            .update({"is_active": request_data.is_active}, synchronize_session=False)
        )
        db.commit()

        await log_admin_action(
            admin_email=current_admin.email,
            action="bulk_update_status",
            details={
                "user_ids": request_data.user_ids,
                "is_active": request_data.is_active,
                "updated_count": updated_count,
            },
            db=db,
        )

        return {
            "message": f"Updated {updated_count} users",
            "updated_count": updated_count,
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error in bulk_update_user_status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user status",
        )


@router.post("/users/bulk-delete")
async def bulk_delete_users(
    request: Request,
    request_data: BulkDeleteUsersRequest,
    current_admin: CurrentUserResponse = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Bulk delete users and all associated data with optimized performance"""

    try:
        if not request_data.user_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No user IDs provided",
            )

        existing_users = (
            db.query(User.id, User.is_protected, User.email)
            .filter(User.id.in_(request_data.user_ids))
            .all()
        )
        existing_user_ids = {user.id for user in existing_users}

        if not existing_user_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No valid users found to delete",
            )

        invalid_ids = set(request_data.user_ids) - existing_user_ids

        protected_users = [
            {"id": user.id, "email": user.email}
            for user in existing_users
            if user.is_protected
        ]
        protected_user_ids = {user["id"] for user in protected_users}

        deletable_user_ids = existing_user_ids - protected_user_ids

        if not deletable_user_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot delete protected admin accounts",
            )

        deleted_count = (
            db.query(User)
            .filter(User.id.in_(deletable_user_ids))
            .delete(synchronize_session=False)
        )
        db.commit()

        await log_admin_action(
            admin_email=current_admin.email,
            action="bulk_delete_users",
            details={
                "requested_user_ids": request_data.user_ids,
                "deleted_count": deleted_count,
                "invalid_ids": list(invalid_ids) if invalid_ids else [],
                "protected_users": protected_users,
            },
            db=db,
        )

        response_message = f"Successfully deleted {deleted_count} user{'s' if deleted_count != 1 else ''}"
        if protected_users:
            response_message += f" ({len(protected_users)} protected account{'s' if len(protected_users) != 1 else ''} skipped)"
        if invalid_ids:
            response_message += f" ({len(invalid_ids)} invalid ID{'s' if len(invalid_ids) != 1 else ''} skipped)"

        return {
            "message": response_message,
            "deleted_count": deleted_count,
            "invalid_ids": list(invalid_ids) if invalid_ids else [],
            "protected_users": protected_users,
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Bulk delete error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete users: {str(e)}",
        )


async def log_admin_action(
    admin_email: str,
    action: str,
    target_user_id: str | None = None,
    details: dict[str, Any] | None = None,
    db: Session | None = None,
) -> None:
    """Log admin actions for audit trail"""

    if not db:
        return

    try:
        audit_log = AdminAuditLog(
            admin_email=admin_email,
            action=action,
            target_user_id=target_user_id,
            details=details or {},
        )

        db.add(audit_log)
        db.commit()
    except Exception as e:
        print(f"Error logging admin action: {e}")
        db.rollback()
