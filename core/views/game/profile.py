from django.views.generic import ListView, TemplateView

from core.models import Rank
from users.models import Journal


class ProfileView(TemplateView):
    template_name = "game/profile.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            "rank": Rank.objects.get(id=self.request.user.rank),
            "next_rank": Rank.objects.filter(id=self.request.user.rank + 1).first(),
        }


class JournalView(ListView):
    template_name = "game/journal.html"
    model = Journal

    def get_queryset(self):
        return Journal.objects.filter(user=self.request.user)
