from django.db import models

class Ponto(models.Model):
    descricao = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.descricao} ({self.categoria})"



