from celery import shared_task
from django.utils import timezone
from .models import Order


@shared_task
def check_past_due_orders():
    today = timezone.now().date()
    past_due_orders = Order.objects.filter(delivery_date__gt=today, status="CREATED")
    for order in past_due_orders:
        order.status = "DELAYED"
        order.save()
