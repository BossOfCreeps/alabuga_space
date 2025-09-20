from django.contrib import messages
from django.forms import Form
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView

from core.forms import (
    MissionCodeForm,
    MissionForceCodeForm,
    MissionForm,
    MissionQuizForm,
    MissionRecruitingForm,
    MissionTeachingForm,
)
from core.models import Competence, Mission, MissionCode, MissionQuiz, MissionRecruiting, MissionTeaching
from utils.forms import parse_competence_levels_map, show_bootstrap_error_message
from utils.qr import decode_qr_from_image


class MissionMixin(FormView):
    queryset = Mission.objects.all()
    form_class = MissionForm
    template_name = "mission/form.html"
    success_url = reverse_lazy("index")  # TODO:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method in ("POST", "PUT"):
            kwargs["data"] = self.request.POST.dict() | {
                "prizes": self.request.POST.getlist("prizes"),
                "competence_level": parse_competence_levels_map(self.request.POST.dict()),
            }

        return kwargs

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"competences": Competence.objects.all()}

    def form_invalid(self, form):
        show_bootstrap_error_message(form, self.request)
        return super().form_invalid(form)


class MissionCreateView(MissionMixin, CreateView):
    pass


class MissionUpdateView(MissionMixin, UpdateView):
    def get_form_class(self):
        return {
            MissionCode: MissionCodeForm,
            MissionRecruiting: MissionRecruitingForm,
            MissionTeaching: MissionTeachingForm,
            MissionQuiz: MissionQuizForm,
        }.get(self.object.get_real_instance_class())

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            "competence_level_map": {cl.competence.id: cl.level for cl in self.object.competence_level.all()},
        }


class MissionDeleteView(MissionMixin, DeleteView):
    template_name = "mission/delete.html"
    form_class = Form


class MissionForceCodeView(FormView):
    form_class = MissionForceCodeForm
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
