from django import forms
from django.forms import ModelForm

from core.models import Rank


class RankForm(ModelForm):
    class Meta:
        model = Rank
        fields = "__all__"

        widgets = {"competence_level": forms.HiddenInput()}
