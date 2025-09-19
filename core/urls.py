from django.urls import path

from core.views import (
    CompetenceCreateView,
    CompetenceDeleteView,
    CompetenceUpdateView,
    IndexView,
    RankCreateView,
    RankDeleteView,
    RankUpdateView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    #
    # path("ranks/", RankListView.as_view(), name="rank-list"),
    # path("ranks/<int:pk>/", RankDetailView.as_view(), name="rank-detail"),
    path("ranks/<int:pk>/update/", RankUpdateView.as_view(), name="rank-update"),
    path("ranks/<int:pk>/delete/", RankDeleteView.as_view(), name="rank-delete"),
    path("ranks/create/", RankCreateView.as_view(), name="rank-create"),
    #
    # path("competences/", CompetenceListView.as_view(), name="competence-list"),
    # path("competences/<int:pk>/", CompetenceDetailView.as_view(), name="competence-detail"),
    path("competences/<int:pk>/update/", CompetenceUpdateView.as_view(), name="competence-update"),
    path("competences/<int:pk>/delete/", CompetenceDeleteView.as_view(), name="competence-delete"),
    path("competences/create/", CompetenceCreateView.as_view(), name="competence-create"),
]
