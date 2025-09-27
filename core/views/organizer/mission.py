from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView

from core.models import MissionManual
from users.mixins import OrgRequiredMixin


class OrgMissionsView(OrgRequiredMixin, ListView):
    queryset = MissionManual.objects.all()
    template_name = "org/list.html"


class OrgMissionView(DetailView):
    queryset = MissionManual.objects.all()
    template_name = "org/detail.html"


class OrgMissionCheckView(OrgRequiredMixin, View):
    def get(self, request, pk):
        _ = MissionManual.objects.get(pk=pk)
        return redirect("org-missions")
