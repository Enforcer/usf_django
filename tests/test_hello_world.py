from django.test import Client


def test_root_returns_404(client: Client) -> None:
    response = client.get("/")

    assert response.status_code == 404
