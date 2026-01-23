from typing import Any

from fastapi.testclient import TestClient


def test_complete_user_flow(client: TestClient) -> None:
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "integration@example.com",
            "password": "IntegrationTest123!",
            "full_name": "Integration Test User",
            "company_name": "Integration Test Company",
        },
    )
    assert register_response.status_code == 200
    token = register_response.json()["access_token"]

    start_response = client.post(
        "/api/assessment/start", headers={"Authorization": f"Bearer {token}"}
    )
    assert start_response.status_code == 200
    assessment_id = start_response.json()["id"]

    save_response = client.post(
        f"/api/assessment/{assessment_id}/save-progress",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "responses": [
                {
                    "section_id": "access-control",
                    "question_id": "ac-1",
                    "answer_value": "yes",
                    "comment": "Implemented",
                }
            ]
        },
    )
    assert save_response.status_code == 200

    complete_response = client.post(
        f"/api/assessment/{assessment_id}/complete",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert complete_response.status_code == 200

    from unittest.mock import patch

    with patch("app.api.reports.BackgroundTasks.add_task"):
        report_response = client.post(
            f"/api/reports/{assessment_id}/generate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert report_response.status_code == 200


def test_admin_workflow(
    client: TestClient,
    admin_token: str,
    test_user: Any,
    admin_completed_assessment: Any,
) -> None:
    users_response = client.get(
        "/api/admin/users", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert users_response.status_code == 200

    assessments_response = client.get(
        "/api/admin/assessments", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert assessments_response.status_code == 200

    stats_response = client.get(
        "/api/admin/dashboard/stats", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert stats_response.status_code == 200

    from unittest.mock import patch

    with patch("app.api.reports.BackgroundTasks.add_task"):
        generate_response = client.post(
            f"/api/reports/{admin_completed_assessment.id}/generate",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert generate_response.status_code == 200
