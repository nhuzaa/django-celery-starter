from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestResult
from .tasks import send_test_result_notification

@receiver(post_save, sender=TestResult)
def notify_admin_on_test_result_creation(sender, instance, created, **kwargs):
    """
    Signal handler to send email notification when a new test result is created.
    """
    if created:
        # Trigger the Celery task asynchronously
        send_test_result_notification.delay(instance.id) 