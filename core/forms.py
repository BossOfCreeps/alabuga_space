from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
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


class LoginForm(AuthenticationForm):
    # username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Логин"}))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Пароль"}))
    pass


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(self, "instance") and self.instance and self.instance.pk:
            self.fields["childrens"].queryset = Mission.objects.filter(
                Q(rank=self.instance.rank), ~Q(id=self.instance.id)
            )

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
