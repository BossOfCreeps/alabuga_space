from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView

from utils.forms import show_bootstrap_error_message

from .forms import UserRegisterForm


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        login(self.request, form.save())
        return super().form_valid(form)

    def form_invalid(self, form):
        show_bootstrap_error_message(form, self.request)
        return super().form_invalid(form)
