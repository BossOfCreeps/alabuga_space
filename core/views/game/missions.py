from functools import cached_property

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView

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
        template_name = {
            MissionCode: "game/mission_code.html",
            MissionRecruiting: "game/mission_recruiting.html",
            MissionTeaching: "game/mission_teaching.html",
            MissionQuiz: "game/mission_quiz.html",
        }.get(self.mission.get_real_instance_class())
        return render(request, template_name, {"mission": self.mission})

    def post(self, request, *args, **kwargs):
        mission_type, data = self.mission.get_real_instance_class(), None
        if mission_type == MissionCode:
            return  # TODO
        elif mission_type == MissionRecruiting:
            return  # TODO
        elif mission_type == MissionTeaching:
            data = {}
        elif mission_type == MissionQuiz:
            return  # TODO

        self.mission.verify(self.request.user, **data)
        return redirect(reverse_lazy("missions"))

    @cached_property
    def mission(self) -> Mission:
        return Mission.objects.get(pk=self.kwargs["pk"])


class MissionForceCodeView(FormView):
    form_class = MissionForceCodeForm
    template_name = "hr/mission/force_code.html"
    success_url = reverse_lazy("index")  # TODO:

    def form_valid(self, form):
        data = form.cleaned_data

        if (data["text"] == "" and data["image"] is None) or (data["text"] != "" and data["image"] is not None):
            messages.error(self.request, "Должен быть отправлен текст или изображение")
            return self.form_invalid(form)

        if data["image"] is not None:
            text = decode_qr_from_image(data["image"].read())
        else:
            text = data["text"]

        mission: MissionCode = MissionCode.objects.filter(code=text).first()
        if mission is None:
            messages.error(self.request, "Миссия не найдена")
            return self.form_invalid(form)

        v = mission.verify(self.request.user, text)
        if v is False:
            messages.error(self.request, "Миссия не найдена")
            return self.form_invalid(form)

        return super().form_valid(form)
