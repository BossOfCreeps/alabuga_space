from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from core.forms import LoginForm


class HrLoginView(FormView):
    form_class = LoginForm
    template_name = "hr/login.html"
    success_url = reverse_lazy("rank-list")

    def form_valid(self, form):
        # Выполняем стандартную аутентификацию
        response = super().form_valid(form)
        # Дополнительные действия после успешного входа
        return response


class HrLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("hr-login")
