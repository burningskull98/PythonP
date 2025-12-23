"""
Этот модуль отвечает за обработку пользовательских
 запросов и отображение данных в приложении accounts.
"""

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.http import HttpResponse
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from accounts.forms import RegistrationForm, UserLoginForm, ProfileForm
from accounts.models import Profile
from orders.models import Order


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = "accounts/registration.html"
    success_url = reverse_lazy("accounts:profile")


def form_valid(self, form):
    response = super().form_valid(form)
    messages.success(
        self.request, "Регистрация прошла успешно! Теперь войдите в систему."
    )
    return response


def user_login(request):
    """
    Функция для входа пользователя в профиль.
    """
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(
                        "accounts:profile"
                    )
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid username or password")
    else:
        form = UserLoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """
    Функция для выхода пользователя из профиля.
    """
    logout(request)
    messages.success(request, "Вы успешно вышли из профиля.")
    return redirect(
        "accounts:login"
    )


@login_required
def profile_view(request):
    """
    Функция для отображения профиля.
    """
    return render(request, "accounts/profile.html")


@login_required
def profile_edit(request):
    """Редактирование профиля"""
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        user_form = UserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль обновлен!")
            return redirect("accounts:profile")
        else:
            messages.error(
                request, "Ошибка при обновлении профиля. Пожалуйста, проверьте ошибки!"
            )

    else:
        user_form = UserChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )


@login_required
def change_password(request):
    """Изменение пароля"""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Пароль изменен!")
            return redirect("profile")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/change_password.html", {"form": form})


@login_required
def order_history(request):
    """История заказов"""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})
