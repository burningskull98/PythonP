"""
Этот модуль отвечает за управление корзиной с покупками в приложении cart.
"""

from decimal import Decimal
from django.conf import settings
from Game_app.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        product_ids_int = []

        for pid in product_ids:
            try:
                if pid:  # Проверяем, что pid не пустой
                    product_ids_int.append(int(pid))
            except ValueError:
                continue

        products = Product.objects.filter(pk__in=product_ids_int)
        for product in products:
            item = self.cart[str(product.pk)]
            item_copy = item.copy()  # Создаем копию, чтобы не изменять self.cart
            item_copy["product"] = product
            item_copy["price"] = Decimal(item["price"])
            item_copy["total_price"] = item_copy["price"] * item["quantity"]
            yield item_copy

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(
            float(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
