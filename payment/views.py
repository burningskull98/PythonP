"""
Этот модуль отвечает за обработку пользовательских
 запросов и отображение данных в приложении payment.
"""

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import yookassa
from .models import Payment
from orders.models import Order
from yookassa import Configuration, Payment as YooPayment

Configuration.configure(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)
Configuration.test_mode = settings.YOOKASSA_TEST_MODE


@login_required
def create_payment(request):
    if request.method == "GET" and "order_id" in request.GET:
        order_id = request.GET.get("order_id")
        try:
            order = Order.objects.get(id=order_id, user=request.user, status="pending")
        except Order.DoesNotExist:
            return redirect("orders:order_list")

        amount = order.total_price
        payment_data = {
            "amount": {"value": str(amount), "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": request.build_absolute_uri("/payment/success/"),
            },
            "capture": True,
            "description": f"Оплата заказа {order.id} в магазине игр",
        }
        payment = YooPayment.create(payment_data)

        Payment.objects.create(
            user=request.user,
            order=order,
            yookassa_id=payment.id,
            amount=amount,
            status=payment.status,
        )
        request.session["payment_id"] = payment.id
        return redirect(payment.confirmation.confirmation_url)

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        try:
            order = Order.objects.get(id=order_id, user=request.user, status="pending")
        except Order.DoesNotExist:
            return redirect("orders:order_list")

        amount = order.total_price
        payment_data = {
            "amount": {"value": str(amount), "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": request.build_absolute_uri("/payment/success/"),
            },
            "capture": True,
            "description": f"Оплата заказа {order.id} в магазине игр",
        }
        payment = YooPayment.create(payment_data)

        Payment.objects.create(
            user=request.user,
            order=order,
            yookassa_id=payment.id,
            amount=amount,
            status=payment.status,
        )
        request.session["payment_id"] = payment.id
        return redirect(payment.confirmation.confirmation_url)

    orders = Order.objects.filter(user=request.user, status="pending")
    return render(request, "payment/create.html", {"orders": orders})


@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        event_json = request.body.decode("utf-8")
        try:
            notification = yookassa.WebhookNotification(event_json)
            payment_id = notification.object.id
            status = notification.object.status

            payment = Payment.objects.get(yookassa_id=payment_id)
            payment.status = status
            payment.save()

            if status == "succeeded":
                payment.order.status = "paid"
                payment.order.save()

            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)


def payment_success(request):
    payment_id = request.session.get("payment_id")
    if not payment_id:
        return redirect("orders:order_list")
    try:
        payment = Payment.objects.get(yookassa_id=payment_id, user=request.user)
        context = {
            "payment_id": payment.yookassa_id,
            "amount": payment.amount,
            "date": payment.created_at.strftime("%Y-%m-%d %H:%M"),
            "order": payment.order,
        }
        return render(request, "payment/success.html", context)
    except Payment.DoesNotExist:
        return redirect("orders:order_list")
