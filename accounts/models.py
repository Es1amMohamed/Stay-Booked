from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from rooms.models import *
from allauth.account.signals import user_signed_up
from django.dispatch import receiver


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('normal', 'Normal User'),
        ('hotel_manager', 'Hotel Manager'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='normal')

    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = ["username", "phone_number"]
    def __str__(self):
        return f"{self.username} ({self.role})"


class HotelManagment(CustomUser):
    hotel = models.ForeignKey("rooms.Hotel", on_delete=models.CASCADE)

@receiver(user_signed_up)
def set_verified_for_google_signup(request, user, sociallogin=None, **kwargs):
    if user and not user.is_active:
        user.is_active = True
        user.save()

