from unittest.mock import patch

from fastapi.testclient import TestClient


def test_health_endpoint_healthy(client: TestClient) -> None:
    """Test comprehensive health check when all systems are healthy"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert data["version"] == "1.0.0"
    assert "uptime_seconds" in data
    assert data["uptime_seconds"] >= 0
    assert "timestamp" in data
    assert "checks" in data
    assert "database" in data["checks"]
    assert data["checks"]["database"]["status"] == "healthy"


def test_health_endpoint_database_failure(client: TestClient) -> None:
    """Test health check when database is unavailable"""
    with patch("app.api.health.check_database") as mock_check:
        mock_check.return_value = {
            "status": "unhealthy",
            "message": "Database connection failed: Connection refused",
        }
        response = client.get("/health")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["checks"]["database"]["status"] == "unhealthy"


def test_health_endpoint_with_redis(client: TestClient) -> None:
    """Test health check includes Redis when configured"""
    with patch("app.core.config.settings.REDIS_URL", "redis://localhost:6379/0"):
        with patch("app.api.health.check_redis") as mock_redis:
            mock_redis.return_value = {
                "status": "healthy",
                "message": "Redis connection successful",
            }
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert "redis" in data["checks"]
            assert data["checks"]["redis"]["status"] == "healthy"


def test_health_endpoint_redis_failure(client: TestClient) -> None:
    """Test health check when Redis is configured but unavailable"""
    with patch("app.core.config.settings.REDIS_URL", "redis://localhost:6379/0"):
        with patch("app.api.health.check_redis") as mock_redis:
            mock_redis.return_value = {
                "status": "unhealthy",
                "message": "Redis connection failed: Connection refused",
            }
            response = client.get("/health")
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "unhealthy"
            assert data["checks"]["redis"]["status"] == "unhealthy"


def test_liveness_probe(client: TestClient) -> None:
    """Test liveness probe always returns 200"""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "version" in data
    assert data["version"] == "1.0.0"
    assert "uptime_seconds" in data
    assert data["uptime_seconds"] >= 0
    assert "timestamp" in data


def test_liveness_probe_even_with_db_failure(client: TestClient) -> None:
    """Test liveness probe returns 200 even if database is down"""
    with patch("app.api.health.check_database") as mock_check:
        mock_check.return_value = {
            "status": "unhealthy",
            "message": "Database connection failed",
        }
        response = client.get("/health/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"


def test_readiness_probe_healthy(client: TestClient) -> None:
    """Test readiness probe when database is accessible"""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "version" in data
    assert "uptime_seconds" in data
    assert "checks" in data
    assert "database" in data["checks"]
    assert data["checks"]["database"]["status"] == "healthy"


def test_readiness_probe_database_failure(client: TestClient) -> None:
    """Test readiness probe when database is unavailable"""
    with patch("app.api.health.check_database") as mock_check:
        mock_check.return_value = {
            "status": "unhealthy",
            "message": "Database connection failed: Connection refused",
        }
        response = client.get("/health/ready")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "not_ready"
        assert data["checks"]["database"]["status"] == "unhealthy"


def test_uptime_increases(client: TestClient) -> None:
    """Test that uptime increases between calls"""
    import time

    response1 = client.get("/health/live")
    uptime1 = response1.json()["uptime_seconds"]

    time.sleep(0.1)

    response2 = client.get("/health/live")
    uptime2 = response2.json()["uptime_seconds"]

    assert uptime2 > uptime1
