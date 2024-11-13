from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

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
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Define a senha de forma segura
            user.save()

            # Envia e-mail de boas-vindas
            send_mail(
                'Bem-vindo ao Marca Aí!',
                'Olá {}, seja bem-vindo ao nosso sistema!'.format(user.username),
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            # Faz login do usuário e redireciona para home
            login(request, user)
            return redirect('home')  # Substitua 'home' pelo nome correto da sua url de home.html
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

""" Login de usuário """
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha incorretos.')
    return render(request, 'login.html')