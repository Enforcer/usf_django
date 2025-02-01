from unittest.mock import Mock, patch, seal

import pytest
import stripe
from django.test import override_settings
from rest_framework.test import APIClient

from tests.factories import CategoryFactory

pytestmark = [pytest.mark.django_db(transaction=True)]


BUYER_USERNAME = "buyer"
BUYER_PASSWORD = "Pwd123!BYR"  # noqa: S105

SELLER_USERNAME = "seller"
SELLER_PASSWORD = "Pwd123!SLR"  # noqa: S105


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
def test_bought_product_is_no_longer_available(api_client: APIClient) -> None:
    register_buyer = api_client.post(
        "/auth/users/", {"username": BUYER_USERNAME, "password": BUYER_PASSWORD}
    )
    assert register_buyer.status_code == 201
    register_seller = api_client.post(
        "/auth/users/", {"username": SELLER_USERNAME, "password": SELLER_PASSWORD}
    )
    assert register_seller.status_code == 201

    assert api_client.login(username=SELLER_USERNAME, password=SELLER_PASSWORD)

    category = CategoryFactory()
    add_product = api_client.post(
        "/api/products/",
        {
            "name": "test",
            "description": "test",
            "price": 100,
            "category": category.id,
            "status": "available",
        },
    )
    assert add_product.status_code == 201

    assert api_client.login(username=BUYER_USERNAME, password=BUYER_PASSWORD)
    find_product = api_client.get("/api/public/products/?search=test")
    assert find_product.status_code == 200
    assert len(find_product.json()) == 1
    product_id = find_product.json()[0]["id"]
    price_with_insurance = find_product.json()[0]["price_with_insurance"]

    create_order = api_client.post("/api/orders/", {"product_id": product_id})
    assert create_order.status_code == 201
    assert create_order.json()["price"] == price_with_insurance
    order_id = create_order.json()["id"]
    intent_mock = Mock(client_secret="a_client_secret", id="pi_id123")
    seal(intent_mock)
    with patch.object(stripe.PaymentIntent, "create", return_value=intent_mock):
        confirm_order = api_client.post(f"/api/orders/{order_id}/confirm/")
    assert confirm_order.status_code == 200

    find_product_again = api_client.get("/api/public/products/?search=test")
    assert find_product_again.status_code == 200
    assert len(find_product_again.json()) == 0

    find_product_by_id = api_client.get(f"/api/public/products/{product_id}/")
    assert find_product_by_id.status_code == 200
    assert find_product_by_id.json()["id"] == product_id
    assert find_product_by_id.json()["effective_status"] == "reserved"

    payment_id = confirm_order.json()["payment_id"]
    payment = api_client.get(f"/api/payments/{payment_id}/")
    assert payment.status_code == 200
    assert payment.json()["amount"] == price_with_insurance

    webhook = api_client.post(
        "/api/payments/webhook/",
        format="json",
        data={
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": intent_mock.id}},
        },
    )
    assert webhook.status_code == 200

    find_product_by_id_after_payment = api_client.get(
        f"/api/public/products/{product_id}/"
    )
    assert find_product_by_id_after_payment.status_code == 404, "Item was found!"

    user_orders = api_client.get("/api/orders/")
    assert user_orders.status_code == 200
    assert len(user_orders.json()) == 1
    assert user_orders.json()[0]["status"] == "paid"
