from django.urls import path, reverse_lazy
from .views import detalhe_inscricao, home, receitas, evento, NovaInscricao

from apps.eventos.code_gen import CodeGeneration
from .views import BBCodeViewSet, detalhe_inscricao, evento, NovaInscricao, gen_storecodes, generate_bbcode, select_storecodes
app_name = "eventos"

urlpatterns = [
    path('home/', home, name='home'),
    path('receitas/', receitas, name='receitas'),
    path('inscricao/', detalhe_inscricao, name='inscricao'),
    path('nova-inscricao/', NovaInscricao.as_view(), name='nova-inscricao'),
    path('evento/', evento, name='evento'),
    path('generate-codes/', gen_storecodes, name='gen_codes'),
    path('generate-bb-codes/', generate_bbcode, name='generate_bb_code'),
    path('generate-list-codes/', select_storecodes, name='generate_list_code'),
    path('list-duplicate-store-codes/', CodeGeneration.list_duplicate_store_codes, name='list_duplicate_store_codes'),
    path('code/', BBCodeViewSet.as_view({'post': 'create'})),
    
]
