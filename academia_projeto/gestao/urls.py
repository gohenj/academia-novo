from django.urls import path
from . import views

urlpatterns = [
    # Quando o endereço for /gestao/alunos/, chame a função 'lista_alunos' da nossa view
    path('alunos/', views.lista_alunos, name='lista_alunos'),
]