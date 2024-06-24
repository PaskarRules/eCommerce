import pytest

from django.urls import reverse

from user.models import User


@pytest.fixture
def user(user_data):
    return User.objects.create_user(**user_data)


@pytest.fixture
def auth_client(api_client, user):
    url = reverse("login")
    response = api_client.post(
        url, {"email": user.email, "password": "testpassword"}, format="json"
    )
    api_client.credentials(
        HTTP_AUTHORIZATION="Bearer " + response.data["access"], instance=user
    )
    return api_client


@pytest.fixture
def order_data():
    return {"sku": "ABC12345", "price": 99.99, "delivery_date": "2024-07-15"}
