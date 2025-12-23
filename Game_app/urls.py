"""
Этот модуль отвечает за маршрутизацию URL в приложении Game_app.
"""

from django.urls import path
from . import views

app_name = "Game_app"

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name="products"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("search_results/", views.product_search, name="search_results"),
    path("about/", views.about_us, name="about_us"),
    path("contacts/", views.contacts, name="contacts"),
    path("terms_of_return/", views.terms_of_return, name="terms_of_return"),
    path("delivery/", views.delivery, name="delivery"),
]
