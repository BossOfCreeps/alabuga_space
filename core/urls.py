from django.urls import path

from core.views import Index, RankCreateView

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("ranks/create/", RankCreateView.as_view(), name="rank-create"),
]
