"""
Этот модуль отвечает за маршрутизацию URL в приложении payment.
"""

from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("create/", views.create_payment, name="create_payment"),
    path("callback/", views.payment_callback, name="payment_callback"),
    path("success/", views.payment_success, name="payment_success"),
]
