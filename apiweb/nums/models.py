from django.db import models

class Numero(models.Model):
    numero = models.CharField(max_length = 30)
    abrev = models.CharField(max_length = 30)
