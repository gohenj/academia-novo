# gestao_academia_lib.py
# Versão refatorada para ser usada como biblioteca pelo Flask

import os
from arvore_binaria import ArvoreBinariaBusca

# --- ESTRUTURA DOS DADOS E ARQUIVOS ---
dados = {
    "cidades": {},
    "alunos": {},
    "professores": {},
    "modalidades": {},
    "matriculas": {}
}
indices = {
    "cidades": ArvoreBinariaBusca(),
    "alunos": ArvoreBinariaBusca(),
    "professores": ArvoreBinariaBusca(),
    "modalidades": ArvoreBinariaBusca(),
    "matriculas": ArvoreBinariaBusca()
}
arquivos = {
    "cidades": "cidades.txt",
    "alunos": "alunos.txt",
    "professores": "professores.txt",
    "modalidades": "modalidades.txt",
    "matriculas": "matriculas.txt"
}

# --- FUNÇÕES DE PERSISTÊNCIA ---

def carregar_dados():
    """Carrega os dados dos arquivos para a memória e constrói os índices."""
    print("Carregando dados e construindo índices...")
    for tabela, nome_arquivo in arquivos.items():
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                for linha in f:
                    linha = linha.strip()
                    if linha:
                        partes = linha.split(';')
                        chave = int(partes[0])
                        dados[tabela][chave] = partes
                        indices[tabela].inserir(chave)
    print("Dados carregados!")

def salvar_dados(tabela):
    """Salva os dados de uma tabela da memória para o arquivo."""
    nome_arquivo = arquivos[tabela]
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        chaves_ordenadas = sorted(dados[tabela].keys())
        for chave in chaves_ordenadas:
            linha = ";".join(map(str, dados[tabela][chave]))
            f.write(f"{linha}\n")

# --- FUNÇÕES AUXILIARES ---

def calcular_imc(peso, altura):
    try:
        peso = float(peso)
        altura = float(altura)
        if altura == 0:
            return 0, "Altura inválida"
        imc = peso / (altura * altura)
        if imc < 18.5: diagnostico = "Abaixo do peso"
        elif 18.5 <= imc < 25: diagnostico = "Peso normal"
        elif 25 <= imc < 30: diagnostico = "Sobrepeso"
        else: diagnostico = "Obesidade"
        return imc, diagnostico
    except ValueError:
        return 0, "Dados inválidos"

# --- FUNÇÕES DE CIDADES ---

def get_todas_cidades():
    return sorted(dados["cidades"].values(), key=lambda x: int(x[0]))

def get_cidade(cod):
    return dados["cidades"].get(cod)

def incluir_cidade(cod, descricao, estado):
    if indices["cidades"].buscar(cod):
        return False, "Código de cidade já existe."
    dados["cidades"][cod] = [cod, descricao, estado]
    indices["cidades"].inserir(cod)
    salvar_dados("cidades")
    return True, "Cidade incluída com sucesso."

def excluir_cidade(cod):
    if not indices["cidades"].buscar(cod):
        return False, "Cidade não encontrada."
    
    # Validação de chave estrangeira
    if any(int(aluno[2]) == cod for aluno in dados['alunos'].values()) or \
       any(int(prof[4]) == cod for prof in dados['professores'].values()):
        return False, "Não é possível excluir, cidade em uso por alunos ou professores."
        
    del dados["cidades"][cod]
    indices["cidades"].remover(cod)
    salvar_dados("cidades")
    return True, "Cidade excluída com sucesso."

# --- FUNÇÕES DE ALUNOS ---

def get_todos_alunos_detalhado():
    alunos_detalhados = []
    for aluno in dados["alunos"].values():
        alunos_detalhados.append(get_aluno_detalhado(int(aluno[0])))
    return alunos_detalhados

def get_aluno_detalhado(cod):
    aluno = dados["alunos"].get(cod)
    if not aluno:
        return None
    
    cod_cidade = int(aluno[2])
    cidade_info = dados["cidades"].get(cod_cidade, ["", "N/A", "N/A"])
    
    imc, diag_imc = calcular_imc(aluno[4], aluno[5])
    
    return {
        "cod_aluno": aluno[0],
        "nome": aluno[1],
        "cod_cidade": aluno[2],
        "data_nasc": aluno[3],
        "peso": aluno[4],
        "altura": aluno[5],
        "cidade_nome": cidade_info[1],
        "cidade_uf": cidade_info[2],
        "imc": f"{imc:.2f}",
        "imc_diag": diag_imc
    }

