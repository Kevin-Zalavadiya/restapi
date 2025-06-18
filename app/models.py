from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('superuser', 'Superuser'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    
    def save(self, *args, **kwargs):
        # Ensure superusers have the superuser role
        if self.is_superuser and self.role != 'superuser':
            self.role = 'superuser'
        # Ensure staff users have at least admin role
        elif self.is_staff and self.role not in ['admin', 'superuser']:
            self.role = 'admin'
        super().save(*args, **kwargs)
    
    @classmethod
    def create_superuser(cls, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superuser')
        return super()._create_user(username, email, password, **extra_fields)

class Tea(models.Model):
    name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)

