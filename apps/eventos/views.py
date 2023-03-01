import secrets
import string
import csv
import os
import time

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView

from apps.eventos.code_gen import CodeGeneration
from main import settings
from .models import BBCode, Inscricao, Evento, Message, StoreCode
from .forms import GenerateBBCodeForm, InscricaoForm, SelectCodesForm, StoreCodesForm
from django.urls import reverse_lazy, reverse

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import MessageSerializer
from rest_framework import status
from apps.users.roles import ADMIN, role_required
from django.contrib.auth.decorators import login_required

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
    # if request.user.is_authenticated:
    #     ins = Inscricao.objects.filter(user=request.user)
    #     if ins:
    #         return detalhe_inscricao(request)
    #     else:
    #         return render(request, 'eventos/evento.html', context={'evento':evento})
    ins = Inscricao.objects.filter(user=request.user)
    if ins:
        return detalhe_inscricao(request)
    else:
        return render(request, 'eventos/evento.html', context={'evento':evento})
    

def home(request):
    return render(request, 'eventos/home.html',
                    context={'title':'Home'})

def receitas(request):
    return render(request, 'eventos/receitas.html',
                    context={'title':'Receitas'})

@login_required
@role_required(ADMIN)
def generate_bbcode(request):
    if request.method == 'POST':
        form = GenerateBBCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            result = CodeGeneration.generate_bb_code(request, code)
            context = {
                'result': result,
            }
            return render(request, 'eventos/generate_bbcode.html', context)
    else:
        form = GenerateBBCodeForm()
    context = {
        'form': form,
    }
    return render(request, 'eventos/generate_bbcode.html', context)

@login_required
@role_required(ADMIN)
def gen_storecodes(request):
    if request.method == 'POST':
        form = StoreCodesForm(request.POST)
        if form.is_valid():
            num_codes = form.cleaned_data['num_codes']
            eventid = form.cleaned_data['event']
            storecodes = CodeGeneration.generate_store_codes(request, num_codes, eventid.id)
            evento = Evento.objects.get(id=eventid.id)
            codes = evento.codes.all()
            unused_codes = codes.filter(is_redeemed=False, picked=False).count()
            return render(request, 'eventos/generete_storecodes.html', {'storecodes': storecodes, 'unused_codes': unused_codes, 'form': form})
    else:
        form = SelectCodesForm()
    return render(request, 'eventos/select_codes.html', {'form': form})

@login_required
@role_required(ADMIN)
def select_storecodes(request):
    if request.method == 'POST':
        form = SelectCodesForm(request.POST)
        if form.is_valid():
            num_codes = form.cleaned_data['num_codes']
            eventid = form.cleaned_data['event']
            selected_codes = CodeGeneration.select_codes(request, num_codes, eventid.id)
            filename = download_codes(request, selected_codes)
            return render(request, 'eventos/select_codes.html', {'selected_codes': selected_codes, 'filename': filename, 'form': form})
    else:
        form = SelectCodesForm()
    return render(request, 'eventos/select_codes.html', {'form': form})

from django.core.files.storage import default_storage

def download_codes(request, selected_codes):
    # Generate a unique filename based on the current timestamp
    characters = string.digits + string.ascii_uppercase
    guid = secrets.choice(characters)
    filename = f"selected_codes_{guid}{int(time.time())}.txt"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    # Write the selected codes to the file
    try:
        with open(filepath, 'w') as f:
            for code in selected_codes:
                f.write(str(code.code) + '\n')
    except Exception as e:
        # Log or print out the error message
        return HttpResponse("Error generating file.")

    # Get the URL of the file in the media directory
    file_url = default_storage.url(filename)
    return file_url



class BBCodeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Set permission for this viewset to require authentication (Is set to Basic Auth)
    serializer_class = MessageSerializer  # Set the serializer class for the Message model

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # Get the serializer for the incoming request data
        check_serializer = serializer.is_valid(raise_exception=False)  # Validate the incoming data

        if not check_serializer:  # If validation fails, return a 400 response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            #task = CodeGeneration.send_message(request,**kwargs)
            return Response('OK', content_type='text/plain', status=200)