def incluir_aluno(cod, nome, cod_cidade, data_nasc, peso, altura):
    if indices["alunos"].buscar(cod):
        return False, "Código de aluno já existe."
    if not indices["cidades"].buscar(cod_cidade):
        return False, "Cidade não encontrada."
    
    dados["alunos"][cod] = [cod, nome, cod_cidade, data_nasc, peso, altura]
    indices["alunos"].inserir(cod)
    salvar_dados("alunos")
    return True, "Aluno incluído com sucesso."

def excluir_aluno(cod):
    if not indices["alunos"].buscar(cod):
        return False, "Aluno não encontrado."
    if any(int(mat[1]) == cod for mat in dados['matriculas'].values()):
        return False, "Não é possível excluir, aluno possui matrículas."
        
    del dados["alunos"][cod]
    indices["alunos"].remover(cod)
    salvar_dados("alunos")
    return True, "Aluno excluído com sucesso."


# --- FUNÇÕES DE PROFESSORES --- (Simplificado, adicione o resto)

def get_todos_professores_detalhado():
    lista = []
    for prof in dados["professores"].values():
        cod_cidade = int(prof[4])
        cidade_info = dados["cidades"].get(cod_cidade, ["", "N/A", "N/A"])
        lista.append({
            "cod_professor": prof[0],
            "nome": prof[1],
            "endereco": prof[2],
            "telefone": prof[3],
            "cidade_nome": cidade_info[1],
            "cidade_uf": cidade_info[2]
        })
    return lista

def incluir_professor(cod, nome, endereco, telefone, cod_cidade):
    if indices["professores"].buscar(cod):
        return False, "Código de professor já existe."
    if not indices["cidades"].buscar(cod_cidade):
        return False, "Cidade não encontrada."
    
    dados["professores"][cod] = [cod, nome, endereco, telefone, cod_cidade]
    indices["professores"].inserir(cod)
    salvar_dados("professores")
    return True, "Professor incluído com sucesso."

def excluir_professor(cod):
    if not indices["professores"].buscar(cod):
        return False, "Professor não encontrado."
    if any(int(mod[2]) == cod for mod in dados['modalidades'].values()):
        return False, "Não é possível excluir, professor está em uma modalidade."
    
    del dados["professores"][cod]
    indices["professores"].remover(cod)
    salvar_dados("professores")
    return True, "Professor excluído com sucesso."

# --- FUNÇÕES DE MODALIDADES ---

def get_todas_modalidades_detalhado():
    lista = []
    for mod in dados["modalidades"].values():
        cod_prof = int(mod[2])
        prof_info = dados["professores"].get(cod_prof, ["", "N/A"])
        lista.append({
            "cod_modalidade": mod[0],
            "descricao": mod[1],
            "professor_nome": prof_info[1],
            "valor_aula": float(mod[3]),
            "limite_alunos": mod[4],
            "total_alunos": mod[5]
        })
    return lista

def incluir_modalidade(cod, desc, cod_prof, valor, limite):
    if indices["modalidades"].buscar(cod):
        return False, "Código de modalidade já existe."
    if not indices["professores"].buscar(cod_prof):
        return False, "Professor não encontrado."
    
    dados["modalidades"][cod] = [cod, desc, cod_prof, valor, limite, 0]
    indices["modalidades"].inserir(cod)
    salvar_dados("modalidades")
    return True, "Modalidade incluída com sucesso."

def excluir_modalidade(cod):
    if not indices["modalidades"].buscar(cod):
        return False, "Modalidade não encontrada."
    if any(int(mat[2]) == cod for mat in dados['matriculas'].values()):
        return False, "Não é possível excluir, modalidade possui matrículas."
        
    del dados["modalidades"][cod]
    indices["modalidades"].remover(cod)
    salvar_dados("modalidades")
    return True, "Modalidade excluída com sucesso."


# --- FUNÇÕES DE MATRÍCULAS ---

