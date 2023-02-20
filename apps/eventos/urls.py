from django.urls import path, reverse_lazy
from .views import detalhe_inscricao, evento, NovaInscricao

app_name = "eventos"

urlpatterns = [
    path('inscricao/', detalhe_inscricao, name='inscricao'),
    path('nova-inscricao/', NovaInscricao.as_view(), name='nova-inscricao'),
    path('evento/', evento, name='evento'),
]
