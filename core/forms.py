from django import forms
from django.forms import Form, ModelForm

from core.models import Competence, Mission, MissionCode, MissionQuiz, MissionRecruiting, MissionTeaching, Prize, Rank


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


class MissionForm(ModelForm):
    class Meta:
        model = Mission
        fields = "__all__"
        widgets = {"competence_level": forms.HiddenInput()}


class MissionCodeForm(MissionForm):
    class Meta:
        model = MissionCode
        fields = "__all__"
        widgets = {"competence_level": forms.HiddenInput()}


class MissionRecruitingForm(MissionForm):
    class Meta:
        model = MissionRecruiting
        fields = "__all__"
        widgets = {"competence_level": forms.HiddenInput()}


class MissionTeachingForm(MissionForm):
    class Meta:
        model = MissionTeaching
        fields = "__all__"
        widgets = {"competence_level": forms.HiddenInput()}


class MissionQuizForm(MissionForm):
    class Meta:
        model = MissionQuiz
        fields = "__all__"
        widgets = {"competence_level": forms.HiddenInput()}


class MissionForceCodeForm(Form):
    image = forms.ImageField(required=False, label="Загрузить QR код")
    text = forms.CharField(required=False, label="Текстовый код")
