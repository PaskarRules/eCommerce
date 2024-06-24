from django.core.management.base import BaseCommand
from order.tasks import check_past_due_orders


class Command(BaseCommand):
    help = "Check for past due orders"

    def handle(self, *args, **kwargs):
        check_past_due_orders.delay()
        self.stdout.write(
            self.style.SUCCESS("Successfully triggered check_past_due_orders task")
        )
