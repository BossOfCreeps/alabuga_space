from django.urls import path

from core.views import Index, RankCreateView, RankUpdateView

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("ranks/create/", RankCreateView.as_view(), name="rank-create"),
    path("ranks/<int:pk>/update/", RankUpdateView.as_view(), name="rank-update"),
]
