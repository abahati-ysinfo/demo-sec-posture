from typing import Any

from fastapi.testclient import TestClient


def test_get_assessment_structure(client: TestClient) -> None:
    response = client.get("/api/assessment/structure")
    assert response.status_code == 200
    data = response.json()
    assert "sections" in data
    assert "total_questions" in data
    assert data["total_questions"] > 0
    assert len(data["sections"]) > 0


def test_start_assessment_new(
    client: TestClient, test_user: Any, auth_token: str
) -> None:
    response = client.post(
        "/api/assessment/start", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"
    assert data["user_id"] == str(test_user.id)
    assert data["progress_percentage"] == 0.0


def test_start_assessment_existing(
    client: TestClient, test_user: Any, auth_token: str, test_assessment: Any
) -> None:
    response = client.post(
        "/api/assessment/start", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_assessment.id)
    assert data["status"] == "in_progress"


def test_start_assessment_unauthenticated(client: TestClient) -> None:
    response = client.post("/api/assessment/start")
    assert response.status_code == 403


def test_get_current_assessment(
    client: TestClient, auth_token: str, test_assessment: Any
) -> None:
    response = client.get(
        "/api/assessment/current", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_assessment.id)
    assert data["status"] == "in_progress"


def test_get_current_assessment_none(client: TestClient, auth_token: str) -> None:
    response = client.get(
        "/api/assessment/current", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 404
    assert "no active assessment" in response.json()["detail"].lower()


def test_get_assessment_responses(
    client: TestClient,
    auth_token: str,
    test_assessment: Any,
    test_assessment_response: Any,
) -> None:
    response = client.get(
        f"/api/assessment/{test_assessment.id}/responses",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["question_id"] == "ac-1"
    assert data[0]["answer_value"] == "yes"


def test_get_assessment_responses_not_found(
    client: TestClient, auth_token: str
) -> None:
    response = client.get(
        "/api/assessment/nonexistent-id/responses",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 404


def test_save_assessment_progress(
    client: TestClient, auth_token: str, test_assessment: Any
) -> None:
    response = client.post(
        f"/api/assessment/{test_assessment.id}/save-progress",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "responses": [
                {
                    "section_id": "access-control",
                    "question_id": "ac-2",
                    "answer_value": "no",
                    "comment": "Not implemented yet",
                }
            ]
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "progress_percentage" in data


def test_save_assessment_progress_update_existing(
    client: TestClient,
    auth_token: str,
    test_assessment: Any,
    test_assessment_response: Any,
) -> None:
    response = client.post(
        f"/api/assessment/{test_assessment.id}/save-progress",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "responses": [
                {
                    "section_id": "access-control",
                    "question_id": "ac-1",
                    "answer_value": "no",
                    "comment": "Updated comment",
                }
            ]
        },
    )
    assert response.status_code == 200


def test_save_assessment_progress_not_found(
    client: TestClient, auth_token: str
) -> None:
    response = client.post(
        "/api/assessment/nonexistent-id/save-progress",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "responses": [
                {
                    "section_id": "access-control",
                    "question_id": "ac-1",
                    "answer_value": "yes",
                }
            ]
        },
    )
    assert response.status_code == 404


def test_complete_assessment(
    client: TestClient, auth_token: str, test_assessment: Any
) -> None:
    response = client.post(
        f"/api/assessment/{test_assessment.id}/complete",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_complete_assessment_not_found(client: TestClient, auth_token: str) -> None:
    response = client.post(
        "/api/assessment/nonexistent-id/complete",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 404


def test_save_consultation_interest(
    client: TestClient, auth_token: str, test_assessment: Any
) -> None:
    consultation_details = " ".join(["word"] * 250)
    response = client.post(
        f"/api/assessment/{test_assessment.id}/consultation",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "consultation_interest": True,
            "consultation_details": consultation_details,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_save_consultation_interest_invalid_word_count(
    client: TestClient, auth_token: str, test_assessment: Any
) -> None:
    short_details = "Too short"
    response = client.post(
        f"/api/assessment/{test_assessment.id}/consultation",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"consultation_interest": True, "consultation_details": short_details},
    )
    assert response.status_code == 422
    assert "at least 10 words" in str(response.json())
