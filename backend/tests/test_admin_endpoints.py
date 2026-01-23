from datetime import UTC
from typing import Any

from fastapi.testclient import TestClient


def test_get_all_users(client: TestClient, admin_token: str, test_user: Any) -> None:
    response = client.get(
        "/api/admin/users", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 1


def test_get_all_users_with_search(
    client: TestClient, admin_token: str, test_user: Any
) -> None:
    response = client.get(
        "/api/admin/users",
        params={"search": test_user.email},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 1


def test_get_all_users_unauthorized(client: TestClient, auth_token: str) -> None:
    response = client.get(
        "/api/admin/users", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 403


def test_get_user(client: TestClient, admin_token: str, test_user: Any) -> None:
    response = client.get(
        f"/api/admin/users/{test_user.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email


def test_get_user_not_found(client: TestClient, admin_token: str) -> None:
    response = client.get(
        "/api/admin/users/nonexistent-id",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


def test_get_user_assessments(
    client: TestClient, admin_token: str, test_user: Any, test_assessment: Any
) -> None:
    response = client.get(
        f"/api/admin/users/{test_user.id}/assessments",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_all_assessments(
    client: TestClient, admin_token: str, test_assessment: Any
) -> None:
    response = client.get(
        "/api/admin/assessments", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)


def test_get_all_assessments_with_status_filter(
    client: TestClient, admin_token: str, test_assessment: Any
) -> None:
    response = client.get(
        "/api/admin/assessments",
        params={"status": "in_progress"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)


def test_get_dashboard_stats(
    client: TestClient, admin_token: str, test_user: Any, test_assessment: Any
) -> None:
    response = client.get(
        "/api/admin/dashboard/stats", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_users" in data
    assert "active_assessments" in data
    assert "completed_assessments" in data
    assert data["total_users"] >= 1


def test_get_users_progress_summary(
    client: TestClient, admin_token: str, test_user: Any
) -> None:
    response = client.get(
        "/api/admin/users-progress-summary",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "users_progress" in data
    assert isinstance(data["users_progress"], list)


def test_get_all_reports(
    client: TestClient, admin_token: str, test_report: Any
) -> None:
    response = client.get(
        "/api/admin/reports", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)


def test_get_alerts(client: TestClient, admin_token: str) -> None:
    response = client.get(
        "/api/admin/alerts", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data
    assert isinstance(data["alerts"], list)


def test_delete_user(client: TestClient, admin_token: str, db_session: Any) -> None:
    from app.core.security import get_password_hash
    from app.models.user import User

    user_to_delete = User(
        email="delete@example.com",
        full_name="Delete User",
        company_name="Test Company",
        password_hash=get_password_hash("DeletePass123!"),
        is_active=True,
        is_admin=False,
    )
    db_session.add(user_to_delete)
    db_session.commit()
    db_session.refresh(user_to_delete)

    response = client.delete(
        f"/api/admin/users/{user_to_delete.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_reset_user_password(
    client: TestClient, admin_token: str, test_user: Any
) -> None:
    response = client.post(
        f"/api/admin/users/{test_user.id}/reset-password",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"new_password": "NewSecurePassword123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_get_consultation_requests(
    client: TestClient, admin_token: str, db_session: Any, test_user: Any
) -> None:
    from datetime import datetime, timedelta

    from app.models.assessment import Assessment

    consultation_assessment = Assessment(
        user_id=test_user.id,
        status="completed",
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        expires_at=datetime.now(UTC) + timedelta(days=14),
        progress_percentage=100.0,
        consultation_interest=True,
        consultation_details=" ".join(["word"] * 250),
    )
    db_session.add(consultation_assessment)
    db_session.commit()

    response = client.get(
        "/api/admin/consultations", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)


def test_bulk_update_user_status(
    client: TestClient, admin_token: str, test_user: Any
) -> None:
    response = client.post(
        "/api/admin/users/bulk-update-status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"user_ids": [str(test_user.id)], "is_active": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert "updated_count" in data


def test_bulk_delete_users(
    client: TestClient, admin_token: str, db_session: Any
) -> None:
    from app.core.security import get_password_hash
    from app.models.user import User

    user1 = User(
        email="bulk1@example.com",
        full_name="Bulk User 1",
        company_name="Test Company",
        password_hash=get_password_hash("BulkPass123!"),
        is_active=True,
        is_admin=False,
    )
    user2 = User(
        email="bulk2@example.com",
        full_name="Bulk User 2",
        company_name="Test Company",
        password_hash=get_password_hash("BulkPass123!"),
        is_active=True,
        is_admin=False,
    )
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()

    response = client.post(
        "/api/admin/users/bulk-delete",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"user_ids": [str(user1.id), str(user2.id)]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "deleted_count" in data
