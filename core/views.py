from cProfile import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from streamlit import form
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Partida, Ponto
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from .forms import QuadraForm, UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth.backends import ModelBackend
from .models import PasswordResetToken
from django.contrib.auth.decorators import login_required
from .forms import PartidaForm
from .models import Profile

def user_login_view(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def partidas(request):
    return render(request, 'partidas.html')

def perfil(request):
    return render(request, 'perfil.html')

def logout(request):
    return render(request, 'login.html')

def editar_perfil(request):
    return render(request, 'editar_perfil.html')


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
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            local = data.get("local")
            descricao = data.get("descricao")
            latitude = data.get("lat")  # Alterado para lat
            longitude = data.get("lng")  # Alterado para lng

            if not local or not descricao or latitude is None or longitude is None:
                return JsonResponse({"error": "Todos os campos são obrigatórios."}, status=400)

            # Lógica para salvar a quadra no banco de dados
            nova_quadra = Quadra.objects.create(
                local=local,
                descricao=descricao,
                latitude=latitude,
                longitude=longitude
            )
            print(f"Quadra salva: {nova_quadra}")  # Verifica se a quadra foi salva corretamente

            return JsonResponse({"message": "Quadra salva com sucesso!"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados inválidos no corpo da requisição."}, status=400)
    return JsonResponse({"error": "Método não permitido."}, status=405)

def listar_quadras(request):
    quadras = Quadra.objects.all()
    return render(request, 'partidas.html', {'quadras': quadras})

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

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render

def confirmar_codigo(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        try:
            # Buscar o Profile pelo código de recuperação
            profile = Profile.objects.get(codigo_recuperacao=token)
            profile.codigo_recuperacao = None  # Apaga o código após uso
            profile.save()

            # Autentica o usuário temporariamente para redefinir a senha
            request.session['user_id'] = profile.user.id  # Armazena o ID do usuário na sessão
            return redirect('redefinir_senha')
        except Profile.DoesNotExist:
            messages.error(request, 'Código inválido ou expirado.')
    return render(request, 'confirmar_codigo.html')

def redefinir_senha(request):
    if request.method == 'POST':
        nova_senha = request.POST.get('password')
        user_id = request.session.get('user_id')  # Recupera o ID do usuário da sessão

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user.password = make_password(nova_senha)
                user.save()
                messages.success(request, 'Senha redefinida com sucesso.')
                del request.session['user_id']  # Remove o ID da sessão após a redefinição
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
        else:
            messages.error(request, 'Sessão inválida. Tente novamente.')

    return render(request, 'redefinir_senha.html')


@login_required
def criar_partida(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)

    if request.method == 'POST':
        form = PartidaForm(request.POST)
        if form.is_valid():
            partida = form.save(commit=False)  # Não salva no banco ainda
            partida.criador = request.user    # Associa o usuário logado
            partida.quadra = quadra           # Associa a quadra específica
            partida.save()                    # Agora salva no banco
            return redirect('ver_partidas_criadas', quadra_id=quadra.id)
        else:
            messages.error(request, 'Erro ao criar a partida. Verifique os dados.')

    else:
        form = PartidaForm()

    return render(request, 'criar_partida.html', {
        'form': form,
        'quadra': quadra,
    })

def partidas_por_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    partidas = Partida.objects.filter(quadra=quadra) 
    
    return render(request, 'partidas_da_quadra.html', {
        'quadra': quadra,
        'partidas': partidas,
    })

def listar_partidas(request, quadra_id):
    quadra = Quadra.objects.get(id=quadra_id)
    partidas = Partida.objects.filter(quadra=quadra)
    
    return render(request, 'partidas_da_quadra.html', {'quadra': quadra, 'partidas': partidas})

def ver_partidas_criadas(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    partidas = Partida.objects.filter(quadra=quadra)
    return render(request, 'partidas_da_quadra.html', {'quadra': quadra, 'partidas': partidas})

def editar_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    
    if request.method == 'POST':
        form = QuadraForm(request.POST, instance=quadra)
        if form.is_valid():
            form.save()
            messages.success(request, "Quadra atualizada com sucesso!")
            return redirect('listar_quadras')  # Redireciona para a lista de quadras
    else:
        form = QuadraForm(instance=quadra)

    return render(request, 'editar_quadra.html', {'form': form})

# Excluir quadra
def excluir_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)

    if request.method == 'POST':
        quadra.delete()
        messages.success(request, "Quadra excluída com sucesso!")
        return redirect('listar_quadras')  # Redireciona para a lista de quadras
    
    return render(request, 'confirmar_exclusao.html', {'quadra': quadra})

# View para editar a partida
def editar_partida(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)
    quadra_id = partida.quadra.id  # Pega o ID da quadra associada à partida

    if request.method == 'POST':
        form = PartidaForm(request.POST, instance=partida)
        if form.is_valid():
            form.save()
            messages.success(request, "Partida atualizada com sucesso!")
            return redirect('ver_partidas_criadas', quadra_id=quadra_id)
    else:
        form = PartidaForm(instance=partida)

    return render(request, 'editar_partida.html', {'form': form, 'quadra_id': quadra_id})


# View para excluir a partida
def excluir_partida(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)
    quadra_id = partida.quadra.id  # Pega o ID da quadra associada à partida

    if request.method == 'POST':
        partida.delete()
        messages.success(request, "Partida excluída com sucesso!")
        return redirect('ver_partidas_criadas', quadra_id=quadra_id)

    return render(request, 'excluir_partida.html', {'partida': partida, 'quadra_id': quadra_id})
