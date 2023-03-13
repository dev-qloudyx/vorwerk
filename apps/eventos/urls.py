from django.urls import path, reverse_lazy
from .views import detalhe_inscricao, home, receitas, promos,  evento, NovaInscricao

from apps.eventos.code_gen import CodeGeneration
from .views import BBCodeViewSet, detalhe_inscricao, evento, NovaInscricao, gen_storecodes, generate_bbcode, select_storecodes, import_store_codes, import_rewards, choice

app_name = "eventos"

urlpatterns = [
    path('', home, name='home'),
    path('receitas/', receitas, name='receitas'),
    path('promos/', promos, name='promos'),
    path('inscricao/', detalhe_inscricao, name='inscricao'),
    path('nova-inscricao/', NovaInscricao.as_view(), name='nova-inscricao'),
    path('evento/', evento, name='evento'),
    path('generate-codes/', gen_storecodes, name='gen_codes'),
    path('passatempo/', generate_bbcode, name='passatempo'),
    path('generate-list-codes/', select_storecodes, name='generate_list_code'),
    path('list-duplicate-store-codes/', CodeGeneration.list_duplicate_store_codes, name='list_duplicate_store_codes'),
    path('code/', BBCodeViewSet.as_view({'post': 'create'})),
    path('import-store-codes/', import_store_codes, name='import_store_codes'),
    path('import-rewards/', import_rewards, name='import_rewards'),
    path('choice/', choice, name='choice'),
    path('export_data/<str:choice>', CodeGeneration.export_data, name='export_data')
    
]
