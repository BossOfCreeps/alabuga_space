from django.contrib import messages
from django.forms import Form
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from core.forms import (
    MissionCodeForm,
    MissionForceCodeForm,
    MissionQuizForm,
    MissionRecruitingForm,
    MissionTeachingForm,
    QuestionForm,
)
from core.models import Competence, Mission, MissionCode, MissionQuiz, MissionRecruiting, MissionTeaching, Question
from utils.forms import parse_competence_levels_map, show_bootstrap_error_message
from utils.qr import decode_qr_from_image


class MissionMixin(ModelFormMixin, ProcessFormView):
    queryset = Mission.objects.all()
    template_name = "mission/form.html"
    success_url = reverse_lazy("index")  # TODO:

    def get_form_class(self):
        if self.object is not None:
            return {
                MissionCode: MissionCodeForm,
                MissionRecruiting: MissionRecruitingForm,
                MissionTeaching: MissionTeachingForm,
                MissionQuiz: MissionQuizForm,
            }.get(self.object.get_real_instance_class())

        return {
            "c": MissionCodeForm,
            "r": MissionRecruitingForm,
            "t": MissionTeachingForm,
            "q": MissionQuizForm,
        }.get(self.request.GET.get("type"))

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
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            "competence_level_map": {cl.competence.id: cl.level for cl in self.object.competence_level.all()},
        }


class MissionDeleteView(MissionMixin, DeleteView):
    template_name = "mission/delete.html"
    form_class = Form


class MissionForceCodeView(FormView):
    form_class = MissionForceCodeForm
    template_name = "mission/force_code.html"
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


class MissionGraphView(ListView):
    template_name = "mission/graph.html"
    queryset = Mission.objects.all()


class QuestionMixin(ModelFormMixin, ProcessFormView):
    queryset = Question.objects.all()
    form_class = QuestionForm
    template_name = "mission/question_form.html"
    success_url = reverse_lazy("index")  # TODO:


class QuestionCreateView(QuestionMixin, CreateView):
    pass


class QuestionUpdateView(QuestionMixin, UpdateView):
    pass


class QuestionDeleteView(QuestionMixin, DeleteView):
    template_name = "mission/question_delete.html"
    form_class = Form
