from django.db import models

class Numero(models.Model):
    num_id = models.AutoField(primary_key=True, default="")
    numero = models.CharField(max_length = 30)
    abrev = models.CharField(max_length = 30)

class Log(models.Model):
    usuario = models.CharField(max_length = 30)
    tipo = models.CharField(max_length = 30)
    numero_viejo = models.CharField(max_length = 30)
    abrev_viejo = models.CharField(max_length = 30)
    numero_nuevo = models.CharField(max_length = 30)
    abrev_nuevo = models.CharField(max_length = 30)
    hora = models.DateTimeField(auto_now = True)
