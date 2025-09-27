from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView

from core.models import MissionManual
from users.mixins import OrgRequiredMixin
from users.models import User


class OrgMissionsView(OrgRequiredMixin, ListView):
    template_name = "org/list.html"

    def get_queryset(self):
        return MissionManual.objects.filter(organizers=self.request.user)


class OrgMissionView(OrgRequiredMixin, DetailView):
    template_name = "org/detail.html"

    def get_queryset(self):
        return MissionManual.objects.filter(organizers=self.request.user)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"users": User.objects.all()}


class OrgMissionCheckView(OrgRequiredMixin, View):
    def get(self, request, pk):
        MissionManual.objects.get(pk=pk).do_success(User.objects.get(pk=request.GET.get("user_id")))
        return redirect("org-mission", pk=pk)
