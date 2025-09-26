from django.views.generic import ListView

from core.models import Rank


class RanksView(ListView):
    template_name = "game/ranks.html"

    def get_queryset(self):
        return Rank.objects.prefetch_related("missions", "competence_level__competence").all()

    def get_context_data(self, **kwargs):
        rank = Rank.objects.get(id=self.request.user.rank)
        return super().get_context_data(**kwargs) | {
            "rank": rank,
            "next_rank": Rank.objects.filter(id=self.request.user.rank + 1).first() or rank,
        }
