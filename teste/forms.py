from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange

# Neste arquivo, definimos as REGRAS para cada campo de cada formulário.
# Isso centraliza a validação e deixa o app.py muito mais limpo.

class CidadeForm(FlaskForm):
    """Formulário para validar dados de Cidades."""
    cod = IntegerField('Código', validators=[
        DataRequired(message="O código é obrigatório."),
        NumberRange(min=1, message="O código deve ser um número positivo.")
    ])
    desc = StringField('Descrição', validators=[
        DataRequired(message="A descrição é obrigatória."),
        Length(min=3, max=50, message="Deve ter entre 3 e 50 caracteres."),
        Regexp(r'^[A-ZÀ-Ö][A-Za-zÀ-ÖØ-öø-ÿ0-9\s]*$', message='Descrição inválida. Use apenas letras e espaços. E letra maiúscula no começo!')
    ])
    uf = StringField('UF', validators=[
        DataRequired(message="A UF é obrigatória."),
        Length(min=2, max=2, message="UF deve ter exatamente 2 letras."),
        Regexp('^[A-Za-z]*$', message='Use apenas letras para a UF.')
    ])
    submit = SubmitField('Salvar Cidade')

class AlunoForm(FlaskForm):
    """Formulário para validar dados de Alunos."""
    cod_aluno = IntegerField('Código do Aluno', validators=[
        DataRequired(message="O código é obrigatório."),
        NumberRange(min=1, message="O código deve ser um número positivo.")
    ])
    nome = StringField('Nome Completo', validators=[
        DataRequired(message="O nome é obrigatório."),
        Length(min=3, max=100),
        Regexp(r'^[A-ZÀ-Ö][A-Za-zÀ-ÖØ-öø-ÿ0-9\s]*$', message='Descrição inválida. Use apenas letras e espaços. E letra maiúscula no começo!')
    ])
    cod_cidade = SelectField('Cidade', coerce=int, validators=[
        DataRequired(message="Selecione uma cidade.")
    ])
    data_nasc = StringField('Data de Nascimento', validators=[
        DataRequired(message="A data é obrigatória."),
        Regexp(r'^\d{2}/\d{2}/\d{4}$', message="Formato inválido. Use DD/MM/AAAA.")
    ])
    peso = FloatField('Peso (kg)', validators=[
        DataRequired(message="O peso é obrigatório."),
        NumberRange(min=20, max=300, message="Peso deve ser um valor realista.")
    ])
    altura = FloatField('Altura (m)', validators=[
        DataRequired(message="A altura é obrigatória."),
        NumberRange(min=1, max=2.5, message="Altura deve estar em metros (ex: 1.75).")
    ])
    submit = SubmitField('Salvar Aluno')

class ProfessorForm(FlaskForm):
    """Formulário para validar dados de Professores."""
    cod_professor = IntegerField('Código do Professor', validators=[
        DataRequired(message="O código é obrigatório."),
        NumberRange(min=1, message="O código deve ser um número positivo.")
    ])
    nome = StringField('Nome Completo', validators=[
        DataRequired(message="O nome é obrigatório."),
        Length(min=3, max=100),
        Regexp(r'^[A-ZÀ-Ö][A-Za-zÀ-ÖØ-öø-ÿ0-9\s]*$', message='Descrição inválida. Use apenas letras e espaços. E letra maiúscula no começo!')
    ])
    endereco = StringField('Endereço', validators=[
        DataRequired(message="O endereço é obrigatório.")
    ])
    telefone = StringField('Telefone', validators=[
        DataRequired(message="O telefone é obrigatório."),
        Regexp(r'^\d{10,11}$', message='Telefone inválido. Use apenas números, com DDD e sem espaços ou caracteres.')
    ])
    cod_cidade = SelectField('Cidade', coerce=int, validators=[
        DataRequired(message="Selecione uma cidade.")
    ])
    submit = SubmitField('Salvar Professor')

class ModalidadeForm(FlaskForm):
    """Formulário para validar dados de Modalidades."""
    cod_modalidade = IntegerField('Código da Modalidade', validators=[
        DataRequired(message="O código é obrigatório."),
        NumberRange(min=1, message="O código deve ser um número positivo.")
    ])
    descricao = StringField('Descrição', validators=[
        DataRequired(message="A descrição é obrigatória."),
        Length(min=3, max=50),
        Regexp(r'^[A-ZÀ-Ö][A-Za-zÀ-ÖØ-öø-ÿ0-9\s]*$', message='Descrição inválida. Use apenas letras e espaços. E letra maiúscula no começo!')
    ])
    cod_professor = SelectField('Professor', coerce=int, validators=[
        DataRequired(message="Selecione um professor.")
    ])
    valor_aula = FloatField('Valor da Aula (R$)', validators=[
        DataRequired(message="O valor é obrigatório."),
        NumberRange(min=1, message="O valor deve ser positivo.")
    ])
    limite_alunos = IntegerField('Limite de Alunos', validators=[
        DataRequired(message="O limite é obrigatório."),
        NumberRange(min=1, message="O limite deve ser de pelo menos 1 aluno.")
    ])
    submit = SubmitField('Salvar Modalidade')

class MatriculaForm(FlaskForm):
    """Formulário para validar dados de Matrículas."""
    cod_matricula = IntegerField('Código da Matrícula', validators=[
        DataRequired(message="O código é obrigatório."),
        NumberRange(min=1, message="O código deve ser um número positivo.")
    ])
    cod_aluno = SelectField('Aluno', coerce=int, validators=[
        DataRequired(message="Selecione um aluno.")
    ])
    cod_modalidade = SelectField('Modalidade', coerce=int, validators=[
        DataRequired(message="Selecione uma modalidade.")
    ])
    qtde_aulas = IntegerField('Quantidade de Aulas', validators=[
        DataRequired(message="A quantidade de aulas é obrigatória."),
        NumberRange(min=1, message="Deve haver pelo menos 1 aula.")
    ])
    submit = SubmitField('Realizar Matrícula')

