from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_policy_query_endpoint_returns_hotel_allowance():
    response = client.post(
        "/api/policy/query",
        json={
            "question": "What is the hotel allowance in India?"
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "answer": "$120 USD per night."
    }


def test_policy_query_endpoint_handles_unsupported_question():
    response = client.post(
        "/api/policy/query",
        json={
            "question": "What is the company policy for maternity leave?"
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "answer": (
            "The travel expense policy does not cover this question."
        )
    }


def test_policy_query_endpoint_handles_ambiguous_question():
    response = client.post(
        "/api/policy/query",
        json={
            "question": "What is the airfare allowance?"
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "answer": (
            "The question matches multiple travel policies. "
            "Please provide more specific details."
        )
    }


def test_policy_query_endpoint_rejects_missing_question():
    response = client.post(
        "/api/policy/query",
        json={}
    )

    assert response.status_code == 422