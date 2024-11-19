from django.db import models


class Ponto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.nome


