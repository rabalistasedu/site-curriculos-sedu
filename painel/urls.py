from django.urls import path
from . import views

app_name = 'painel'

urlpatterns = [
    path('', views.painel_central_view, name='central'),
    path('conteudos/', views.conteudos_view, name='conteudos'),
]
