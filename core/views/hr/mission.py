from django.contrib import messages
from django.forms import Form
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView

from core.forms import MissionCodeForm, MissionQuizForm, MissionRecruitingForm, MissionTeachingForm, QuestionForm
from core.models import (
    Answer,
    Competence,
    Mission,
    MissionCode,
    MissionQuiz,
    MissionRecruiting,
    MissionTeaching,
    Question,
)
from utils.forms import parse_competence_levels_map, show_bootstrap_error_message


class MissionMixin(FormView):
    queryset = Mission.objects.all()
    template_name = "hr/mission/form.html"
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


class MissionListView(MissionMixin, ListView):
    template_name = "hr/mission/list.html"


class MissionCreateView(MissionMixin, CreateView):
    pass


class MissionUpdateView(MissionMixin, UpdateView):
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            "competence_level_map": {cl.competence.id: cl.level for cl in self.object.competence_level.all()},
        }


class MissionDeleteView(MissionMixin, DeleteView):
    template_name = "hr/mission/delete.html"
    form_class = Form


class MissionGraphView(ListView):
    template_name = "hr/mission/graph.html"
    queryset = Mission.objects.all()


class QuestionMixin(FormView):
    queryset = Question.objects.all()
    form_class = QuestionForm
    template_name = "hr/mission/question_form.html"
    success_url = reverse_lazy("index")  # TODO:

    def form_valid(self, form):
        data = self.request.POST.dict()

        has_answer = False
        for k, v in data.items():
            if k.startswith("answer_text_") and v:
                has_answer = True
                break

        if not has_answer:
            messages.error(self.request, "Вопрос должен иметь хотя бы один ответ")
            return self.form_invalid(form)

        self.object = form.save()
        self.object.answers.all().delete()

        for k, v in data.items():
            if k.startswith("answer_text_"):
                self.object.answers.add(
                    Answer.objects.create(
                        question=self.object, text=v, is_correct=k.replace("answer_text_", "answer_correct_") in data
                    )
                )
        self.object.save()

        return super().form_valid(form)


class QuestionListView(QuestionMixin, ListView):
    template_name = "hr/mission/question_list.html"


class QuestionCreateView(QuestionMixin, CreateView):
    pass


class QuestionUpdateView(QuestionMixin, UpdateView):
    pass


class QuestionDeleteView(QuestionMixin, DeleteView):
    template_name = "hr/mission/question_delete.html"
    form_class = Form
