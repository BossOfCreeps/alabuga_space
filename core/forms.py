from django import forms
from django.forms import Form, ModelForm

from core.models import (
    Competence,
    Mission,
    MissionCode,
    MissionQuiz,
    MissionRecruiting,
    MissionTeaching,
    Prize,
    Question,
    Rank,
)


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
    childrens = forms.ModelMultipleChoiceField(Mission.objects.all(), label="Дочерние миссии", required=False)

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


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"


class MissionForceCodeForm(Form):
    image = forms.ImageField(required=False, label="Загрузить QR код")
    text = forms.CharField(required=False, label="Текстовый код")
