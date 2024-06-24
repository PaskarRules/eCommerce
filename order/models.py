from django.db import models
from user.models import User


class Order(models.Model):
    CREATED = "CREATED"
    DELAYED = "DELAYED"
    STATUS_CHOICES = [
        (CREATED, "Created"),
        (DELAYED, "Delayed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    sku = models.CharField(max_length=8, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=CREATED)
