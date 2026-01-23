"""
Comprehensive permission boundary tests for authorization checks.

Tests cover:
- Cross-user access attempts (User A cannot access User B's data)
- Regular user cannot access admin endpoints
- Admin can access all user data
- Unauthenticated requests are rejected
- User cannot modify other user's data
"""

from typing import Any

from fastapi.testclient import TestClient


def test_user_cannot_access_other_user_assessment(
    client: TestClient, auth_token: str, test_user2_token: str, db_session: Any
) -> None:
    """Test that User A cannot access User B's assessment"""
    response = client.post(
        "/api/assessment/start", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assessment_id = response.json()["id"]

    response = client.get(
        f"/api/assessment/{assessment_id}/responses",
        headers={"Authorization": f"Bearer {test_user2_token}"},
    )
    assert response.status_code in [403, 404]


def test_user_cannot_access_other_user_report(
    client: TestClient,
    auth_token: str,
    test_user2_token: str,
    completed_assessment: Any,
    test_report: Any,
) -> None:
    """Test that User A cannot download User B's report"""
    response = client.get(
        f"/api/reports/{test_report.id}/download",
        headers={"Authorization": f"Bearer {test_user2_token}"},
    )
    assert response.status_code == 403


def test_user_cannot_access_admin_endpoints(
    client: TestClient, auth_token: str
) -> None:
    """Test that regular user cannot access admin endpoints"""
    admin_endpoints = [
        "/api/admin/users",
        "/api/admin/assessments",
        "/api/admin/dashboard/stats",
        "/api/admin/reports",
        "/api/admin/users-progress-summary",
    ]

    for endpoint in admin_endpoints:
        response = client.get(
            endpoint, headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 403, (
            f"Endpoint {endpoint} should return 403 for regular user"
        )


def test_admin_can_access_all_user_data(
    client: TestClient, admin_token: str, auth_token: str, test_assessment: Any
) -> None:
    """Test that admin can access all user assessments and reports"""
    response = client.get(
        "/api/admin/assessments", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assessments = response.json()["items"]
    assert any(a["id"] == str(test_assessment.id) for a in assessments)


def test_unauthenticated_cannot_access_protected_endpoints(client: TestClient) -> None:
    """Test that unauthenticated requests are rejected"""
    protected_endpoints = [
        ("/api/assessment/current", "GET"),
        ("/api/assessment/start", "POST"),
        ("/api/reports/user/reports", "GET"),
        ("/api/admin/users", "GET"),
    ]

    for endpoint, method in protected_endpoints:
        if method == "GET":
            response = client.get(endpoint)
        else:
            response = client.post(endpoint)
        assert response.status_code == 401 or response.status_code == 403, (
            f"{method} {endpoint} should return 401 or 403 for unauthenticated request"
        )


def test_user_cannot_modify_other_user_assessment(
    client: TestClient, auth_token: str, test_user2_token: str, db_session: Any
) -> None:
    """Test that User A cannot save progress to User B's assessment"""
    response = client.post(
        "/api/assessment/start", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assessment_id = response.json()["id"]

    response = client.post(
        f"/api/assessment/{assessment_id}/save-progress",
        headers={"Authorization": f"Bearer {test_user2_token}"},
        json={"responses": []},
    )
    assert response.status_code in [403, 422]


def test_user_cannot_complete_other_user_assessment(
    client: TestClient, auth_token: str, test_user2_token: str, db_session: Any
) -> None:
    """Test that User A cannot complete User B's assessment"""
    response = client.post(
        "/api/assessment/start", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assessment_id = response.json()["id"]

    response = client.post(
        f"/api/assessment/{assessment_id}/complete",
        headers={"Authorization": f"Bearer {test_user2_token}"},
        json={"consultation_interest": False},
    )
    assert response.status_code in [403, 404]


def test_user_cannot_generate_report_for_other_user_assessment(
    client: TestClient,
    auth_token: str,
    test_user2_token: str,
    completed_assessment: Any,
) -> None:
    """Test that User A cannot generate report for User B's assessment"""
    response = client.post(
        f"/api/reports/{completed_assessment.id}/generate",
        headers={"Authorization": f"Bearer {test_user2_token}"},
    )
    assert response.status_code == 403 or response.status_code == 404


def test_user_cannot_view_other_user_report_status(
    client: TestClient, auth_token: str, test_user2_token: str, test_report: Any
) -> None:
    """Test that User A cannot view User B's report status"""
    response = client.get(
        f"/api/reports/{test_report.id}/status",
        headers={"Authorization": f"Bearer {test_user2_token}"},
    )
    assert response.status_code == 403


def test_admin_can_generate_ai_reports(
    client: TestClient, admin_token: str, completed_assessment: Any, db_session: Any
) -> None:
    """Test that admin can generate AI reports for any user"""
    from app.models.assessment import Report

    report = Report(
        assessment_id=completed_assessment.id,
        report_type="ai_enhanced",
        status="pending",
    )
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    response = client.post(
        f"/api/reports/admin/{report.id}/generate-ai",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200


def test_regular_user_cannot_generate_ai_reports(
    client: TestClient, auth_token: str, completed_assessment: Any, db_session: Any
) -> None:
    """Test that regular user cannot generate AI reports"""
    from app.models.assessment import Report

    report = Report(
        assessment_id=completed_assessment.id,
        report_type="ai_enhanced",
        status="pending",
    )
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    response = client.post(
        f"/api/reports/admin/{report.id}/generate-ai",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 403


def test_admin_can_release_ai_reports(
    client: TestClient, admin_token: str, completed_assessment: Any, db_session: Any
) -> None:
    """Test that admin can release AI reports to users"""
    from app.models.assessment import Report

    report = Report(
        assessment_id=completed_assessment.id,
        report_type="ai_enhanced",
        status="completed",
    )
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    response = client.post(
        f"/api/reports/admin/{report.id}/release",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200


def test_regular_user_cannot_release_ai_reports(
    client: TestClient, auth_token: str, completed_assessment: Any, db_session: Any
) -> None:
    """Test that regular user cannot release AI reports"""
    from app.models.assessment import Report

    report = Report(
        assessment_id=completed_assessment.id,
        report_type="ai_enhanced",
        status="completed",
    )
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    response = client.post(
        f"/api/reports/admin/{report.id}/release",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 403
