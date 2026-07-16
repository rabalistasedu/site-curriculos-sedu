from django.urls import path
from . import views

app_name = 'inteligencia'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/', views.dashboard_api, name='api'),
    path('exportar/excel/', views.exportar_excel_view, name='exportar_excel'),
    path('exportar/pdf/', views.exportar_pdf_view, name='exportar_pdf'),
]
