from django import forms
from django.forms import Form


class MissionForceCodeForm(Form):
    image = forms.ImageField(required=False, label="Загрузить QR код")
    text = forms.CharField(required=False, label="Текстовый код")
