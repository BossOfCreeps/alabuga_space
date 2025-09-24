from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from core.forms import MissionForceCodeForm
from core.models import Mission, MissionCode
from utils.qr import decode_qr_from_image


class MissionsView(ListView):
    template_name = "game/missions.html"

    def get_queryset(self):
        return Mission.objects.prefetch_related("prizes", "competence_level").filter(rank=self.request.user.rank)


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
