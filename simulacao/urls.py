from django.urls import path
from . import views

urlpatterns = [
    path('realizar_simulacao/', views.realizar_simulacao, name='realizar_simulacao'),
    path('simulacoes/', views.listar_simulacoes, name='listar_simulacoes'),
    path('listar/', views.listar_simulacoes, name='listar_simulacoes'),
    path('visualizar/<int:simulacao_id>/', views.visualizar_simulacao, name='visualizar_simulacao'),
    path('nova/', views.realizar_simulacao, name='realizar_simulacao'),
]

