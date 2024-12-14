from django.urls import path
from . import views

urlpatterns = [
    path('realizar_simulacao/', views.realizar_simulacao, name='realizar_simulacao'),
]

