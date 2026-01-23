from typing import Any

from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_root_endpoint(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200


def test_docs_endpoint(client: TestClient) -> None:
    response = client.get("/docs")
    assert response.status_code == 200


def test_register_new_user(client: TestClient) -> None:
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "SecurePass123!",
            "full_name": "New User",
            "company_name": "New Company",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user" in data
    assert data["user"]["email"] == "newuser@example.com"
    assert data["user"]["full_name"] == "New User"
    assert data["user"]["company_name"] == "New Company"


def test_register_duplicate_email(client: TestClient, test_user: Any) -> None:
    response = client.post(
        "/api/auth/register",
        json={
            "email": test_user.email,
            "password": "SecurePass123!",
            "full_name": "Duplicate User",
            "company_name": "Company",
        },
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_valid_credentials(client: TestClient, test_user: Any) -> None:
    response = client.post(
        "/api/auth/login",
        json={"email": test_user.email, "password": "TestPass123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user" in data
    assert data["user"]["email"] == test_user.email


def test_login_invalid_password(client: TestClient, test_user: Any) -> None:
    response = client.post(
        "/api/auth/login", json={"email": test_user.email, "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


def test_login_nonexistent_user(client: TestClient) -> None:
    response = client.post(
        "/api/auth/login",
        json={"email": "nonexistent@example.com", "password": "password123"},
    )
    assert response.status_code == 401


def test_get_current_user_authenticated(
    client: TestClient, test_user: Any, auth_token: str
) -> None:
    response = client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["full_name"] == test_user.full_name
    assert data["company_name"] == test_user.company_name


def test_get_current_user_unauthenticated(client: TestClient) -> None:
    response = client.get("/api/auth/me")
    assert response.status_code == 403


def test_get_current_user_invalid_token(client: TestClient) -> None:
    response = client.get(
        "/api/auth/me", headers={"Authorization": "Bearer invalid_token_here"}
    )
    assert response.status_code == 401


def test_admin_user_login(client: TestClient, test_admin_user: Any) -> None:
    response = client.post(
        "/api/auth/login",
        json={"email": test_admin_user.email, "password": "AdminPass123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == test_admin_user.email


def test_password_hashing() -> None:
    """Test password hashing and verification"""
    from app.core.security import get_password_hash, verify_password

    password = "SecurePassword123!"
    hashed = get_password_hash(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_token_verification() -> None:
    """Test token creation and verification"""
    from app.core.security import create_access_token, verify_token

    data = {"sub": "test@example.com", "user_id": "123"}
    token, csrf_token = create_access_token(data=data)

    assert token is not None
    assert isinstance(token, str)

    decoded = verify_token(token)
    assert decoded["sub"] == "test@example.com"
    assert decoded["user_id"] == "123"


def test_admin_token_creation() -> None:
    """Test creating admin token with is_admin flag"""
    from app.core.security import create_access_token, verify_token

    data = {"sub": "admin@example.com", "user_id": "456"}
    token, csrf_token = create_access_token(data=data, is_admin=True)

    decoded = verify_token(token)
    assert decoded["sub"] == "admin@example.com"
    assert decoded["is_admin"]


def test_generate_admin_password() -> None:
    """Test admin password generation"""
    from app.core.security import generate_admin_password, verify_password

    plain, hashed = generate_admin_password()

    assert len(plain) == 16
    assert plain != hashed
    assert verify_password(plain, hashed)
