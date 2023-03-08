from django import forms
from .models import User, Profile
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    aceito = forms.BooleanField(widget=forms.CheckboxInput(),
                           label=mark_safe('Aceito a <a class="x" href="#">Política de Privacidade</a>'))

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'bimby', 'loja', 'aceito', 'role']
        help_texts = {
            'password1': '',
            'password2': ''
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['password1'].widget.attrs['hidden'] = True
        self.fields['password2'].widget.attrs['hidden'] = True
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['email'].label = 'E-mail'
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['aceito'].required = True


class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'bimby']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True