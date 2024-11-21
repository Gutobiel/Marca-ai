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

def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def partidas(request):
    return render(request, 'partidas.html')


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

            # Faz login do usuário e redireciona para a página inicial
            login(request, user)
            return redirect('home')  # Redireciona para a página de home (ajuste conforme necessário)

        else:
            # Se o formulário não for válido, exibe as mensagens de erro
            messages.error(request, 'Erro no cadastro. Verifique os campos e tente novamente.')
    else:
        form = UserRegistrationForm()

    return render(request, 'cadastro.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(f"Tentando login com: Email: {email} e Senha: {password}")  # Debug
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha incorretos.')
    
    return render(request, 'login.html')


def partidas(request):
    return render(request, 'partidas.html')


@csrf_exempt
def salvar_ponto(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        descricao = data.get('descricao')
        categoria = data.get('categoria')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if descricao and categoria and latitude and longitude:
            Ponto.objects.create(
                descricao=descricao,
                categoria=categoria,
                latitude=latitude,
                longitude=longitude
            )
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Dados inválidos'})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

def listar_pontos(request):
    pontos = Ponto.objects.all()
    return render(request, 'listar_pontos.html', {'pontos': pontos})

def mapa_e_lista(request):
    pontos = Ponto.objects.all()
    return render(request, 'mapa_lista.html', {'pontos': pontos})

