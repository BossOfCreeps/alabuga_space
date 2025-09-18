from django.urls import path

from users.views import RegisterView

urlpatterns = [
    path("login/", RegisterView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
]
