"""
Этот модуль отвечает за определение моделей данных в приложении Game_app.
"""

from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=150, verbose_name="Название категории", default="", null=True
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="Название товара", null=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    characteristic = models.TextField(blank=True, verbose_name="Характеристика")
    image = models.ImageField(
        upload_to="product_im", blank=True, verbose_name="Изображение"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Game_app:product_detail", args=[self.pk])
