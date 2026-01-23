import io
from typing import Any
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_generate_standard_report(
    client: TestClient, auth_token: str, completed_assessment: Any
) -> None:
    with patch("app.api.reports.BackgroundTasks.add_task") as _mock_task:
        response = client.post(
            f"/api/reports/{completed_assessment.id}/generate",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["status"] == "generating"
        assert data["report_type"] == "standard"


def test_generate_report_assessment_not_found(
    client: TestClient, auth_token: str
) -> None:
    response = client.post(
        "/api/reports/nonexistent-id/generate",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 404


def test_generate_report_incomplete_assessment(
    client: TestClient, auth_token: str, test_assessment: Any
) -> None:
    response = client.post(
        f"/api/reports/{test_assessment.id}/generate",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 404
    assert "not found or not completed" in response.json()["detail"].lower()


def test_request_ai_report(
    client: TestClient, auth_token: str, completed_assessment: Any
) -> None:
    with patch("app.api.reports.BackgroundTasks.add_task") as _mock_task:
        response = client.post(
            f"/api/reports/{completed_assessment.id}/request-ai-report",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "assessment_id": str(completed_assessment.id),
                "message": "Please generate AI report",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["status"] == "pending"


def test_get_user_reports(
    client: TestClient, auth_token: str, test_report: Any
) -> None:
    response = client.get(
        "/api/reports/user/reports", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 1


def test_get_report_status(
    client: TestClient, auth_token: str, test_report: Any
) -> None:
    response = client.get(
        f"/api/reports/{test_report.id}/status",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "pending"


def test_get_report_status_not_found(client: TestClient, auth_token: str) -> None:
    response = client.get(
        "/api/reports/nonexistent-id/status",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 404


def test_download_report_not_ready(
    client: TestClient, auth_token: str, test_report: Any
) -> None:
    response = client.get(
        f"/api/reports/{test_report.id}/download",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 404
    assert "not ready" in response.json()["detail"].lower()


def test_admin_generate_ai_report(
    client: TestClient, admin_token: str, db_session: Session, completed_assessment: Any
) -> None:
    from app.models.assessment import Report

    ai_report = Report(
        assessment_id=completed_assessment.id,
        report_type="ai_enhanced",
        status="pending",
    )
    db_session.add(ai_report)
    db_session.commit()
    db_session.refresh(ai_report)

    with patch("app.api.reports.BackgroundTasks.add_task") as _mock_task:
        response = client.post(
            f"/api/reports/admin/{ai_report.id}/generate-ai",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "generating"


def test_admin_generate_ai_report_unauthorized(
    client: TestClient, auth_token: str, test_report: Any
) -> None:
    response = client.post(
        f"/api/reports/admin/{test_report.id}/generate-ai",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 403


def test_admin_release_report(
    client: TestClient, admin_token: str, test_report: Any, db_session: Session
) -> None:
    test_report.status = "completed"
    test_report.report_type = "ai_enhanced"
    db_session.commit()

    response = client.post(
        f"/api/reports/admin/{test_report.id}/release",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_duplicate_standard_report_prevention(
    client: TestClient, auth_token: str, completed_assessment: Any
) -> None:
    """Test that attempting to create duplicate standard reports returns existing report."""
    with patch("app.api.reports.BackgroundTasks.add_task") as _mock_task:
        response1 = client.post(
            f"/api/reports/{completed_assessment.id}/generate",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response1.status_code == 200
        data1 = response1.json()
        report_id_1 = data1["id"]

        response2 = client.post(
            f"/api/reports/{completed_assessment.id}/generate",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response2.status_code == 200
        data2 = response2.json()
        report_id_2 = data2["id"]

        assert report_id_1 == report_id_2
        assert data2["report_type"] == "standard"


def test_duplicate_ai_report_prevention(
    client: TestClient, auth_token: str, completed_assessment: Any
) -> None:
    """Test that attempting to create duplicate AI reports returns existing report."""
    response1 = client.post(
        f"/api/reports/{completed_assessment.id}/request-ai-report",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"message": "First request"},
    )
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["status"] == "pending"

    response2 = client.post(
        f"/api/reports/{completed_assessment.id}/request-ai-report",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"message": "Second request"},
    )
    assert response2.status_code == 200
    data2 = response2.json()
    assert "already requested" in data2["message"].lower()
    assert data2["status"] == "pending"


def test_concurrent_report_generation_race_condition(
    client: TestClient, auth_token: str, completed_assessment: Any, db_session: Session
) -> None:
    """Test that concurrent report generation attempts don't create duplicates."""
    from app.models.assessment import Report

    with patch("app.api.reports.BackgroundTasks.add_task") as _mock_task:
        responses = []
        for _ in range(3):
            response = client.post(
                f"/api/reports/{completed_assessment.id}/generate",
                headers={"Authorization": f"Bearer {auth_token}"},
            )
            responses.append(response)

        for response in responses:
            assert response.status_code == 200

        reports = (
            db_session.query(Report)
            .filter(
                Report.assessment_id == completed_assessment.id,
                Report.report_type == "standard",
            )
            .all()
        )
        assert len(reports) == 1


def test_different_report_types_allowed(
    client: TestClient, auth_token: str, completed_assessment: Any, db_session: Session
) -> None:
    """Test that different report types (standard vs AI) can coexist for same assessment."""
    from app.models.assessment import Report

    with patch("app.api.reports.BackgroundTasks.add_task") as _mock_task:
        response1 = client.post(
            f"/api/reports/{completed_assessment.id}/generate",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response1.status_code == 200

        response2 = client.post(
            f"/api/reports/{completed_assessment.id}/request-ai-report",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"message": "AI report request"},
        )
        assert response2.status_code == 200

        reports = (
            db_session.query(Report)
            .filter(Report.assessment_id == completed_assessment.id)
            .all()
        )
        assert len(reports) == 2
        report_types = {r.report_type for r in reports}
        assert report_types == {"standard", "ai_enhanced"}


def test_user_reports_ordered_by_requested_at(
    client: TestClient, auth_token: str, completed_assessment: Any, db_session: Session
) -> None:
    """Test that user reports are returned in descending order by requested_at."""
    from datetime import UTC, datetime, timedelta

    from app.models.assessment import Report

    base_time = datetime.now(UTC)
    reports_data: list[dict[str, Any]] = [
        {"offset_minutes": -60, "type": "standard"},  # 1 hour ago
        {"offset_minutes": -30, "type": "ai_enhanced"},  # 30 minutes ago
    ]

    for data in reports_data:
        report = Report(
            assessment_id=completed_assessment.id,
            report_type=str(data["type"]),
            status="completed",
            requested_at=base_time + timedelta(minutes=int(data["offset_minutes"])),
        )
        db_session.add(report)
    db_session.commit()

    response = client.get(
        "/api/reports/user/reports", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    items = data["items"]

    if len(items) >= 2:
        for i in range(len(items) - 1):
            current_time = datetime.fromisoformat(
                items[i]["requested_at"].replace("Z", "+00:00")
            )
            next_time = datetime.fromisoformat(
                items[i + 1]["requested_at"].replace("Z", "+00:00")
            )
            assert current_time >= next_time, (
                "Reports should be ordered by requested_at DESC"
            )


def test_admin_retry_failed_standard_report(
    client: TestClient, admin_token: str, completed_assessment: Any, db_session: Session
) -> None:
    """Test that admin can retry a failed standard report."""
    from app.models.assessment import Report

    failed_report = Report(
        assessment_id=completed_assessment.id,
        report_type="standard",
        status="failed",
    )
    db_session.add(failed_report)
    db_session.commit()
    db_session.refresh(failed_report)

    with patch("app.api.reports.BackgroundTasks.add_task") as _mock_task:
        response = client.post(
            f"/api/reports/admin/{failed_report.id}/retry-standard",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "generating"
        assert data["report_type"] == "standard"


def test_admin_retry_non_failed_report_fails(
    client: TestClient, admin_token: str, completed_assessment: Any, db_session: Session
) -> None:
    """Test that admin cannot retry a report that hasn't failed."""
    from app.models.assessment import Report

    completed_report = Report(
        assessment_id=completed_assessment.id,
        report_type="standard",
        status="completed",
    )
    db_session.add(completed_report)
    db_session.commit()
    db_session.refresh(completed_report)

    response = client.post(
        f"/api/reports/admin/{completed_report.id}/retry-standard",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_user_generate_report_excludes_file_path(
    client: TestClient, auth_token: str, completed_assessment: Any
) -> None:
    """Test that user generate report endpoint excludes file_path from response."""
    with patch("app.api.reports.BackgroundTasks.add_task") as _mock_task:
        response = client.post(
            f"/api/reports/{completed_assessment.id}/generate",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "file_path" not in data
        assert "id" in data
        assert "status" in data


def test_user_get_reports_excludes_file_path(
    client: TestClient, auth_token: str, test_report: Any
) -> None:
    """Test that user get reports endpoint excludes file_path from response."""
    response = client.get(
        "/api/reports/user/reports", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    for item in data["items"]:
        assert "file_path" not in item
        assert "id" in item
        assert "status" in item


def test_user_get_report_status_excludes_file_path(
    client: TestClient, auth_token: str, test_report: Any
) -> None:
    """Test that user get report status endpoint excludes file_path from response."""
    response = client.get(
        f"/api/reports/{test_report.id}/status",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "file_path" not in data
    assert "id" in data
    assert "status" in data


def test_admin_generate_ai_report_includes_file_path(
    client: TestClient, admin_token: str, db_session: Session, completed_assessment: Any
) -> None:
    """Test that admin generate AI report endpoint includes file_path in response."""
    from app.models.assessment import Report

    ai_report = Report(
        assessment_id=completed_assessment.id,
        report_type="ai_enhanced",
        status="pending",
    )
    db_session.add(ai_report)
    db_session.commit()
    db_session.refresh(ai_report)

    with patch("app.api.reports.BackgroundTasks.add_task") as _mock_task:
        response = client.post(
            f"/api/reports/admin/{ai_report.id}/generate-ai",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "file_path" in data
        assert "id" in data
        assert "status" in data


def test_admin_retry_standard_report_includes_file_path(
    client: TestClient, admin_token: str, completed_assessment: Any, db_session: Session
) -> None:
    """Test that admin retry standard report endpoint includes file_path in response."""
    from app.models.assessment import Report

    failed_report = Report(
        assessment_id=completed_assessment.id,
        report_type="standard",
        status="failed",
    )
    db_session.add(failed_report)
    db_session.commit()
    db_session.refresh(failed_report)

    with patch("app.api.reports.BackgroundTasks.add_task") as _mock_task:
        response = client.post(
            f"/api/reports/admin/{failed_report.id}/retry-standard",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "file_path" in data
        assert "id" in data
        assert "status" in data


def test_reports_admin_overview_flow(
    client: TestClient,
    admin_token: str,
    test_user: Any,
    completed_assessment: Any,
    db_session: Session,
) -> None:
    """Exercise key admin overview endpoints to guard the reporting workflow."""

    from datetime import UTC, datetime, timedelta

    from app.models.assessment import Assessment, Report
    from app.models.user import User

    headers = {"Authorization": f"Bearer {admin_token}"}

    stale_assessment = Assessment(
        user_id=test_user.id,
        status="in_progress",
        started_at=datetime.now(UTC) - timedelta(days=10),
        last_saved_at=datetime.now(UTC) - timedelta(days=8),
        expires_at=datetime.now(UTC) + timedelta(hours=12),
        progress_percentage=42.0,
    )

    pending_ai_report = Report(
        assessment_id=completed_assessment.id,
        report_type="ai_enhanced",
        status="pending",
    )

    completed_report = Report(
        assessment_id=completed_assessment.id,
        report_type="standard",
        status="completed",
        file_path="/tmp/report.pdf",
    )

    consultation_assessment = Assessment(
        user_id=test_user.id,
        status="completed",
        consultation_interest=True,
        consultation_details="Need follow-up",
        started_at=datetime.now(UTC) - timedelta(days=2),
        completed_at=datetime.now(UTC) - timedelta(days=1),
    )

    extra_user = User(
        email="report-temp@example.com",
        full_name="Report Temp",
        company_name="Coverage Inc",
        password_hash=test_user.password_hash,
        is_active=True,
    )

    db_session.add_all(
        [
            stale_assessment,
            pending_ai_report,
            completed_report,
            consultation_assessment,
            extra_user,
        ]
    )
    db_session.commit()

    users_response = client.get("/api/admin/users", headers=headers)
    assert users_response.status_code == 200
    assert users_response.json()["total"] >= 1

    user_detail = client.get(f"/api/admin/users/{test_user.id}", headers=headers)
    assert user_detail.status_code == 200
    assert user_detail.json()["email"] == test_user.email

    assessments_response = client.get(
        f"/api/admin/users/{test_user.id}/assessments", headers=headers
    )
    assert assessments_response.status_code == 200
    assert isinstance(assessments_response.json(), list)

    all_assessments = client.get("/api/admin/assessments", headers=headers)
    assert all_assessments.status_code == 200
    assert all_assessments.json()["total"] >= 1

    reports_response = client.get("/api/admin/reports", headers=headers)
    assert reports_response.status_code == 200
    assert reports_response.json()["total"] >= 1

    dashboard_stats = client.get("/api/admin/dashboard/stats", headers=headers)
    assert dashboard_stats.status_code == 200
    stats_payload = dashboard_stats.json()
    assert "active_assessments" in stats_payload
    assert "average_completion_hours" in stats_payload

    alerts_response = client.get("/api/admin/alerts", headers=headers)
    assert alerts_response.status_code == 200
    assert "alerts" in alerts_response.json()

    progress_summary = client.get("/api/admin/users-progress-summary", headers=headers)
    assert progress_summary.status_code == 200

    consultations = client.get("/api/admin/consultations", headers=headers)
    assert consultations.status_code == 200

    filtered_reports = client.get("/api/admin/reports?status=pending", headers=headers)
    assert filtered_reports.status_code == 200

    password_reset = client.post(
        f"/api/admin/users/{test_user.id}/reset-password",
        headers=headers,
        json={"new_password": "ResetPass123!"},
    )
    assert password_reset.status_code == 200

    bulk_update = client.post(
        "/api/admin/users/bulk-update-status",
        headers=headers,
        json={"user_ids": [str(test_user.id)], "is_active": True},
    )
    assert bulk_update.status_code == 200

    bulk_delete = client.post(
        "/api/admin/users/bulk-delete",
        headers=headers,
        json={"user_ids": [str(extra_user.id)]},
    )
    assert bulk_delete.status_code == 200


def test_reports_user_health_flow(
    client: TestClient,
    auth_token: str,
    test_assessment: Any,
    test_assessment_response: Any,
) -> None:
    """Run user, auth, and health endpoints to maintain coverage for report pipelines."""

    headers = {"Authorization": f"Bearer {auth_token}"}

    structure_response = client.get("/api/assessment/structure", headers=headers)
    assert structure_response.status_code == 200

    current_assessment = client.get("/api/assessment/current", headers=headers)
    assert current_assessment.status_code in (200, 404)

    responses_response = client.get(
        f"/api/assessment/{test_assessment.id}/responses", headers=headers
    )
    assert responses_response.status_code == 200

    user_info = client.get("/api/auth/me", headers=headers)
    assert user_info.status_code == 200
    assert user_info.json()["email"]

    root_response = client.get("/")
    assert root_response.status_code == 200

    health_response = client.get("/health")
    assert health_response.status_code in (200, 503)

    liveness_response = client.get("/health/live")
    assert liveness_response.status_code == 200

    readiness_response = client.get("/health/ready")
    assert readiness_response.status_code in (200, 503)


def test_download_report_serves_existing_file(
    client: TestClient,
    auth_token: str,
    db_session: Session,
    completed_assessment: Any,
    monkeypatch: Any,
) -> None:
    from app.models.assessment import Report

    report = Report(
        assessment_id=completed_assessment.id,
        report_type="standard",
        status="completed",
        file_path="reports/test_report.pdf",
    )
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    fake_pdf_bytes = b"%PDF-1.4 FAKE PDF CONTENT"

    mock_storage = MagicMock()
    mock_storage.exists.return_value = True
    mock_storage.open.return_value = io.BytesIO(fake_pdf_bytes)

    monkeypatch.setattr("app.api.reports.get_storage_service", lambda: mock_storage)

    response = client.get(
        f"/api/reports/{report.id}/download",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers.get("content-disposition", "").lower()
    assert len(response.content) > 0


def test_download_report_regenerates_when_file_missing(
    client: TestClient,
    auth_token: str,
    db_session: Session,
    completed_assessment: Any,
    monkeypatch: Any,
) -> None:
    from app.models.assessment import AssessmentResponse, Report

    assessment_response = AssessmentResponse(
        assessment_id=completed_assessment.id,
        section_id="access-control",
        question_id="ac-1",
        answer_value="yes",
    )
    db_session.add(assessment_response)
    db_session.commit()

    report = Report(
        assessment_id=completed_assessment.id,
        report_type="standard",
        status="completed",
        file_path=None,
    )
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    fake_pdf_bytes = b"%PDF-1.4 REGENERATED PDF"
    saved_path = None

    def mock_save(pdf_bytes: bytes, filename: str) -> str:
        nonlocal saved_path
        saved_path = f"reports/{filename}"
        return saved_path

    mock_storage = MagicMock()
    mock_storage.exists.return_value = False
    mock_storage.save.side_effect = mock_save

    monkeypatch.setattr("app.api.reports.get_storage_service", lambda: mock_storage)
    monkeypatch.setattr(
        "app.api.reports.HTML",
        lambda string, url_fetcher=None: MagicMock(write_pdf=lambda: fake_pdf_bytes),
    )
    monkeypatch.setattr(
        "app.api.reports.generate_report_html", lambda *args, **kwargs: "<html></html>"
    )
    monkeypatch.setattr(
        "app.api.reports.calculate_assessment_scores", lambda *args, **kwargs: {}
    )
    monkeypatch.setattr(
        "app.api.reports.load_assessment_structure", lambda: {"sections": []}
    )

    response = client.get(
        f"/api/reports/{report.id}/download",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 0

    db_session.refresh(report)
    assert report.file_path is not None
    assert report.file_path == saved_path


def test_download_report_ai_report_fails_when_file_missing(
    client: TestClient,
    auth_token: str,
    db_session: Session,
    completed_assessment: Any,
    monkeypatch: Any,
) -> None:
    from app.models.assessment import Report

    report = Report(
        assessment_id=completed_assessment.id,
        report_type="ai_enhanced",
        status="completed",
        file_path=None,
    )
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    mock_storage = MagicMock()
    mock_storage.exists.return_value = False

    monkeypatch.setattr("app.api.reports.get_storage_service", lambda: mock_storage)

    response = client.get(
        f"/api/reports/{report.id}/download",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 404
    assert "cannot be regenerated" in response.json()["detail"].lower()


def test_download_report_uses_filtered_structure_for_customized_assessment(
    client: TestClient,
    auth_token: str,
    db_session: Session,
    test_user: Any,
    monkeypatch: Any,
) -> None:
    from datetime import UTC, datetime, timedelta

    from app.models.assessment import Assessment, AssessmentResponse, Report

    customized_assessment = Assessment(
        user_id=test_user.id,
        status="completed",
        started_at=datetime.now(UTC) - timedelta(days=1),
        completed_at=datetime.now(UTC),
        expires_at=datetime.now(UTC) + timedelta(days=14),
        progress_percentage=100.0,
        selected_section_ids=["access-control", "data-protection"],
    )
    db_session.add(customized_assessment)
    db_session.commit()
    db_session.refresh(customized_assessment)

    assessment_response = AssessmentResponse(
        assessment_id=customized_assessment.id,
        section_id="access-control",
        question_id="ac-1",
        answer_value="yes",
    )
    db_session.add(assessment_response)
    db_session.commit()

    report = Report(
        assessment_id=customized_assessment.id,
        report_type="standard",
        status="completed",
        file_path=None,
    )
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    fake_pdf_bytes = b"%PDF-1.4 FILTERED PDF"
    filter_called_with = None

    def mock_filter(structure: Any, selected_ids: Any) -> Any:
        nonlocal filter_called_with
        filter_called_with = selected_ids
        return structure

    mock_storage = MagicMock()
    mock_storage.exists.return_value = False
    mock_storage.save.return_value = "reports/filtered.pdf"

    monkeypatch.setattr("app.api.reports.get_storage_service", lambda: mock_storage)
    monkeypatch.setattr(
        "app.api.reports.HTML",
        lambda string, url_fetcher=None: MagicMock(write_pdf=lambda: fake_pdf_bytes),
    )
    monkeypatch.setattr(
        "app.api.reports.generate_report_html", lambda *args, **kwargs: "<html></html>"
    )
    monkeypatch.setattr(
        "app.api.reports.calculate_assessment_scores", lambda *args, **kwargs: {}
    )
    monkeypatch.setattr(
        "app.api.reports.load_assessment_structure", lambda: {"sections": []}
    )
    monkeypatch.setattr("app.api.reports.filter_structure_by_sections", mock_filter)

    response = client.get(
        f"/api/reports/{report.id}/download",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    assert filter_called_with == ["access-control", "data-protection"]
