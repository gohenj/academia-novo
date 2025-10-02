# app.py
# Servidor Web Flask

from flask import Flask, render_template, request, redirect, url_for, flash
import gestao_academia_lib as lib  # Importa nossa biblioteca

app = Flask(__name__)
# Chave secreta para mensagens flash (necessária para exibir erros/sucesso)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-12345'

# Carrega os dados dos arquivos UMA VEZ ao iniciar o servidor
lib.carregar_dados()

# --- Rota Principal ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Rotas de Cidades ---
@app.route('/cidades', methods=['GET', 'POST'])
def cidades():
    if request.method == 'POST':
        # Recebe dados do formulário
        cod = int(request.form['cod'])
        desc = request.form['desc']
        uf = request.form['uf']
        
        # Tenta incluir no backend
        sucesso, msg = lib.incluir_cidade(cod, desc, uf)
        flash(msg, 'success' if sucesso else 'danger') # Exibe mensagem
        
        return redirect(url_for('cidades'))

    # Se for GET, apenas lista
    lista_cidades = lib.get_todas_cidades()
    return render_template('cidades.html', cidades=lista_cidades)

@app.route('/cidades/excluir/<int:cod>')
def excluir_cidade(cod):
    sucesso, msg = lib.excluir_cidade(cod)
    flash(msg, 'success' if sucesso else 'danger')
    return redirect(url_for('cidades'))

# --- Rotas de Alunos ---
@app.route('/alunos', methods=['GET', 'POST'])
def alunos():
    if request.method == 'POST':
        cod = int(request.form['cod_aluno'])
        nome = request.form['nome']
        cod_cidade = int(request.form['cod_cidade'])
        data_nasc = request.form['data_nasc']
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        
        sucesso, msg = lib.incluir_aluno(cod, nome, cod_cidade, data_nasc, peso, altura)
        flash(msg, 'success' if sucesso else 'danger')
        return redirect(url_for('alunos'))

    lista_alunos = lib.get_todos_alunos_detalhado()
    lista_cidades = lib.get_todas_cidades() # Para o dropdown
    return render_template('alunos.html', alunos=lista_alunos, cidades=lista_cidades)

@app.route('/alunos/excluir/<int:cod>')
def excluir_aluno(cod):
    sucesso, msg = lib.excluir_aluno(cod)
    flash(msg, 'success' if sucesso else 'danger')
    return redirect(url_for('alunos'))

# --- Rotas de Professores ---
@app.route('/professores', methods=['GET', 'POST'])
def professores():
    if request.method == 'POST':
        cod = int(request.form['cod_professor'])
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        cod_cidade = int(request.form['cod_cidade'])

        sucesso, msg = lib.incluir_professor(cod, nome, endereco, telefone, cod_cidade)
        flash(msg, 'success' if sucesso else 'danger')
        return redirect(url_for('professores'))

    lista_professores = lib.get_todos_professores_detalhado()
    lista_cidades = lib.get_todas_cidades() # Para o dropdown
    return render_template('professores.html', professores=lista_professores, cidades=lista_cidades)

@app.route('/professores/excluir/<int:cod>')
def excluir_professor(cod):
    sucesso, msg = lib.excluir_professor(cod)
    flash(msg, 'success' if sucesso else 'danger')
    return redirect(url_for('professores'))

# --- Rotas de Modalidades ---
@app.route('/modalidades', methods=['GET', 'POST'])
def modalidades():
    if request.method == 'POST':
        cod = int(request.form['cod_modalidade'])
        desc = request.form['descricao']
        cod_prof = int(request.form['cod_professor'])
        valor = float(request.form['valor_aula'])
        limite = int(request.form['limite_alunos'])

        sucesso, msg = lib.incluir_modalidade(cod, desc, cod_prof, valor, limite)
        flash(msg, 'success' if sucesso else 'danger')
        return redirect(url_for('modalidades'))

    lista_modalidades = lib.get_todas_modalidades_detalhado()
    lista_professores = lib.get_todos_professores_detalhado() # Para o dropdown
    return render_template('modalidades.html', modalidades=lista_modalidades, professores=lista_professores)

@app.route('/modalidades/excluir/<int:cod>')
def excluir_modalidade(cod):
    sucesso, msg = lib.excluir_modalidade(cod)
    flash(msg, 'success' if sucesso else 'danger')
    return redirect(url_for('modalidades'))

# --- Rotas de Matrículas ---
@app.route('/matriculas', methods=['GET', 'POST'])
def matriculas():
    if request.method == 'POST':
        cod = int(request.form['cod_matricula'])
        cod_aluno = int(request.form['cod_aluno'])
        cod_modalidade = int(request.form['cod_modalidade'])
        qtde_aulas = int(request.form['qtde_aulas'])

        sucesso, msg = lib.incluir_matricula(cod, cod_aluno, cod_modalidade, qtde_aulas)
        flash(msg, 'success' if sucesso else 'danger')
        return redirect(url_for('matriculas'))

    lista_matriculas = lib.get_todas_matriculas_detalhado()
    lista_alunos = lib.get_todos_alunos_detalhado()
    lista_modalidades = lib.get_todas_modalidades_detalhado()
    return render_template('matriculas.html', matriculas=lista_matriculas, alunos=lista_alunos, modalidades=lista_modalidades)

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

# --- Roda o Servidor ---
if __name__ == '__main__':
    app.run(debug=True)