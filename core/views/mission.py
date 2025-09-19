from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from core.forms import MissionCodeForm
from core.models import Mission
from utils.qr import decode_qr_from_image


class MissionCodeView(FormView):
    form_class = MissionCodeForm
    template_name = "mission/code.html"
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

        print(text)

        return super().form_valid(form)


class MissionGraphView(ListView):
    template_name = "mission/graph.html"
    queryset = Mission.objects.all()
