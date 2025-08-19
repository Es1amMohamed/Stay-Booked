from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from allauth.account.signals import user_signed_up
from django.dispatch import receiver


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
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

    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = ["username", "phone_number"]
    def __str__(self):
        return self.username


@receiver(user_signed_up)
def set_verified_for_google_signup(request, user, sociallogin=None, **kwargs):
    if user and not user.is_active:
        user.is_active = True
        user.save()