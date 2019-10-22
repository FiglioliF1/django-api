from django.db import models

class Numero(models.Model):
    num_id = models.AutoField(primary_key=True, default="")
    numero = models.CharField(max_length = 30)
    abrev = models.CharField(max_length = 30)
