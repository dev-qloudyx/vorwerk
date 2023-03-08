from django import forms

from .models import Evento, Inscricao

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

class GenerateBBCodeForm(forms.Form):
    code = forms.CharField(label='', max_length=10)

class SelectCodesForm(forms.Form):
    num_codes = forms.IntegerField(min_value=1, max_value=10000)
    event = forms.ModelChoiceField(queryset=Evento.objects.all())

class StoreCodesForm(forms.Form):
    #num_codes = forms.IntegerField(min_value=1, max_value=100000)
    event = forms.ModelChoiceField(queryset=Evento.objects.all())
    excel_file = forms.FileField()

class RewardsForm(forms.Form):
    #num_codes = forms.IntegerField(min_value=1, max_value=100000)
    event = forms.ModelChoiceField(queryset=Evento.objects.all())
    excel_file = forms.FileField()