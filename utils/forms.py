from django.contrib import messages
from django.utils.translation import gettext_lazy


def show_bootstrap_error_message(form, request):
    error_messages = []
    for field, errors in form.errors.items():
        field_name = form.fields[field].label if field in form.fields else field
        for error in errors:
            error_messages.append(f"{field_name}: {gettext_lazy(error)}")  # TODO: перевод

    for error_msg in error_messages:
        messages.error(request, error_msg)
