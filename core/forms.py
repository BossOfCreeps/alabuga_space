from django import forms
from django.forms import Form, ModelForm

from core.models import Competence, Prize, Rank


class RankForm(ModelForm):
    class Meta:
        model = Rank
        fields = "__all__"

        widgets = {"competence_level": forms.HiddenInput()}


class CompetenceForm(ModelForm):
    class Meta:
        model = Competence
        fields = "__all__"


class PrizeForm(ModelForm):
    class Meta:
        model = Prize
        fields = "__all__"


class MissionCodeForm(Form):
    image = forms.ImageField(required=False, label="Загрузить QR код")
    text = forms.CharField(required=False, label="Текстовый код")
