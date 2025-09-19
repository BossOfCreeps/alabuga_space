from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from core.forms import RankForm
from core.models import Competence, CompetenceLevel, Rank
from utils.forms import show_bootstrap_error_message


class Index(TemplateView):
    template_name = "index.html"


class RankCreateView(CreateView):
    queryset = Rank.objects.prefetch_related("missions", "competence_level").all()
    form_class = RankForm
    template_name = "rank/form.html"
    success_url = reverse_lazy("index")  # TODO:

    def get_form_kwargs(self):
        kwargs = {"initial": self.get_initial(), "prefix": self.get_prefix()}

        if self.request.method in ("POST", "PUT"):
            data = self.request.POST.dict()
            data["missions"] = self.request.POST.getlist("missions")
            competence_levels = [
                str(CompetenceLevel.objects.get_or_create(competence_id=int(k.split("_")[-1]), level=int(v))[0].id)
                for k, v in data.items()
                if k.startswith("competence_level_")
            ]
            data["competence_level"] = competence_levels

            kwargs.update({"data": data, "files": self.request.FILES})
        return kwargs

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"competences": Competence.objects.all()}

    def form_invalid(self, form):
        show_bootstrap_error_message(form, self.request)
        return super().form_invalid(form)
