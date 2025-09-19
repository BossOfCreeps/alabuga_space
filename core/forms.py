from django import forms
from django.forms import ModelForm

from core.models import Competence, Rank


class RankForm(ModelForm):
    class Meta:
        model = Rank
        fields = "__all__"

        widgets = {"competence_level": forms.HiddenInput()}


class CompetenceForm(ModelForm):
    class Meta:
        model = Competence
        fields = "__all__"
