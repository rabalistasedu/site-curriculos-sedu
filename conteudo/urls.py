from django.urls import path
from . import views

app_name = 'conteudo'

urlpatterns = [
    path('', views.home, name='home'),
    path('busca/', views.busca, name='busca'),
    path('categoria/<slug:slug>/', views.categoria_detalhe, name='categoria'),
    path('conteudo/<slug:slug>/', views.conteudo_detalhe, name='conteudo_detalhe'),
]
