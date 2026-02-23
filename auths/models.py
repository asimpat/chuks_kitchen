from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),

    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer'
    )

    email = models.EmailField(unique=True, null=True, blank=True)

    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)

    referral_code = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    otp = models.CharField(max_length=6, null=True, blank=True)

    otp_created_at = models.DateTimeField(null=True, blank=True)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.email or self.phone or self.username
