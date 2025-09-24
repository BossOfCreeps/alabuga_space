from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, TemplateView

from core.models import Prize, Rank
from users.models import Journal


class ProfileView(TemplateView):
    template_name = "game/profile.html"

    def get_context_data(self, **kwargs):
        rank = Rank.objects.get(id=self.request.user.rank)
        return super().get_context_data(**kwargs) | {
            "rank": rank,
            "next_rank": Rank.objects.filter(id=self.request.user.rank + 1).first() or rank,
        }


class JournalView(ListView):
    template_name = "game/journal.html"
    model = Journal

    def get_queryset(self):
        return Journal.objects.filter(user=self.request.user)


class ShopView(ListView):
    template_name = "game/shop.html"
    queryset = Prize.objects.filter(is_buying=True)


class ShopBuyView(View):
    def get(self, request, pk):
        prize = Prize.objects.get(id=pk)
        if request.user.mana >= prize.price:
            request.user.mana -= prize.price
            request.user.save()
            Journal.objects.create(user=request.user, text=f"Куплен артефакт {prize.name}")

        return redirect("profile")
