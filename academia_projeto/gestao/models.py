from django.db import models

# Modelo baseado em cidades.txt
class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.CharField(max_length=2) # ex: sp

    def __str__(self):
        return f"{self.nome} ({self.estado})"

# Modelo baseado em professores.txt
class Professor(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome

# Modelo baseado em alunos.txt
class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)
    data_nascimento = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.nome

# Modelo baseado em modalidades.txt
class Modalidade(models.Model):
    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)
    valor_mensal = models.DecimalField(max_digits=7, decimal_places=2)
    max_alunos = models.IntegerField()

    def __str__(self):
        return self.nome

# Modelo baseado em matriculas.txt
class Matricula(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
    dia_vencimento = models.IntegerField()
    data_inicio = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Matrícula de {self.aluno.nome} em {self.modalidade.nome}"