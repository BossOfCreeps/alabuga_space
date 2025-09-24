from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from core.forms import LoginForm
from users.forms import UserRegisterForm
from utils.forms import show_bootstrap_error_message


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("missions")
        else:
            return redirect("login")


class LoginView(FormView):
    form_class = LoginForm
    template_name = "game/login.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        login(
            self.request, authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        )
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("index")


class RegisterView(FormView):
    template_name = "game/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        login(self.request, form.save())
        return super().form_valid(form)

    def form_invalid(self, form):
        show_bootstrap_error_message(form, self.request)
        return super().form_invalid(form)
