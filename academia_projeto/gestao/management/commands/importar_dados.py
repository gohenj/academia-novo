from django.core.management.base import BaseCommand
from gestao.models import Cidade, Professor, Aluno, Modalidade, Matricula
from datetime import datetime

class Command(BaseCommand):
    help = 'Importa dados dos arquivos .txt para o banco de dados'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando importação...'))

        # Limpa tabelas na ordem correta para evitar erros de referência
        Matricula.objects.all().delete()
        Modalidade.objects.all().delete()
        Aluno.objects.all().delete()
        Professor.objects.all().delete()
        Cidade.objects.all().delete()
        self.stdout.write('Banco de dados antigo limpo.')

        cidades_map = {}
        professores_map = {}
        alunos_map = {}
        modalidades_map = {}

        # Importar Cidades
        with open('cidades.txt', 'r', encoding='utf-8') as f:
            for linha in f:
                id_antigo, nome, estado = linha.strip().split(';')
                cidade = Cidade.objects.create(nome=nome, estado=estado)
                cidades_map[id_antigo] = cidade
        self.stdout.write(self.style.SUCCESS(f'{len(cidades_map)} cidades importadas.'))

        # Importar Professores
        with open('professores.txt', 'r', encoding='utf-8') as f:
            for linha in f:
                id_antigo, nome, rua, tel, id_cidade = linha.strip().split(';')
                cidade_obj = cidades_map.get(id_cidade)
                professor = Professor.objects.create(nome=nome, endereco=rua, telefone=tel, cidade=cidade_obj)
                professores_map[id_antigo] = professor
        self.stdout.write(self.style.SUCCESS(f'{len(professores_map)} professores importados.'))

        # Importar Alunos
        with open('alunos.txt', 'r', encoding='utf-8') as f:
            for linha in f:
                id_antigo, nome, id_cidade, nasc, peso, altura = linha.strip().split(';')
                cidade_obj = cidades_map.get(id_cidade)
                data_nasc_obj = datetime.strptime(nasc, '%d/%m/%Y').date()
                aluno = Aluno.objects.create(nome=nome, cidade=cidade_obj, data_nascimento=data_nasc_obj, peso=peso.replace(',', '.'), altura=altura.replace(',', '.'))
                alunos_map[id_antigo] = aluno
        self.stdout.write(self.style.SUCCESS(f'{len(alunos_map)} alunos importados.'))

        # Importar Modalidades
        with open('modalidades.txt', 'r', encoding='utf-8') as f:
            for linha in f:
                id_antigo, nome, id_prof, valor, max_a, status = linha.strip().split(';')
                prof_obj = professores_map.get(id_prof)
                modalidade = Modalidade.objects.create(nome=nome, professor=prof_obj, valor_mensal=valor.replace(',', '.'), max_alunos=max_a)
                modalidades_map[id_antigo] = modalidade
        self.stdout.write(self.style.SUCCESS(f'{len(modalidades_map)} modalidades importadas.'))

        # Importar Matrículas
        with open('matriculas.txt', 'r', encoding='utf-8') as f:
            for linha in f:
                id_aluno, id_modalidade, id_antigo_matricula, dia_venc = linha.strip().split(';')
                aluno_obj = alunos_map.get(id_aluno)
                modalidade_obj = modalidades_map.get(id_modalidade)
                if aluno_obj and modalidade_obj:
                    Matricula.objects.create(aluno=aluno_obj, modalidade=modalidade_obj, dia_vencimento=dia_venc)
        self.stdout.write(self.style.SUCCESS('Matrículas importadas.'))

        self.stdout.write(self.style.SUCCESS('Importação finalizada com sucesso!'))