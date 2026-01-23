from typing import Any

from fastapi.testclient import TestClient


def test_admin_users_pagination_first_page(
    client: TestClient, admin_token: Any, test_user: Any
) -> None:
    """Test first page of users pagination"""
    response = client.get(
        "/api/admin/users",
        params={"skip": 0, "limit": 10},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "pages" in data
    assert "has_next" in data
    assert "has_prev" in data
    assert data["page"] == 1
    assert data["has_prev"] is False
    assert isinstance(data["items"], list)


def test_admin_users_pagination_metadata(
    client: TestClient, admin_token: Any, db_session: Any
) -> None:
    """Test pagination metadata calculation"""
    from app.core.security import get_password_hash
    from app.models.user import User

    for i in range(25):
        user = User(
            email=f"pagtest{i}@example.com",
            full_name=f"Pag Test {i}",
            company_name="Test Co",
            password_hash=get_password_hash("TestPass123!"),
            is_active=True,
        )
        db_session.add(user)
    db_session.commit()

    response = client.get(
        "/api/admin/users",
        params={"skip": 0, "limit": 10},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 25
    assert data["page"] == 1
    assert len(data["items"]) == 10
    assert data["has_next"] is True
    assert data["has_prev"] is False

    response = client.get(
        "/api/admin/users",
        params={"skip": 10, "limit": 10},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert data["has_prev"] is True


def test_admin_assessments_pagination(
    client: TestClient, admin_token: Any, test_assessment: Any
) -> None:
    """Test assessments pagination"""
    response = client.get(
        "/api/admin/assessments",
        params={"skip": 0, "limit": 20},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "has_next" in data
    assert "has_prev" in data


def test_admin_reports_pagination(
    client: TestClient, admin_token: Any, test_report: Any
) -> None:
    """Test reports pagination"""
    response = client.get(
        "/api/admin/reports",
        params={"skip": 0, "limit": 20},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "has_next" in data
    assert "has_prev" in data


def test_consultations_pagination(
    client: TestClient, admin_token: Any, db_session: Any, test_user: Any
) -> None:
    """Test consultations pagination"""
    from datetime import UTC, datetime, timedelta

    from app.models.assessment import Assessment

    consultation = Assessment(
        user_id=test_user.id,
        status="completed",
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        expires_at=datetime.now(UTC) + timedelta(days=14),
        progress_percentage=100.0,
        consultation_interest=True,
        consultation_details=" ".join(["word"] * 250),
    )
    db_session.add(consultation)
    db_session.commit()

    response = client.get(
        "/api/admin/consultations",
        params={"skip": 0, "limit": 20},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "has_next" in data
    assert "has_prev" in data


def test_user_reports_pagination(client: TestClient, auth_token: str) -> None:
    """Test user reports pagination"""
    response = client.get(
        "/api/reports/user/reports",
        params={"skip": 0, "limit": 20},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "has_next" in data
    assert "has_prev" in data


def test_pagination_empty_results(client: TestClient, admin_token: str) -> None:
    """Test pagination with no results"""
    response = client.get(
        "/api/admin/users",
        params={"skip": 0, "limit": 10, "search": "nonexistent-user-xyz"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["pages"] == 0
    assert data["has_next"] is False
    assert data["has_prev"] is False


def test_pagination_pages_calculation(
    client: TestClient, admin_token: Any, db_session: Any
) -> None:
    """Test pages calculation in pagination"""
    from app.core.security import get_password_hash
    from app.models.user import User

    for i in range(35):
        user = User(
            email=f"pagetest{i}@example.com",
            full_name=f"Page Test {i}",
            company_name="Test Co",
            password_hash=get_password_hash("TestPass123!"),
            is_active=True,
        )
        db_session.add(user)
    db_session.commit()

    response = client.get(
        "/api/admin/users",
        params={"skip": 0, "limit": 10},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 35
    expected_pages = (data["total"] + 9) // 10
    assert data["pages"] == expected_pages
