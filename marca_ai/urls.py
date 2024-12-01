"""
URL configuration for marca_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from core import views
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.user_login, name='login'),       
    path('cadastro/', views.register, name='cadastro'),
    path('home/', views.home, name='home'), 
    path('partidas/', views.partidas, name='partidas'), 
    path('salvar-ponto/', views.salvar_ponto, name='salvar_ponto'),
    path('listar-pontos/', views.listar_pontos, name='listar_pontos'),
    path('mapa-e-lista/', views.mapa_e_lista, name='mapa_e_lista'),
    path('enviar-codigo/', views.enviar_codigo, name='enviar-codigo'),
    path('confirmar-codigo/', views.confirmar_codigo, name='confirmar_codigo'),
    path('redefinir-senha/', views.redefinir_senha, name='redefinir_senha'),
    path('partidas-criadas/', views.ver_partidas_criadas, name='ver_partidas_criadas'),
    path('criar-partida/', views.criar_partida, name='criar_partida'),
]
