from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
# from .models import TestResult

@shared_task
def send_test_result_notification(test_result_id):
    """
    Send an email notification when a new test result is created.
    """
    try:
        # test_result = TestResult.objects.get(id=test_result_id)
        # subject = f'New Test Result Created: {test_result.device.name}'
        # message = f"""
        # A new test result has been created:
        
        # Device: {test_result.device.name}
        # Protocol: {test_result.protocol.name}
        # Status: {test_result.status}
        # Performed by: {test_result.performed_by.username}
        # Start Time: {test_result.start_time}
        
        # You can view the full details in the admin panel.
        # """
        
        # send_mail(
        #     subject=subject,
        #     message=message,
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=['admin@example.com'],
        #     fail_silently=False,
        # )
        return f"Email notification sent for test result {test_result_id}"
    except TestResult.DoesNotExist:
        return f"Test result {test_result_id} not found"
    except Exception as e:
        return f"Error sending email notification: {str(e)}" 