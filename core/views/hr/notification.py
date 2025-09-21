from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView

from users.models import Notification


class NotificationListView(ListView):
    queryset = Notification.objects.all()
    template_name = "hr/notification/list.html"


class NotificationCheckView(View):
    def get(self, request, pk):
        obj = Notification.objects.get(pk=pk)
        obj.is_read = True
        obj.save()
        return redirect("notifications-list")
