from django.contrib import admin
from .models import Evento, DetalhesEvento, SubEvento, Inscricao, StoreCode, BBCode, Message, Reward

admin.site.register(Evento)
admin.site.register(DetalhesEvento)
admin.site.register(SubEvento)
admin.site.register(Inscricao)

class StoreCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_redeemed', 'picked', 'event')
    list_filter = ('is_redeemed','picked','event__nome')

admin.site.register(StoreCode, StoreCodeAdmin)

class BBCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'store_code')
    list_filter = ('store_code',)

admin.site.register(BBCode, BBCodeAdmin)

class RewardAdmin(admin.ModelAdmin):
    list_display = ('id', 'reward', 'bbcode', 'is_redeemed')
    list_filter = ('is_redeemed',)

admin.site.register(Reward, RewardAdmin)
admin.site.register(Message)

