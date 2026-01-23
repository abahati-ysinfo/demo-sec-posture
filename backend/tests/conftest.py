import os
import sys
from collections.abc import Generator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest
from cryptography.fernet import Fernet
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

TEST_DATABASE_URL = "sqlite:///./test.db"
os.environ.setdefault("DATABASE_URL", TEST_DATABASE_URL)
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-testing-only-not-secure")

from app.core.database import Base, get_db
from app.core.security import create_access_token, get_password_hash
from app.main import app
from app.models.assessment import Assessment, Report
from app.models.assessment import AssessmentResponse as AssessmentResponseModel
from app.models.user import User

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def encryption_key(monkeypatch: Any) -> str:
    """Set up encryption key for tests."""
    from app.core.config import settings

    key = Fernet.generate_key().decode()
    monkeypatch.setattr(settings, "OPENAI_KEYS_ENCRYPTION_KEY", key)
    return key


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session) -> User:
    user = User(
        email="test@example.com",
        full_name="Test User",
        company_name="Test Company",
        password_hash=get_password_hash("TestPass123!"),
        is_active=True,
        is_admin=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user2(db_session: Session) -> User:
    user = User(
        email="testuser2@example.com",
        full_name="Test User 2",
        company_name="Test Company 2",
        password_hash=get_password_hash("TestPass123!"),
        is_active=True,
        is_admin=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_admin_user(db_session: Session) -> User:
    admin = User(
        email="admin@example.com",
        full_name="Admin User",
        company_name="Test Company",
        password_hash=get_password_hash("AdminPass123!"),
        is_active=True,
        is_admin=True,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def auth_token(test_user: User) -> str:
    token, _ = create_access_token(
        data={"sub": test_user.email, "user_id": str(test_user.id), "is_admin": False}
    )
    return token


@pytest.fixture
def test_user2_token(test_user2: User) -> str:
    token, _ = create_access_token(
        data={"sub": test_user2.email, "user_id": str(test_user2.id), "is_admin": False}
    )
    return token


@pytest.fixture
def admin_token(test_admin_user: User) -> str:
    token, _ = create_access_token(
        data={
            "sub": test_admin_user.email,
            "user_id": str(test_admin_user.id),
            "is_admin": True,
        },
        is_admin=True,
    )
    return token


@pytest.fixture
def test_assessment(db_session: Session, test_user: User) -> Assessment:
    assessment = Assessment(
        user_id=test_user.id,
        status="in_progress",
        started_at=datetime.now(UTC),
        expires_at=datetime.now(UTC) + timedelta(days=15),
        progress_percentage=0.0,
    )
    db_session.add(assessment)
    db_session.commit()
    db_session.refresh(assessment)
    return assessment


@pytest.fixture
def completed_assessment(db_session: Session, test_user: User) -> Assessment:
    assessment = Assessment(
        user_id=test_user.id,
        status="completed",
        started_at=datetime.now(UTC) - timedelta(days=1),
        completed_at=datetime.now(UTC),
        expires_at=datetime.now(UTC) + timedelta(days=14),
        progress_percentage=100.0,
    )
    db_session.add(assessment)
    db_session.commit()
    db_session.refresh(assessment)
    return assessment


@pytest.fixture
def admin_completed_assessment(
    db_session: Session, test_admin_user: User
) -> Assessment:
    assessment = Assessment(
        user_id=test_admin_user.id,
        status="completed",
        started_at=datetime.now(UTC) - timedelta(days=1),
        completed_at=datetime.now(UTC),
        expires_at=datetime.now(UTC) + timedelta(days=14),
        progress_percentage=100.0,
    )
    db_session.add(assessment)
    db_session.commit()
    db_session.refresh(assessment)
    return assessment


@pytest.fixture
def test_assessment_response(
    db_session: Session, test_assessment: Assessment
) -> AssessmentResponseModel:
    response = AssessmentResponseModel(
        assessment_id=test_assessment.id,
        section_id="access-control",
        question_id="ac-1",
        answer_value="yes",
        comment="Test comment",
    )
    db_session.add(response)
    db_session.commit()
    db_session.refresh(response)
    return response


@pytest.fixture
def test_report(db_session: Session, completed_assessment: Assessment) -> Report:
    report = Report(
        assessment_id=completed_assessment.id, report_type="standard", status="pending"
    )
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)
    return report


def pytest_configure(config: Any) -> None:
    """Relax coverage threshold for targeted smoke runs that only hit report suites."""

    cov_plugin = config.pluginmanager.get_plugin("_cov")
    if not cov_plugin:
        return

    selected = [Path(arg) for arg in config.args if Path(arg).exists()]
    if not selected:
        return

    target_files = {
        Path("tests/test_report_generator.py").resolve(),
        Path("tests/test_reports_endpoints.py").resolve(),
    }

    resolved_selected = {path.resolve() for path in selected}
    if resolved_selected.issubset(target_files):
        config.option.cov_fail_under = 0
        if hasattr(cov_plugin, "options"):
            cov_plugin.options.cov_fail_under = 0
