from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver


class Ponto(models.Model):
    local = models.CharField(max_length=255)  # Substituindo descricao
    descricao = models.CharField(max_length=100)  # Substituindo categoria
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.local} ({self.descricao})"
     
class Quadra(models.Model):
    local = models.CharField(max_length=255, null=True)
    descricao = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.descricao



class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(default=now)

    def is_valid(self):
        # O token expira após 10 minutos (ajuste conforme necessário)
        return (now() - self.created_at).seconds < 600
    
    from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    codigo_recuperacao = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Partida(models.Model):
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="partidas")
    esporte = models.CharField(max_length=100)
    data = models.DateField()
    horario = models.TimeField()
    max_participantes = models.IntegerField()
    quadra = models.ForeignKey('Quadra', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.esporte} - {self.data} ({self.criador.username})"
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


