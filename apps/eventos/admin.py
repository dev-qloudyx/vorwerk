from django.contrib import admin
from .models import Evento, DetalhesEvento, SubEvento, Inscricao

admin.site.register(Evento)
admin.site.register(DetalhesEvento)
admin.site.register(SubEvento)
admin.site.register(Inscricao)