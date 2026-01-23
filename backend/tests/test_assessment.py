from fastapi.testclient import TestClient


def test_assessment_structure_endpoint(client: TestClient) -> None:
    response = client.get("/api/assessment/structure")
    assert response.status_code == 200
    payload = response.json()
    assert "sections" in payload
    assert isinstance(payload.get("sections"), list)
