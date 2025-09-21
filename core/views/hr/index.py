from django.views.generic import TemplateView


class HrIndexView(TemplateView):
    template_name = "hr/index.html"
