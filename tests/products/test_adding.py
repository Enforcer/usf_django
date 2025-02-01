import pytest
from rest_framework.test import APIClient

from tests.factories import CategoryFactory, UserFactory

pytestmark = [pytest.mark.django_db(transaction=True)]


def test_added_product_is_visible_only_for_the_owner(api_client: APIClient) -> None:
    user = UserFactory(password="pass")
    category = CategoryFactory(created_by=user)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/api/products/",
        {
            "name": "test",
            "description": "test",
            "price": 100,
            "category": category.id,
        },
        format="json",
    )

    assert response.status_code == 201

    response2 = api_client.get("/api/products/")

    assert response2.status_code == 200
    assert len(response2.json()) == 1
    assert response2.json()[0] == response.json()

    api_client.force_authenticate(user=UserFactory(password="123"))
    response3 = api_client.get("/api/products/")
    assert response3.status_code == 200
    assert len(response3.json()) == 0
