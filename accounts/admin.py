"""
Этот модуль отвечает за настройку административного интерфейса приложения accounts.
"""

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "address", "birth_date"]
