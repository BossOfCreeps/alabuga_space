from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import FormView

from .forms import UserRegisterForm


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        login(self.request, form.save())
        return super().form_valid(form)

    def form_invalid(self, form):
        error_messages = []
        for field, errors in form.errors.items():
            field_name = form.fields[field].label if field in form.fields else field
            for error in errors:
                error_messages.append(f"{field_name}: {gettext_lazy(error)}")  # TODO: перевод

        for error_msg in error_messages:
            messages.error(self.request, error_msg)

        return super().form_invalid(form)
