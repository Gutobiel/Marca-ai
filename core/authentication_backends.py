# core/authentication_backends.py
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Tentando pegar o usuário com o e-mail informado
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        
        # Verificar se a senha está correta
        if user.check_password(password):
            return user
        return None