from django.forms import Form
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, UpdateView

from core.forms import RankForm
from core.models import Competence, CompetenceLevel, Rank
from utils.forms import show_bootstrap_error_message


class RankMixin(FormView):
    queryset = Rank.objects.prefetch_related("missions", "competence_level").all()
    form_class = RankForm
    template_name = "rank/form.html"
    success_url = reverse_lazy("index")  # TODO:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method in ("POST", "PUT"):
            data = self.request.POST.dict()
            data["missions"] = self.request.POST.getlist("missions")
            competence_levels = [
                str(CompetenceLevel.objects.get_or_create(competence_id=int(k.split("_")[-1]), level=int(v))[0].id)
                for k, v in data.items()
                if k.startswith("competence_level_")
            ]
            data["competence_level"] = competence_levels

            kwargs["data"] = data

        return kwargs

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"competences": Competence.objects.all()}

    def form_invalid(self, form):
        show_bootstrap_error_message(form, self.request)
        return super().form_invalid(form)


class RankCreateView(RankMixin, CreateView):
    pass


class RankUpdateView(RankMixin, UpdateView):
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            "competence_level_map": {cl.competence.id: cl.level for cl in self.object.competence_level.all()},
        }


class RankDeleteView(RankMixin, DeleteView):
    template_name = "rank/delete.html"
    form_class = Form
