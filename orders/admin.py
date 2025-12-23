"""
Этот модуль отвечает за настройку административного интерфейса приложения orders.
"""

from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_price",
        "status",
        "created_at",
        "delivery_address",
        "phone",
    )
    list_filter = ("status", "created_at")
    search_fields = ("id", "user__username", "delivery_address", "phone")
    readonly_fields = (
        "created_at",
        "updated_at",
        "total_price",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    actions = ["mark_as_paid", "mark_as_shipped"]

    def mark_as_paid(self, request, queryset):
        queryset.update(status="paid")
        self.message_user(request, "Выбранные заказы отмечены как оплаченные.")

    mark_as_paid.short_description = "Отметить как оплаченные"

    def mark_as_shipped(self, request, queryset):
        queryset.update(status="shipped")
        self.message_user(request, "Выбранные заказы отмечены как отправленные.")

    mark_as_shipped.short_description = "Отметить как отправленные"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "price", "quantity", "get_cost")
    list_filter = ("order__status", "product")
    search_fields = ("order__id", "product__name")
    readonly_fields = ("get_cost",)
    ordering = ("order",)
