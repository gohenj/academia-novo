from django.shortcuts import render
from .models import Aluno

# Create your views here.
def lista_alunos(request):
    # 1. Busca todos os objetos do tipo Aluno no banco de dados
    todos_os_alunos = Aluno.objects.all()

    # 2. Define o contexto que será enviado para o HTML
    contexto = {
        'alunos': todos_os_alunos,
    }

    # 3. Renderiza (desenha) a página HTML, enviando os dados para ela
    return render(request, 'gestao/lista_alunos.html', contexto)