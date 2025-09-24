from django.views.generic import TemplateView

from core.models import Rank


class ProfileView(TemplateView):
    template_name = "game/profile.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            "rank": Rank.objects.get(id=self.request.user.rank),
            "next_rank": Rank.objects.filter(id=self.request.user.rank + 1).first(),
        }
