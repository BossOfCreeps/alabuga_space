from django.contrib import messages
from django.utils.translation import gettext_lazy

from core.models import CompetenceLevel


def show_bootstrap_error_message(form, request):
    error_messages = []
    for field, errors in form.errors.items():
        field_name = form.fields[field].label if field in form.fields else field
        for error in errors:
            error_messages.append(f"{field_name}: {gettext_lazy(error)}")  # TODO: перевод

    for error_msg in error_messages:
        messages.error(request, error_msg)


def parse_competence_levels_map(data):
    return [
        str(CompetenceLevel.objects.get_or_create(competence_id=int(k.split("_")[-1]), level=int(v))[0].id)
        for k, v in data.items()
        if k.startswith("competence_level_")
    ]
