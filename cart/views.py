"""
Этот модуль отвечает за обработку пользовательских запросов и отображение данных в приложении cart.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from Game_app.models import Product
from .cart import Cart


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart(request)
    quantity = int(request.POST.get("quantity", 1))
    cart.add(product, quantity)
    return redirect("cart:cart")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    cart.remove(product)
    return redirect("cart:cart")


@require_POST
def update_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get("quantity", 1))
    cart.add(
        product, quantity, update_quantity=True
    )
    return redirect("cart:cart")


def cart_view(request):
    cart = Cart(request)
    total_price = float(
        cart.get_total_price()
    )
    return render(request, "cart/cart.html", {"cart": cart, "total_price": total_price})
