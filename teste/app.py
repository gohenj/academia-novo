from flask import Flask, render_template, request, redirect, url_for, flash
import gestao_academia_lib as lib
# Importamos TODAS as nossas classes de formulário do arquivo forms.py
from forms import CidadeForm, AlunoForm, ProfessorForm, ModalidadeForm, MatriculaForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-12345'

# Carrega os dados na memória ao iniciar
lib.carregar_dados()

@app.route('/')
def index():
    return render_template('index.html')

# --- Rotas de Cidades ---
@app.route('/cidades', methods=['GET', 'POST'])
def cidades():
    form = CidadeForm()
    # Este 'if' só será verdadeiro se o formulário for enviado (POST) E passar em todas as regras
    if form.validate_on_submit():
        # Pegamos os dados validados e limpos do formulário
        sucesso, msg = lib.incluir_cidade(form.cod.data, form.desc.data, form.uf.data)
        flash(msg, 'success' if sucesso else 'danger')
        return redirect(url_for('cidades'))
    
    # Se for GET ou se a validação falhar, a página é renderizada normalmente
    lista_cidades = lib.get_todas_cidades()
    # Passamos o objeto 'form' para o template para que ele possa ser desenhado
    return render_template('cidades.html', cidades=lista_cidades, form=form)

@app.route('/cidades/excluir/<int:cod>')
def excluir_cidade(cod):
    sucesso, msg = lib.excluir_cidade(cod)
    flash(msg, 'success' if sucesso else 'danger')
    return redirect(url_for('cidades'))

# --- Rotas de Alunos ---
@app.route('/alunos', methods=['GET', 'POST'])
def alunos():
    form = AlunoForm()
    # Populamos as opções do campo <select> de cidades dinamicamente
    form.cod_cidade.choices = [(c[0], f"{c[1]} - {c[2]}") for c in lib.get_todas_cidades()]
    
    if form.validate_on_submit():
        sucesso, msg = lib.incluir_aluno(
            form.cod_aluno.data, form.nome.data, form.cod_cidade.data,
            form.data_nasc.data, form.peso.data, form.altura.data
        )
        flash(msg, 'success' if sucesso else 'danger')
        return redirect(url_for('alunos'))

    lista_alunos = lib.get_todos_alunos_detalhado()
    return render_template('alunos.html', alunos=lista_alunos, form=form)

@app.route('/alunos/excluir/<int:cod>')
def excluir_aluno(cod):
    sucesso, msg = lib.excluir_aluno(cod)
    flash(msg, 'success' if sucesso else 'danger')
    return redirect(url_for('alunos'))

# --- Rotas de Professores ---
@app.route('/professores', methods=['GET', 'POST'])
def professores():
    form = ProfessorForm()
    # Populamos as opções do campo <select> de cidades
    form.cod_cidade.choices = [(c[0], f"{c[1]} - {c[2]}") for c in lib.get_todas_cidades()]

    if form.validate_on_submit():
        sucesso, msg = lib.incluir_professor(
            form.cod_professor.data, form.nome.data, form.endereco.data,
            form.telefone.data, form.cod_cidade.data
        )
        flash(msg, 'success' if sucesso else 'danger')
        return redirect(url_for('professores'))

    lista_professores = lib.get_todos_professores_detalhado()
    return render_template('professores.html', professores=lista_professores, form=form)

@app.route('/professores/excluir/<int:cod>')
def excluir_professor(cod):
    sucesso, msg = lib.excluir_professor(cod)
    flash(msg, 'success' if sucesso else 'danger')
    return redirect(url_for('professores'))

# --- Rotas de Modalidades ---
@app.route('/modalidades', methods=['GET', 'POST'])
def modalidades():
    form = ModalidadeForm()
    # Populamos as opções do campo <select> de professores
    form.cod_professor.choices = [(p['cod_professor'], p['nome']) for p in lib.get_todos_professores_detalhado()]

    if form.validate_on_submit():
        sucesso, msg = lib.incluir_modalidade(
            form.cod_modalidade.data, form.descricao.data, form.cod_professor.data,
            form.valor_aula.data, form.limite_alunos.data
        )
        flash(msg, 'success' if sucesso else 'danger')
        return redirect(url_for('modalidades'))

    lista_modalidades = lib.get_todas_modalidades_detalhado()
    return render_template('modalidades.html', modalidades=lista_modalidades, form=form)

@app.route('/modalidades/excluir/<int:cod>')
def excluir_modalidade(cod):
    sucesso, msg = lib.excluir_modalidade(cod)
    flash(msg, 'success' if sucesso else 'danger')
    return redirect(url_for('modalidades'))

# --- Rotas de Matrículas ---
@app.route('/matriculas', methods=['GET', 'POST'])
def matriculas():
    form = MatriculaForm()
    # Populamos os campos de seleção de alunos e modalidades
    form.cod_aluno.choices = [(a['cod_aluno'], a['nome']) for a in lib.get_todos_alunos_detalhado()]
    form.cod_modalidade.choices = [(m['cod_modalidade'], m['descricao']) for m in lib.get_todas_modalidades_detalhado()]

    if form.validate_on_submit():
        sucesso, msg = lib.incluir_matricula(
            form.cod_matricula.data, form.cod_aluno.data,
            form.cod_modalidade.data, form.qtde_aulas.data
        )
        flash(msg, 'success' if sucesso else 'danger')
        return redirect(url_for('matriculas'))

    lista_matriculas = lib.get_todas_matriculas_detalhado()
    return render_template('matriculas.html', matriculas=lista_matriculas, form=form)

@app.route('/matriculas/excluir/<int:cod>')
def excluir_matricula(cod):
    sucesso, msg = lib.excluir_matricula(cod)
    flash(msg, 'success' if sucesso else 'danger')
    return redirect(url_for('matriculas'))

# --- Rotas de Relatórios ---
@app.route('/relatorio/faturamento')
def relatorio_faturamento():
    dados_faturamento = lib.get_relatorio_faturamento()
    return render_template('relatorio_faturamento.html', faturamento=dados_faturamento)

@app.route('/relatorio/matriculas_geral')
def relatorio_matriculas_geral():
    dados_relatorio = lib.get_relatorio_matriculas_ordenado()
    return render_template('relatorio_matriculas.html', 
                           matriculas=dados_relatorio['matriculas'], 
                           total_matriculas=dados_relatorio['total_matriculas'],
                           valor_total_geral=dados_relatorio['valor_total_geral'])

if __name__ == '__main__':
    app.run(debug=True)