def get_todas_matriculas_detalhado():
    lista = []
    for mat in dados["matriculas"].values():
        cod_aluno = int(mat[1])
        cod_mod = int(mat[2])
        
        aluno_info = dados["alunos"].get(cod_aluno, ["", "N/A"])
        mod_info = dados["modalidades"].get(cod_mod, ["", "N/A", 0, 0.0])
        
        valor_a_pagar = int(mat[3]) * float(mod_info[3])
        
        lista.append({
            "cod_matricula": mat[0],
            "aluno_nome": aluno_info[1],
            "modalidade_desc": mod_info[1],
            "qtde_aulas": mat[3],
            "valor_a_pagar": f"{valor_a_pagar:.2f}"
        })
    return lista

def incluir_matricula(cod, cod_aluno, cod_modalidade, qtde_aulas):
    if indices["matriculas"].buscar(cod):
        return False, "Código de matrícula já existe."
    if not indices["alunos"].buscar(cod_aluno):
        return False, "Aluno não encontrado."
    if not indices["modalidades"].buscar(cod_modalidade):
        return False, "Modalidade não encontrada."

    modalidade = dados["modalidades"][cod_modalidade]
    limite_alunos = int(modalidade[4])
    total_matriculados = int(modalidade[5])

    if total_matriculados >= limite_alunos:
        return False, "Não há vagas nesta modalidade."

    dados["matriculas"][cod] = [cod, cod_aluno, cod_modalidade, qtde_aulas]
    indices["matriculas"].inserir(cod)
    
    dados["modalidades"][cod_modalidade][5] = total_matriculados + 1
    
    salvar_dados("matriculas")
    salvar_dados("modalidades")
    return True, "Matrícula realizada com sucesso."

def excluir_matricula(cod):
    if not indices["matriculas"].buscar(cod):
        return False, "Matrícula não encontrada."
    
    matricula = dados["matriculas"][cod]
    cod_modalidade = int(matricula[2])

    if cod_modalidade in dados["modalidades"]:
        dados["modalidades"][cod_modalidade][5] = int(dados["modalidades"][cod_modalidade][5]) - 1
        salvar_dados("modalidades")
        
    del dados["matriculas"][cod]
    indices["matriculas"].remover(cod)
    salvar_dados("matriculas")
    return True, "Matrícula excluída com sucesso."

# --- FUNÇÕES DE RELATÓRIOS ---

def get_relatorio_faturamento():
    faturamento = {}
    for mod in dados["modalidades"].values():
        cod_mod = int(mod[0])
        valor_aula = float(mod[3])
        total_mod = 0
        for mat in dados["matriculas"].values():
            if int(mat[2]) == cod_mod:
                total_mod += int(mat[3]) * valor_aula
        
        prof_info = dados["professores"].get(int(mod[2]), ["", "N/A"])
        
        faturamento[cod_mod] = {
            "descricao": mod[1],
            "professor_nome": prof_info[1],
            "valor_faturado": f"{total_mod:.2f}"
        }
    return faturamento

def get_relatorio_matriculas_ordenado():
    chaves_ordenadas = indices["matriculas"].obter_chaves_em_ordem()
    valor_total_geral = 0
    matriculas_detalhadas = []

    for cod_matricula in chaves_ordenadas:
        matricula = dados["matriculas"][cod_matricula]
        
        cod_aluno = int(matricula[1])
        aluno_info = dados["alunos"].get(cod_aluno, ["", "N/A", "0"])
        cidade_aluno_info = dados["cidades"].get(int(aluno_info[2]), ["", "N/A"])
        
        cod_modalidade = int(matricula[2])
        modalidade_info = dados["modalidades"].get(cod_modalidade, ["", "N/A", "0", "0.0"])
        
        cod_prof = int(modalidade_info[2])
        prof_info = dados["professores"].get(cod_prof, ["", "N/A"])

        qtde_aulas = int(matricula[3])
        valor_aula = float(modalidade_info[3])
        valor_a_pagar = qtde_aulas * valor_aula
        valor_total_geral += valor_a_pagar
        
        matriculas_detalhadas.append({
            "cod_matricula": matricula[0],
            "aluno_nome": aluno_info[1],
            "cidade_aluno": cidade_aluno_info[1],
            "modalidade_desc": modalidade_info[1],
            "professor_nome": prof_info[1],
            "valor_a_pagar": f"{valor_a_pagar:.2f}"
        })
        
    return {
        "matriculas": matriculas_detalhadas,
        "total_matriculas": len(matriculas_detalhadas),
        "valor_total_geral": f"{valor_total_geral:.2f}"
    }