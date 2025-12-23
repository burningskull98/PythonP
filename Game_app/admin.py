"""
Этот модуль отвечает за настройку административного интерфейса приложения Game_app.
"""

from django.contrib import admin
from .models import Product, Category
from .forms import ProductForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name", "description"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "image",
        "characteristic",
        "price",
        "rating",
        "category",
        "created_at",
    )
    ordering = (
        "category",
        "created_at",
    )
    list_filter = ("name", "price")
    search_fields = ("name", "description")
    search_help_text = "Поиск по названию и категории"

    @admin.action(description="Изменить цену")
    def change_price(self, request, queryset):
        """
        Изменяет цену для выбранных объектов в queryset.
        """
        for product in queryset:
            product.price += 100
            product.price -= 100
            product.save()
        self.message_user(request, "Цена успешно изменилась")

    @admin.action(description="Опубликовать выбранный товар")
    def publish_product(self, request, queryset):
        """
        Публикует выбранные продукты из queryset.
        """
        queryset.update(is_published=True)
        self.message_user(request, "Выбранные товары успешно опубликованы.")

    @admin.action(description="Добавить изображение")
    def add_image(self, request, queryset):
        """
        Добавляет изображение для выбранных объектов в queryset.
        """
        if "apply" in request.POST:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data["image"]
                for product in queryset:
                    product.image = image
                    product.save()
                self.message_user(
                    request, "Изображения успешно добавлены к выбранным товарам."
                )


actions = ["change_price", "publish_product", "add_image"]
