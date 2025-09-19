from django.forms import Form
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, UpdateView

from core.forms import PrizeForm
from core.models import Prize
from utils.forms import show_bootstrap_error_message


class PrizeMixin(FormView):
    queryset = Prize.objects.all()
    form_class = PrizeForm
    template_name = "prize/form.html"
    success_url = reverse_lazy("index")  # TODO:

    def form_invalid(self, form):
        show_bootstrap_error_message(form, self.request)
        return super().form_invalid(form)


class PrizeCreateView(PrizeMixin, CreateView):
    pass


class PrizeUpdateView(PrizeMixin, UpdateView):
    pass


class PrizeDeleteView(PrizeMixin, DeleteView):
    template_name = "prize/delete.html"
    form_class = Form
