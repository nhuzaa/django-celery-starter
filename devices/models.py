from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_test_result_notification
from users.models import CustomUser

class Device(models.Model):
    DEVICE_TYPES = [
        ('IMPLANT', 'Implant'),
        ('DIAGNOSTIC', 'Diagnostic'),
        ('MONITORING', 'Monitoring'),
        ('THERAPEUTIC', 'Therapeutic'),
    ]

    name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    model_number = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_devices')

    def __str__(self):
        return f"{self.name} ({self.model_number})"

    class Meta:
        ordering = ['-created_at']

class TestProtocol(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('ARCHIVED', 'Archived'),
    ]

    name = models.CharField(max_length=200)
    version = models.CharField(max_length=20)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_protocols')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    devices = models.ManyToManyField(Device, related_name='test_protocols')

    def __str__(self):
        return f"{self.name} v{self.version}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['name', 'version']

class TestResult(models.Model):
    RESULT_STATUS = [
        ('PASS', 'Pass'),
        ('FAIL', 'Fail'),
        ('IN_PROGRESS', 'In Progress'),
        ('INVALID', 'Invalid'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='test_results')
    protocol = models.ForeignKey(TestProtocol, on_delete=models.CASCADE, related_name='test_results')
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performed_tests')
    status = models.CharField(max_length=20, choices=RESULT_STATUS, default='IN_PROGRESS')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    data = models.JSONField(default=dict)  # For storing test-specific data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device.name} - {self.protocol.name} ({self.status})"

    class Meta:
        ordering = ['-created_at']

@receiver(post_save, sender=TestResult)
def notify_admin_on_test_result_creation(sender, instance, created, **kwargs):
    """
    Signal handler to send email notification when a new test result is created.
    """
    if created:
        # Trigger the Celery task asynchronously
        send_test_result_notification.delay(instance.id) 