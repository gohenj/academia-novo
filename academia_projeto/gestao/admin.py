from django.contrib import admin
from .models import Cidade, Professor, Aluno, Modalidade, Matricula

admin.site.register(Cidade)
admin.site.register(Professor)
admin.site.register(Aluno)
admin.site.register(Modalidade)
admin.site.register(Matricula)