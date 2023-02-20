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