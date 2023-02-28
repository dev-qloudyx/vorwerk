from django.urls import path, reverse_lazy
from .views import detalhe_inscricao, home, receitas, evento, NovaInscricao

app_name = "eventos"

urlpatterns = [
    path('home/', home, name='home'),
    path('receitas/', receitas, name='receitas'),
    path('inscricao/', detalhe_inscricao, name='inscricao'),
    path('nova-inscricao/', NovaInscricao.as_view(), name='nova-inscricao'),
    path('evento/', evento, name='evento'),
]
