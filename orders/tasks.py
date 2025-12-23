import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

logger = logging.getLogger(__name__)


@shared_task
def send_order_confirmation_email(order_id):
    logger.info(f"Задача запущена для заказа {order_id}")
    try:
        order = Order.objects.get(id=order_id)
        logger.info(f"Заказ найден: {order.id}")
        products = [
            getattr(item.product, "name", str(item.product))
            for item in order.orderitem_set.all()
        ]
        products_str = ", ".join(products) if products else "неизвестный продукт"
        logger.info(f"Продукты: {products_str}")

        subject = f"Подтверждение заказа #{order.id}"
        message = f"""
        Здравствуйте, {order.user.username}!

        Ваш заказ на игры "{products_str}" успешно создан.
        Номер заказа: {order.id}
        Сумма: {order.total_price} руб.
        Дата: {order.created_at}

        Спасибо за покупку!
        """
        recipient_list = [order.user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        logger.info(f"Email отправлен для заказа {order_id}")
    except Order.DoesNotExist:
        logger.error(f"Заказ с ID {order_id} не найден.")
    except Exception as e:
        logger.error(f"Ошибка при отправке email для заказа {order_id}: {e}")
        raise
