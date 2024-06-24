from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet

urlpatterns = [
    path("register", UserViewSet.as_view({"post": "register"}), name="register"),
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("logout", UserViewSet.as_view({"post": "logout"}), name="logout"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
]
