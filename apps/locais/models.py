from django.db import models

# Create your models here.
class Local(models.Model):
    nome = models.CharField(max_length=30)
    cidade = models.CharField(max_length=30)
    codigopostal = models.CharField(max_length=50)
    coordenadas = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.nome} - {self.cidade}'