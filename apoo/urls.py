from django.contrib import admin
from django.urls import path, include
from simulacao import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.realizar_simulacao, name='home'),  # Rota inicial aponta para a view realizar_simulacao
    path('realizar_simulacao/', include('simulacao.urls')),  # Inclui as URLs do app simulacao
]
