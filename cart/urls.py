"""
Этот модуль отвечает за маршрутизацию URL в приложении cart.
"""

from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_view, name="cart"),
    path(
        "add/<int:product_id>/", views.add_to_cart, name="add_to_cart"
    ),
    path(
        "remove/<int:product_id>/", views.cart_remove, name="remove_from_cart"
    ),
    path(
        "update/<int:product_id>/", views.update_cart, name="update_cart"
    ),
]
