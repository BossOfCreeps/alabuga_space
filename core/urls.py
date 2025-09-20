from django.urls import path

from core.views import (
    CompetenceCreateView,
    CompetenceDeleteView,
    CompetenceUpdateView,
    IndexView,
    MissionCreateView,
    MissionDeleteView,
    MissionForceCodeView,
    MissionGraphView,
    MissionUpdateView,
    PrizeCreateView,
    PrizeDeleteView,
    PrizeUpdateView,
    QuestionCreateView,
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
    #
    # path("prize/", PrizeListView.as_view(), name="prize-list"),
    # path("prize/<int:pk>/", PrizeView.as_view(), name="prize-detail"),
    path("prize/<int:pk>/update/", PrizeUpdateView.as_view(), name="prize-update"),
    path("prize/<int:pk>/delete/", PrizeDeleteView.as_view(), name="prize-delete"),
    path("prize/create/", PrizeCreateView.as_view(), name="prize-create"),
    #
    # path("mission/", MissionListView.as_view(), name="mission-list"),
    # path("mission/<int:pk>/", MissionView.as_view(), name="mission-detail"),
    path("mission/<int:pk>/update/", MissionUpdateView.as_view(), name="mission-update"),
    path("mission/<int:pk>/delete/", MissionDeleteView.as_view(), name="mission-delete"),
    path("mission/create/", MissionCreateView.as_view(), name="mission-create"),
    path("mission/force_code/", MissionForceCodeView.as_view(), name="mission-code"),
    path("mission/graph/", MissionGraphView.as_view(), name="mission-graph"),
    path("mission/question/create/", QuestionCreateView.as_view(), name="question-create"),
]
