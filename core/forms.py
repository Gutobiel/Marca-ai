from django import forms
from django.contrib.auth.models import User
from .models import Partida, Quadra

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2


class PartidaForm(forms.ModelForm):
    class Meta:
        model = Partida
        fields = ['esporte', 'data', 'horario', 'max_participantes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }


class QuadraForm(forms.ModelForm):
    class Meta:
        model = Quadra
        fields = ['local', 'descricao', 'latitude', 'longitude']