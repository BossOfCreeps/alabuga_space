from django.forms import Form
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, UpdateView

from core.forms import CompetenceForm
from core.models import Competence
from utils.forms import show_bootstrap_error_message


class CompetenceMixin(FormView):
    queryset = Competence.objects.all()
    form_class = CompetenceForm
    template_name = "competence/form.html"
    success_url = reverse_lazy("index")  # TODO:

    def form_invalid(self, form):
        show_bootstrap_error_message(form, self.request)
        return super().form_invalid(form)


class CompetenceCreateView(CompetenceMixin, CreateView):
    pass


class CompetenceUpdateView(CompetenceMixin, UpdateView):
    pass


class CompetenceDeleteView(CompetenceMixin, DeleteView):
    template_name = "competence/delete.html"
    form_class = Form
