from functools import cached_property

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView

from core.forms import MissionForceCodeForm
from core.models import Mission, MissionCode, MissionQuiz, MissionRecruiting, MissionTeaching
from utils.qr import decode_qr_from_image


class MissionsView(ListView):
    template_name = "game/missions.html"

    def get_queryset(self):
        return Mission.objects.prefetch_related("prizes", "competence_level__competence").filter(
            rank=self.request.user.rank
        )


class MissionView(DetailView):
    template_name = "game/mission.html"
    queryset = Mission.objects.prefetch_related("prizes", "competence_level__competence")


class MissionRunView(View):
    def get(self, request, *args, **kwargs):
        template_name, extra_context = {
            MissionCode: ("game/mission_code.html", {"form": MissionForceCodeForm}),
            MissionRecruiting: ("game/mission_recruiting.html", {}),
            MissionTeaching: ("game/mission_teaching.html", {}),
            MissionQuiz: ("game/mission_quiz.html", {}),
        }.get(self.mission.get_real_instance_class())
        return render(request, template_name, {"mission": self.mission} | extra_context)

    def post(self, request, *args, **kwargs):
        mission_type, data = self.mission.get_real_instance_class(), None
        if mission_type == MissionCode:
            form = MissionForceCodeForm(request.POST, request.FILES)
            form.is_valid()
            d = form.cleaned_data

            if (d["text"] == "" and d["image"] is None) or (d["text"] != "" and d["image"] is not None):
                messages.error(self.request, "Должен быть отправлен текст или изображение")
                return self.get(request, *args, **kwargs)

            data = {"code": decode_qr_from_image(d["image"].read()) if d["image"] is not None else d["text"]}

        elif mission_type == MissionRecruiting:
            return  # TODO

        elif mission_type == MissionTeaching:
            data = {}

        elif mission_type == MissionQuiz:
            return  # TODO

        if not self.mission.verify(self.request.user, **data):
            messages.error(self.request, "Миссия не пройдена")
            return self.get(request, *args, **kwargs)

        return redirect(reverse_lazy("missions"))

    @cached_property
    def mission(self) -> Mission:
        return Mission.objects.get(pk=self.kwargs["pk"])
