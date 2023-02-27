from django.shortcuts import render
from django.views.generic import CreateView
from .models import Inscricao, Evento
from .forms import InscricaoForm
from django.urls import reverse_lazy, reverse

def detalhe_inscricao(request):
    user = request.user
    i = Inscricao.objects.filter(user=user)
    if i:
        inscricao = i[0]
        separar = inscricao.subevento.local.coordenadas.split()
        coo1 = separar[0][0:15]
        coo2 = separar[1][0:15]
    else:
        i=" "
        separar=" "
        coo1 = " "
        coo2 = " "
    return render(request, 'eventos/inscricao.html', context={'user':user, 'inscricao':inscricao, 'coo1':coo1, 'coo2':coo2})

class NovaInscricao(CreateView):
    form_class = InscricaoForm
    model = Inscricao

    def get(self, request):
        self.user = request.user
        return super().get(request)

    def post(self, request):
        self.user = request.user
        return super().post(request)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user.id
        return kwargs

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     # ctx['']
    #     return ctx

    def get_success_url(self):
        return reverse('eventos:evento')

def evento(request):
    evento = Evento.objects.last()
    ins = Inscricao.objects.filter(user=request.user)
    if ins:
        return detalhe_inscricao(request)
    else:
        return render(request, 'eventos/evento.html', context={'evento':evento})
    

def home(request):
    return render(request, 'eventos/home.html',
                    context={'title':'Home'})
