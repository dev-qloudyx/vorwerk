from django import forms

from .models import Inscricao

from apps.eventos.models import Inscricao
from apps.users.models import User


class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.initial['user'] = user