from django.shortcuts import render

def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def partidas(request):
    return render(request, 'partidas.html')
