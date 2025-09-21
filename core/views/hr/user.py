from django.views.generic import ListView

from users.models import User


class UserListView(ListView):
    queryset = User.objects.all()
    template_name = "hr/user/list.html"
