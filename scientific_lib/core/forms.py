from django import forms

from .models import Arquivos


class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivos
        fields = ["name", "tipo", "data"]

