import pytest
from django.urls import reverse
from rest_framework import status
from user.models import User


@pytest.mark.django_db
def test_user_registration(api_client, user_data):
    url = reverse("register")
    response = api_client.post(url, user_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert "email" in response.data
    assert "name" not in response.data
    assert "password" not in response.data


@pytest.mark.django_db
def test_user_registration_invalid(api_client):
    url = reverse("register")
    response = api_client.post(url, {}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_login(api_client, user_data):
    # Register the user first
    User.objects.create_user(**user_data)

    # Now log in
    url = reverse("login")
    response = api_client.post(
        url,
        {"email": user_data["email"], "password": user_data["password"]},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_user_login_invalid(api_client):
    url = reverse("login")
    response = api_client.post(
        url,
        {"email": "nonexistent@example.com", "password": "wrongpassword"},
        format="json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_logout(api_client, user_data):
    # Register the user first
    User.objects.create_user(**user_data)

    # Log in to get tokens
    url = reverse("login")
    login_response = api_client.post(
        url,
        {"email": user_data["email"], "password": user_data["password"]},
        format="json",
    )
    refresh_token = login_response.data["refresh"]

    # Now log out
    url = reverse("logout")
    response = api_client.post(url, {"refresh": refresh_token}, format="json")
    assert response.status_code == status.HTTP_205_RESET_CONTENT


@pytest.mark.django_db
def test_user_logout_invalid(api_client):
    url = reverse("logout")
    response = api_client.post(url, {"refresh": "invalidtoken"}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_token_refresh(api_client, user_data):
    # Register the user first
    User.objects.create_user(**user_data)

    # Log in to get tokens
    url = reverse("login")
    login_response = api_client.post(
        url,
        {"email": user_data["email"], "password": user_data["password"]},
        format="json",
    )
    refresh_token = login_response.data["refresh"]

    # Refresh the token
    url = reverse("token-refresh")
    response = api_client.post(url, {"refresh": refresh_token}, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_token_refresh_invalid(api_client):
    url = reverse("token-refresh")
    response = api_client.post(url, {"refresh": "invalidtoken"}, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
