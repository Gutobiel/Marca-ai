from cProfile import Profile
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from streamlit import form
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Ponto
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth.backends import ModelBackend
from .models import PasswordResetToken
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PartidaForm

def user_login_view(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def partidas(request):
    return render(request, 'partidas.html')

def ver_partidas_criadas(request):
    return render(request, 'partidas_da_quadra.html')

def criar_partida(request):
    return render(request, 'criar-partida.html')


""" CADASTRO """
# core/views.py

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Define a senha de forma segura
            user.save()

            # Envia e-mail de boas-vindas
            send_mail(
                'Bem-vindo ao Marca Aí!',
                f'Olá {user.username}, seja bem-vindo ao nosso sistema!',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            # Mensagem de sucesso
            messages.success(request, 'Conta criada com sucesso! Você já pode fazer login.')

            # Realiza o login do usuário e redireciona para a página inicial
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Corrigido aqui
            return redirect('home')  # Redireciona para a página de home
        else:
            messages.error(request, 'Erro no cadastro. Verifique os campos e tente novamente.')
    else:
        form = UserRegistrationForm()

    return render(request, 'cadastro.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(f"Tentando login com: Email: {email} e Senha: {password}")  # Debug

        # Autentica o usuário com base no e-mail e senha
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Garante que o perfil do usuário exista
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Login com backend explícito
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha incorretos.')
    
    return render(request, 'login.html')

@csrf_exempt
def salvar_ponto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Analisa o corpo da requisição JSON
            quadra = Quadra.objects.create(
                descricao=data['descricao'],
                latitude=data['lat'],
                longitude=data['lng']
            )
            return JsonResponse({'message': 'Ponto salvo com sucesso!', 'id': quadra.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Quadra  # Certifique-se de que o modelo correto está sendo usado

@csrf_exempt
def salvar_quadra(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Analisa o corpo da requisição JSON
            quadra = Quadra.objects.create(
                descricao=data['descricao'],
                latitude=data['latitude'],
                longitude=data['longitude']
            )
            return JsonResponse({'message': 'Quadra salva com sucesso!', 'id': quadra.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método não permitido'}, status=405)


def listar_pontos(request):
    pontos = Ponto.objects.all()
    return render(request, 'listar_pontos.html', {'pontos': pontos})

def mapa_e_lista(request):
    pontos = Ponto.objects.all()
    return render(request, 'mapa_lista.html', {'pontos': pontos})

from django.contrib.auth.hashers import make_password

import random

def enviar_codigo(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            usuario = User.objects.get(email=email)
            codigo = random.randint(100000, 999999)  # Gera um código de 6 dígitos
            usuario.profile.codigo_recuperacao = codigo  # Supondo que o modelo Profile tenha esse campo
            usuario.profile.save()

            send_mail(
                'Código de Redefinição de Senha',
                f'Seu código para redefinir a senha é: {codigo}',
                'seu_email@exemplo.com',  # Substitua pelo seu e-mail de envio
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Código enviado para o seu e-mail.')
            return redirect('confirmar_codigo')
        except User.DoesNotExist:
            messages.error(request, 'E-mail não encontrado.')
    return render(request, 'enviar_codigo.html')

def confirmar_codigo(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        try:
            profile = request.user.profile  # Ajuste conforme sua relação com User
            if str(profile.codigo_recuperacao) == token:
                profile.codigo_recuperacao = None  # Apaga o código após uso
                profile.save()
                return redirect('redefinir_senha')
            else:
                messages.error(request, 'Código inválido.')
        except AttributeError:
            messages.error(request, 'Erro interno, tente novamente.')
    return render(request, 'confirmar_codigo.html')

def redefinir_senha(request):
    if request.method == 'POST':
        nova_senha = request.POST.get('password')
        user = request.user
        user.password = make_password(nova_senha)
        user.save()
        messages.success(request, 'Senha redefinida com sucesso.')
        return redirect('login')
    return render(request, 'redefinir_senha.html')



@login_required
def criar_partida(request):
    if request.method == 'POST':
        form = PartidaForm(request.POST)
        if form.is_valid():
            partida = form.save(commit=False)
            partida.criador = request.user
            partida.save()
            messages.success(request, 'Partida criada com sucesso!')
            return redirect('partidas')  # Substitua pelo nome da URL da página
        else:
            messages.error(request, 'Erro ao criar partida. Verifique os dados.')
    else:
        form = PartidaForm()

    return render(request, 'partidas.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Quadra, Partida

def partidas_por_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    partidas = quadra.partidas.all()  # Usa o `related_name` definido no modelo
    return render(request, 'partidas_por_quadra.html', {'quadra': quadra, 'partidas': partidas})


