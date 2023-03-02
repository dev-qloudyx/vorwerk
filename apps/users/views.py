from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
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
                    f'Account created... "{email}" is now able to log in!')
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
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('users:profile')
        else:
            messages.error(request,
                'Problems updating your account, see errors below...')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)