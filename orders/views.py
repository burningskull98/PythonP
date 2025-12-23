"""
Этот модуль отвечает за обработку пользовательских
 запросов и отображение данных в приложении orders.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm
from .tasks import send_order_confirmation_email


def create_order(request):
    cart = Cart(request)

    if not request.user.is_authenticated:
        messages.warning(
            request,
            "Пожалуйста, войдите в профиль или создайте аккаунт, чтобы оформить заказ.",
        )
        return redirect("accounts:login")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.delivery_address = form.cleaned_data.get("delivery_address", "")
            order.phone = form.cleaned_data.get("phone", "")
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            order.total_price = sum(
                item.get_cost() for item in order.orderitem_set.all()
            )
            order.save(update_fields=["total_price"])

            send_order_confirmation_email.delay(order.id)
            cart.clear()

            if form.cleaned_data.get("payment_method") == "online":
                return redirect(f"/payment/create/?order_id={order.id}")

            return render(request, "orders/order_created.html", {"order": order})
    else:
        form = OrderCreateForm()

    return render(request, "orders/create_order.html", {"cart": cart, "form": form})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_created.html", {"order": order})
