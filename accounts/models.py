"""
Этот модуль отвечает за определение моделей данных в приложении accounts.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Номер телефона"
    )
    address = models.TextField(blank=True, null=True, verbose_name="Адрес")

    def __str__(self):
        return f"{self.user.username}'s profile"
