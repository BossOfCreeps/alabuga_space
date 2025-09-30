from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from core.models import Mission
from core.templatetags.user_logic import get_mission_type


class HRRequiredMixin(LoginRequiredMixin):
    """Миксин для проверки, что пользователь является HR"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not getattr(request.user, "is_hr", False):
            return HttpResponse(status=403)

        return super().dispatch(request, *args, **kwargs)


class OrgRequiredMixin(LoginRequiredMixin):
    """Миксин для проверки, что пользователь является организатором"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not getattr(request.user, "is_organizer", False):
            return HttpResponse(status=403)

        return super().dispatch(request, *args, **kwargs)


class MissionRankMixin(LoginRequiredMixin):
    """Миксин для проверки, что пользователь является миссионером"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        mission = Mission.objects.get(id=kwargs["pk"])
        if mission.rank != request.user.rank or get_mission_type(mission, request.user) != "open":
            return HttpResponse(status=409)

        return super().dispatch(request, *args, **kwargs)
