from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "yookassa_id",
        "user",
        "order",
        "amount",
        "currency",
        "status",
        "created_at",
    )
    list_filter = ("status", "currency", "created_at")
    search_fields = ("yookassa_id", "user__username", "order__id")
    readonly_fields = ("yookassa_id", "created_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    def has_change_permission(self, request, obj=None):
        if obj and obj.status == "succeeded":
            return False
        return super().has_change_permission(request, obj)
