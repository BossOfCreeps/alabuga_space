from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from core.forms import LoginForm


class HrLoginView(FormView):
    form_class = LoginForm
    template_name = "hr/login.html"
    success_url = reverse_lazy("rank-list")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_hr:
            return redirect("rank-list")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        if user.is_hr:
            login(self.request, user)
            return super().form_valid(form)
        return super().form_invalid(form)


class HrLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("hr-login")


class ChangeThemeView(View):
    def get(self, request):
        self.request.user.theme = "dark" if self.request.user.theme == "light" else "light"
        self.request.user.save()
        return redirect(request.META.get("HTTP_REFERER"))
