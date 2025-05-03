from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class Role(models.Model):
    ROLE_CHOICES = [
        ('MANAGER', 'Manager'),
        ('ENGINEER', 'Engineer'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
    
    def __str__(self):
        return self.get_name_display()

class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display() if self.role else 'No Role'})"
    
    def get_role_display(self):
        return self.role.get_name_display() if self.role else 'No Role'
    
    def is_manager(self):
        return self.role and self.role.name == 'MANAGER'
    
    def is_engineer(self):
        return self.role and self.role.name == 'ENGINEER'
    
    def has_device_access(self, device):
        if self.is_manager():
            return True
        elif self.is_engineer():
            return device.assigned_to == self
        return False 