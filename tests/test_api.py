from __future__ import annotations

import pytest

flask = pytest.importorskip("flask")

from family_tree.api import create_app
from family_tree.constants import CHILD_ADDED, CHILD_ADDITION_FAILED, PERSON_NOT_FOUND


@pytest.fixture
def client() -> flask.testing.FlaskClient:
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_health_endpoint(client: flask.testing.FlaskClient) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_root_redirects_to_ui_page(client: flask.testing.FlaskClient) -> None:
    response = client.get("/")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/ui")


def test_ui_page(client: flask.testing.FlaskClient) -> None:
    response = client.get("/ui")

    assert response.status_code == 200
    assert b"Family Tree UI Validator" in response.data
    assert b"Add Child" in response.data
    assert b"Batch Commands" not in response.data


def test_terminal_page(client: flask.testing.FlaskClient) -> None:
    response = client.get("/terminal")

    assert response.status_code == 200
    assert b"Family Tree Terminal Validator" in response.data
    assert b"Input Commands" in response.data
    assert b"Add Child" not in response.data


def test_add_child_endpoint(client: flask.testing.FlaskClient) -> None:
    response = client.post(
        "/api/add-child",
        json={"mother_name": "Flora", "child_name": "Minerva", "gender": "Female"},
    )

    assert response.status_code == 200
    assert response.get_json() == {"output": CHILD_ADDED}


def test_relationship_endpoint_uses_current_tree_state(
    client: flask.testing.FlaskClient,
) -> None:
    client.post(
        "/api/add-child",
        json={"mother_name": "Flora", "child_name": "Minerva", "gender": "Female"},
    )
    response = client.post(
        "/api/relationship",
        json={"name": "Remus", "relationship": "Maternal-Aunt"},
    )

    assert response.status_code == 200
    assert response.get_json() == {"output": "Dominique Minerva"}


def test_batch_commands_endpoint(client: flask.testing.FlaskClient) -> None:
    response = client.post(
        "/api/commands",
        json={
            "commands": "\n".join(
                [
                    "ADD_CHILD Ted Bella Female",
                    "ADD_CHILD Luna Lola Female",
                ]
            )
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {"outputs": [CHILD_ADDITION_FAILED, PERSON_NOT_FOUND]}


def test_batch_commands_can_reset_before_running(client: flask.testing.FlaskClient) -> None:
    commands = "\n".join(
        [
            "ADD_CHILD Flora Minerva Female",
            "GET_RELATIONSHIP Remus Maternal-Aunt",
        ]
    )
    first_response = client.post(
        "/api/commands",
        json={"commands": commands, "reset_before": True},
    )
    second_response = client.post(
        "/api/commands",
        json={"commands": commands, "reset_before": True},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.get_json() == {"outputs": ["CHILD_ADDED", "Dominique Minerva"]}
    assert second_response.get_json() == {"outputs": ["CHILD_ADDED", "Dominique Minerva"]}


def test_reset_endpoint_restores_initial_tree(client: flask.testing.FlaskClient) -> None:
    client.post(
        "/api/add-child",
        json={"mother_name": "Flora", "child_name": "Minerva", "gender": "Female"},
    )
    client.post("/api/reset")
    response = client.post(
        "/api/relationship",
        json={"name": "Remus", "relationship": "Maternal-Aunt"},
    )

    assert response.status_code == 200
    assert response.get_json() == {"output": "Dominique"}
