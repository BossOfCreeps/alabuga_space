from django.views.generic import ListView

from core.models import Rank


class RanksView(ListView):
    template_name = "game/ranks.html"

    def get_queryset(self):
        return Rank.objects.prefetch_related("missions", "competence_level__competence").all()
