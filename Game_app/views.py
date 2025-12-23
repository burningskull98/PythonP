"""
Этот модуль отвечает за обработку
пользовательских запросов и отображение данных в приложении Game_app.
"""

from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from cart.forms import CartAddProductForm
from .models import Product
from .forms import SearchForm, ProductFilterForm



class ProductListView(ListView):
    """
    Представление для отображения списка продуктов.
    """

    model = Product
    template_name = "Game_app/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all().order_by("-created_at")
        form = ProductFilterForm(self.request.GET)
        if form.is_valid():
            category = form.cleaned_data.get("category")
            min_price = form.cleaned_data.get("min_price")
            max_price = form.cleaned_data.get("max_price")

            if category:
                queryset = queryset.filter(category=category)

            if min_price is not None:
                queryset = queryset.filter(price__gte=min_price)

            if max_price is not None:
                queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = ProductFilterForm(self.request.GET)
        context["form"] = CartAddProductForm()
        return context


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_add_form = CartAddProductForm()
    return render(
        request,
        "Game_app/product_detail.html",
        {"product": product, "cart_add_form": cart_add_form},
    )


def product_search(request):
    form = SearchForm(request.GET)
    results = []
    query = ""

    if form.is_valid():
        query = form.cleaned_data["query"]
        if query:
            results = (
                Product.objects.filter(
                    Q(name__icontains=query) | Q(description__icontains=query)
                )
                .distinct()
                .order_by("-rating")
            )

    context = {
        "form": form,
        "query": query,
        "results": results,
    }
    return render(request, "Game_app/search_results.html", context)


def about_us(request):
    return render(request, "Game_app/about_us.html")


def contacts(request):
    return render(request, "Game_app/contacts.html")


def terms_of_return(request):
    return render(request, "Game_app/terms_of_return.html")


def delivery(request):
    return render(request, "Game_app/delivery.html")
