from django.shortcuts import redirect
from django.views import View


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("missions")
        else:
            return redirect("login")
