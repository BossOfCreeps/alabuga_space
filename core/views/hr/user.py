from django.views.generic import ListView

from users.mixins import HRRequiredMixin
from users.models import User


class UserListView(HRRequiredMixin, ListView):
    queryset = User.objects.all()
    template_name = "hr/user/list.html"
