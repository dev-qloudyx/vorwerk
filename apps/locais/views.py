from django.shortcuts import render
from django.views.generic.list import ListView
from django.db.models import Value, F
from .models import Local

# Create your views here.
class LocalListView(ListView):
    model = Local
    queryset = Local.objects.all()
    template_name = 'locais/local_list.html'
    context_object_name = 'locais'
    ordering = ['nome']
    
