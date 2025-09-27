from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from core.forms import LoginForm


class OrgLoginView(FormView):
    form_class = LoginForm
    template_name = "org/login.html"
    success_url = reverse_lazy("org-missions")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_organizer:
            return redirect("org-missions")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        if user.is_organizer:
            login(self.request, user)
            return super().form_valid(form)
        return super().form_invalid(form)


class OrgLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("org-login")
