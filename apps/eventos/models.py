from datetime import datetime
from django.db import models

from apps.locais.models import Local
from apps.users.models import User

# Create your models here.
class Evento(models.Model):
    nome = models.CharField(max_length=50)
    local = models.CharField(max_length=50)
    datahorainicio = models.DateTimeField()
    datahorafim = models.DateTimeField()
    #estado
    
    def __str__(self):
        return f'{self.nome} - {self.datahorainicio} a {self.datahorafim}'

class DetalhesEvento(models.Model):
    titulo = models.CharField(max_length=30)
    descricao = models.CharField(max_length=200)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

class SubEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    datahorainicio = models.DateTimeField()
    datahorafim = models.DateTimeField()
    notas = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f'{self.evento.nome} - {self.local}'

class Inscricao(models.Model):
    subevento = models.ForeignKey(SubEvento, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subevento.evento} - {self.user}'

class StoreCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    is_redeemed = models.BooleanField(default=False)
    picked = models.BooleanField(default=False)
    event = models.ForeignKey(Evento, on_delete=models.CASCADE, blank=True, null=True, related_name='codes')

    def __str__(self):
        return f'{self.code} - {self.is_redeemed}'

class BBCode(models.Model):
    store_code = models.OneToOneField(StoreCode, on_delete=models.CASCADE, related_name='bbcode')
    code = models.CharField(max_length=7, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    valid = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.code} - {self.store_code}'

class Reward(models.Model):
    REWARD_CHOICES = (
        ('Reward 1', 1),
        ('Reward 2', 2),
        ('Reward 3', 3),
        ('Reward 4', 4),
        ('Reward 5', 5),
    )

    bbcode = models.OneToOneField(BBCode, on_delete=models.CASCADE, related_name='reward')
    reward_type = models.CharField(max_length=20, choices=REWARD_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
        
    def __str__(self):
        return f'{self.reward_type} - {self.bbcode}'


class Message(models.Model):
    MsgId = models.CharField(max_length=255)
    From = models.CharField(max_length=255)
    To = models.CharField(max_length=255)
    Prefix = models.CharField(max_length=255)
    Msg = models.CharField(max_length=255)
    mcc = models.CharField(max_length=255)
    mnc = models.CharField(max_length=255)
    ReceivedDatetime = models.CharField(max_length=255)
    SegmentsTotalNumber = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.MsgId} - {self.Msg} - {self.ReceivedDatetime}'
    
