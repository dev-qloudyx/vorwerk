from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Local

# Create your views here.
class LocalListView(ListView):
    model = Local
    template_name = 'locais/local_list.html'
    context_object_name = 'locais'
    ordering = ['nome']


    
