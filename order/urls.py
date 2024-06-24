from django.urls import path

from .views import OrderViewSet


urlpatterns = [
    path("new", OrderViewSet.as_view({"post": "new"}), name="create_order"),
    path(
        "<int:pk>", OrderViewSet.as_view({"get": "retrieve_order"}), name="order_detail"
    ),
]
