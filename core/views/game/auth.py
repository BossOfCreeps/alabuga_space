from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.forms import LoginForm
from users.forms import UserRegisterForm
from utils.forms import show_bootstrap_error_message


class LoginView(FormView):
    form_class = LoginForm
    template_name = "game/login.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        login(
            self.request, authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        )
        return super().form_valid(form)


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
