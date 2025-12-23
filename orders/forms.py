"""
Этот модуль отвечает за определение форм для обработки пользовательского ввода
в приложении orders.
"""

from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Имя")
    surname = forms.CharField(max_length=100, label="Фамилия")
    email = forms.EmailField(label="Электронная почта")
    phone = forms.CharField(max_length=20, label="Номер телефона")
    delivery_method = forms.ChoiceField(
        choices=[("courier", "Курьером"), ("sdek", "СДЭК"), ("pickup", "Самовывоз")]
    )
    payment_method = forms.ChoiceField(
        choices=[
            ("card", "Картой курьеру"),
            ("cash", "Наличными"),
            ("online", "Оплата картой на сайте"),
        ]
    )

    class Meta:
        model = Order
        fields = ["delivery_address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("delivery_address", None)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.delivery_address = (
            f"{self.cleaned_data['name']} {self.cleaned_data['surname']}"
        )
        instance.phone = self.cleaned_data["phone"]
        if commit:
            instance.save()
        return instance
