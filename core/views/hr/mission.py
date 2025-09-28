from django.contrib import messages
from django.forms import Form
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, ListView, TemplateView, UpdateView

from core.forms import (
    MissionCodeForm,
    MissionManualForm,
    MissionQuizForm,
    MissionRecruitingForm,
    MissionTeachingForm,
    QuestionForm,
)
from core.models import (
    Answer,
    Competence,
    Mission,
    MissionCode,
    MissionManual,
    MissionQuiz,
    MissionRecruiting,
    MissionTeaching,
    MissionTree,
    Question,
    Rank,
)
from users.mixins import HRRequiredMixin
from utils.forms import parse_competence_levels_map, show_bootstrap_error_message


class MissionMixin(HRRequiredMixin, FormView):
    queryset = Mission.objects.prefetch_related("competence_level__competence", "prizes").all()
    template_name = "hr/mission/form.html"
    success_url = reverse_lazy("mission-list")

    def get_form_class(self):
        if hasattr(self, "object") and self.object is not None:
            return {
                MissionCode: MissionCodeForm,
                MissionRecruiting: MissionRecruitingForm,
                MissionTeaching: MissionTeachingForm,
                MissionQuiz: MissionQuizForm,
                MissionManual: MissionManualForm,
            }.get(self.object.get_real_instance_class())

        return {
            "c": MissionCodeForm,
            "r": MissionRecruitingForm,
            "t": MissionTeachingForm,
            "q": MissionQuizForm,
            "m": MissionManualForm,
            None: Form,
        }.get(self.request.GET.get("type"))

    def get_initial(self):
        initial = super().get_initial()
        if hasattr(self, "object") and self.object is not None:
            initial["childrens"] = Mission.objects.filter(
                id__in=MissionTree.objects.filter(parent=self.object).values_list("child", flat=True)
            )
            initial["parents"] = Mission.objects.filter(
                id__in=MissionTree.objects.filter(child=self.object).values_list("parent", flat=True)
            )
        return initial

    def form_valid(self, form):
        self.object = form.save()

        MissionTree.objects.filter(parent=self.object).delete()
        for child in self.request.POST.getlist("childrens"):
            MissionTree.objects.create(parent=self.object, child_id=child)

        MissionTree.objects.filter(child=self.object).delete()
        for parent in self.request.POST.getlist("parents"):
            MissionTree.objects.create(child=self.object, parent_id=parent)

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method in ("POST", "PUT"):
            kwargs["data"] = self.request.POST.dict() | {
                "prizes": self.request.POST.getlist("prizes"),
                "parents": self.request.POST.getlist("parents"),
                "childrens": self.request.POST.getlist("childrens"),
                "competence_level": parse_competence_levels_map(self.request.POST.dict()),
                #
                "questions": self.request.POST.getlist("questions"),
                "organizers": self.request.POST.getlist("organizers"),
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


class MissionGraphView(HRRequiredMixin, TemplateView):
    template_name = "hr/mission/graph.html"

    def get_queryset(self):
        if "rank" in self.request.GET:
            return Mission.objects.filter(rank=self.request.GET["rank"])

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"object_list": self.get_queryset(), "ranks": Rank.objects.all()}


class QuestionMixin(HRRequiredMixin, FormView):
    queryset = Question.objects.prefetch_related("answers").all()
    form_class = QuestionForm
    template_name = "hr/mission/question_form.html"
    success_url = reverse_lazy("question-list")

    def form_valid(self, form):
        data = self.request.POST.dict()

        has_answer = False
        for k, v in data.items():
            if k.startswith("answer_correct_"):
                has_answer = True
                break

        if not has_answer:
            messages.error(self.request, "Вопрос должен иметь хотя бы один правильный ответ")
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
