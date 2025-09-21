from django.urls import path

from core.views import (
    CompetenceCreateView,
    CompetenceDeleteView,
    CompetenceListView,
    CompetenceUpdateView,
    HrLoginView,
    HrLogoutView,
    IndexView,
    MissionCreateView,
    MissionDeleteView,
    MissionForceCodeView,
    MissionGraphView,
    MissionListView,
    MissionUpdateView,
    PrizeCreateView,
    PrizeDeleteView,
    PrizeListView,
    PrizeUpdateView,
    QuestionCreateView,
    QuestionDeleteView,
    QuestionListView,
    QuestionUpdateView,
    RankCreateView,
    RankDeleteView,
    RankListView,
    RankUpdateView,
)
from core.views.hr.notification import NotificationCheckView, NotificationListView
from core.views.hr.user import UserListView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("mission/force_code/", MissionForceCodeView.as_view(), name="mission-code"),
    #
    path("hr/", HrLoginView.as_view(), name="hr-login"),
    path("hr/logout/", HrLogoutView.as_view(), name="hr-logout"),
    #
    path("hr/ranks/", RankListView.as_view(), name="rank-list"),
    path("hr/hr/ranks/<int:pk>/update/", RankUpdateView.as_view(), name="rank-update"),
    path("hr/ranks/<int:pk>/delete/", RankDeleteView.as_view(), name="rank-delete"),
    path("hr/ranks/create/", RankCreateView.as_view(), name="rank-create"),
    #
    path("hr/competences/", CompetenceListView.as_view(), name="competence-list"),
    path("hr/competences/<int:pk>/update/", CompetenceUpdateView.as_view(), name="competence-update"),
    path("hr/competences/<int:pk>/delete/", CompetenceDeleteView.as_view(), name="competence-delete"),
    path("hr/competences/create/", CompetenceCreateView.as_view(), name="competence-create"),
    #
    path("hr/prize/", PrizeListView.as_view(), name="prize-list"),
    path("hr/prize/<int:pk>/update/", PrizeUpdateView.as_view(), name="prize-update"),
    path("hr/prize/<int:pk>/delete/", PrizeDeleteView.as_view(), name="prize-delete"),
    path("hr/prize/create/", PrizeCreateView.as_view(), name="prize-create"),
    #
    path("hr/mission/", MissionListView.as_view(), name="mission-list"),
    path("hr/mission/<int:pk>/update/", MissionUpdateView.as_view(), name="mission-update"),
    path("hr/mission/<int:pk>/delete/", MissionDeleteView.as_view(), name="mission-delete"),
    path("hr/mission/create/", MissionCreateView.as_view(), name="mission-create"),
    path("hr/mission/graph/", MissionGraphView.as_view(), name="mission-graph"),
    #
    path("hr/mission/question/", QuestionListView.as_view(), name="question-list"),
    path("hr/mission/question/create/", QuestionCreateView.as_view(), name="question-create"),
    path("hr/mission/question/<int:pk>/update/", QuestionUpdateView.as_view(), name="question-update"),
    path("hr/mission/question/<int:pk>/delete/", QuestionDeleteView.as_view(), name="question-delete"),
    #
    path("hr/users/", UserListView.as_view(), name="user-list"),
    #
    path("hr/notifications/", NotificationListView.as_view(), name="notifications-list"),
    path("hr/notifications/<int:pk>/check/", NotificationCheckView.as_view(), name="notifications-check"),
]
