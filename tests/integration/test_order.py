import pytest
from django.urls import reverse
from rest_framework import status
from order.models import Order


@pytest.mark.django_db
def test_create_order(auth_client, order_data):
    url = reverse("create_order")
    response = auth_client.post(url, order_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data

    # Check if the order is created in the database
    order = Order.objects.get(id=response.data["id"])
    assert order.sku == order_data["sku"]
    assert order.user.email == "testuser@example.com"


@pytest.mark.django_db
def test_create_order_invalid(auth_client):
    url = reverse("create_order")
    response = auth_client.post(url, {}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_retrieve_order(auth_client, order_data):
    # Create an order first
    url = reverse("create_order")
    create_response = auth_client.post(url, order_data, format="json")
    order_id = create_response.data["id"]

    # Now retrieve the order
    url = reverse("order_detail", args=[order_id])
    response = auth_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == order_id
    assert response.data["sku"] == order_data["sku"]
    assert response.data["user"] == (auth_client._credentials["instance"].id)


@pytest.mark.django_db
def test_retrieve_order_invalid(auth_client):
    url = reverse("order_detail", args=[9999])
    response = auth_client.get(url, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND
