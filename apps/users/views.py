from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetDoneView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse

from .models import Profile, User
from .forms import UserRegisterForm, UserUpdateForm, ProfileRegisterForm
from .roles import role_required, ADMIN


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            reset_password_form = PasswordResetForm(data={'email': email})
            if reset_password_form.is_valid():
                reset_password_form.save(request=request,
                    email_template_name='users/password_define_email.txt',
                    html_email_template_name='users/password_define_email.html')
                messages.success(request,
                    f'Conta criada com sucesso. Consulte a caixa de correio {email} para definir a palavra-passe')
                return redirect('users:login')
            else:
                messages.error(request,
                    'Problemas com o envio de email para definir a password...')
            return redirect('users:login')
        else:
            messages.error(request,
                'Problemas com a criação de conta. Ver informação em baixo...')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'A tua conta foi atualizada!')
            return redirect('users:profile')
        else:
            messages.error(request,
                'Problemas a atualizar a tua conta, vê os erros em baixo...')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
    }
    return render(request, 'users/profile.html', context)


def login_register(request):
    return render(request, 'users/login_register.html')


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'A sua palavra-passe foi definida com sucesso \
            Faça o login agora.')
        return redirect('users:login')

class MyPasswordResetDoneView(PasswordResetDoneView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'Um e-mail acabou de ser enviado com as \
            instruções para redefinir a sua senha... Confirme, por favor.')
        return redirect('users:login')