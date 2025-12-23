"""
Этот модуль отвечает за определение форм для обработки пользовательского ввода
в приложении Game_app.
"""

from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "image", "price", "description"]


class SearchForm(forms.Form):
    query = forms.CharField(
        label="Поиск",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Введите название игры..."}),
    )


class ProductFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Все категории",
        label="Категория",
    )
    min_price = forms.DecimalField(
        required=False,
        label="Минимальная цена",
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "0.00"}),
    )
    max_price = forms.DecimalField(
        required=False,
        label="Максимальная цена",
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "1000.00"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get("min_price")
        max_price = cleaned_data.get("max_price")
        if min_price and max_price and min_price > max_price:
            raise forms.ValidationError(
                "Минимальная цена не может превышать максимальную."
            )
        return cleaned_data
