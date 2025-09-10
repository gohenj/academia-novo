# gestao_academia.py
#gi otario

import os
from datetime import datetime
from arvore_binaria import ArvoreBinariaBusca

# --- ESTRUTURA DOS DADOS E ARQUIVOS ---

# Dicionários para armazenar os dados em memória
dados = {
    "cidades": {},
    "alunos": {},
    "professores": {},
    "modalidades": {},
    "matriculas": {}
}

# Árvores de índice para cada tabela
indices = {
    "cidades": ArvoreBinariaBusca(),
    "alunos": ArvoreBinariaBusca(),
    "professores": ArvoreBinariaBusca(),
    "modalidades": ArvoreBinariaBusca(),
    "matriculas": ArvoreBinariaBusca()
}

# Nomes dos arquivos de dados
arquivos = {
    "cidades": "cidades.txt",
    "alunos": "alunos.txt",
    "professores": "professores.txt",
    "modalidades": "modalidades.txt",
    "matriculas": "matriculas.txt"
}

# --- FUNÇÕES AUXILIARES DE MANIPULAÇÃO DE DADOS ---

def carregar_dados():
    """Carrega os dados dos arquivos de texto para a memória e constrói os índices."""
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
    print("Dados carregados com sucesso!\n")

def salvar_dados(tabela):
    """Salva os dados de uma tabela da memória para o arquivo de texto."""
    nome_arquivo = arquivos[tabela]
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        # Usamos o índice para obter as chaves em ordem e garantir consistência
        chaves_ordenadas = sorted(dados[tabela].keys())
        for chave in chaves_ordenadas:
            linha = ";".join(map(str, dados[tabela][chave]))
            f.write(f"{linha}\n")

# --- FUNÇÕES DE LÓGICA DE NEGÓCIO E VALIDAÇÃO ---

def calcular_imc(peso, altura):
    """Calcula o IMC e retorna o valor e o diagnóstico."""
    if altura == 0:
        return 0, "Altura inválida"
    imc = peso / (altura * altura)
    if imc < 18.5:
        diagnostico = "Abaixo do peso"
    elif 18.5 <= imc < 25:
        diagnostico = "Peso normal"
    elif 25 <= imc < 30:
        diagnostico = "Sobrepeso"
    else:
        diagnostico = "Obesidade"
    return imc, diagnostico

# --- FUNÇÕES DE CRUD (INCLUSÃO, CONSULTA, EXCLUSÃO, LISTAGEM) ---

# 1. CIDADES
def incluir_cidade():
    try:
        cod = int(input("Código da Cidade: "))
        if indices["cidades"].buscar(cod):
            print("\nERRO: Código de cidade já existe!")
            input()
            return
        
        desc = input("Descrição (Nome da Cidade): ")
        uf = input("Estado (UF): ")
        
        dados["cidades"][cod] = [cod, desc, uf]
        indices["cidades"].inserir(cod)
        salvar_dados("cidades")
        print("\nCidade incluída com sucesso!")
        input()
    except ValueError:
        print("\nERRO: Código deve ser um número inteiro.")

def consultar(tabela, nome_tabela):
    try:
        cod = int(input(f"Código do(a) {nome_tabela} a consultar: "))
        if not indices[tabela].buscar(cod):
            print(f"\nERRO: {nome_tabela.capitalize()} com código {cod} não encontrado(a).")
            input()
            return None
        return dados[tabela][cod]
    except ValueError:
        print("\nERRO: Código deve ser um número inteiro.")
        input()
        return None
    
def listar_todos(tabela, cabecalho):
    print(f"\n--- Listagem de {tabela.capitalize()} ---")
    if not dados[tabela]:
        print("Nenhum registro encontrado.")
        input()
        return
        
    print(cabecalho)
    print("-" * 50)
    for registro in dados[tabela].values():
        if tabela == 'alunos':
            # Requisito 2
            cod_cidade = int(registro[2])
            cidade_info = dados["cidades"].get(cod_cidade, ["", "N/A", "N/A"])
            print(f"{registro[0]:<5} | {registro[1]:<20} | {cidade_info[1]} ({cidade_info[2]})")
        elif tabela == 'professores':
            # Requisito 3
            cod_cidade = int(registro[4])
            cidade_info = dados["cidades"].get(cod_cidade, ["", "N/A", "N/A"])
            print(f"{registro[0]:<5} | {registro[1]:<20} | {cidade_info[1]} ({cidade_info[2]})")
        elif tabela == 'modalidades':
            # Requisito 4
            cod_prof = int(registro[2])
            prof_info = dados["professores"].get(cod_prof, ["", "N/A"])
            print(f"{registro[0]:<5} | {registro[1]:<20} | {prof_info[1]:<20} | R${float(registro[3]):.2f} | {registro[5]}/{registro[4]}")
        elif tabela == 'cidades':
            print(f"{registro[0]:<5} | {registro[1]:<20} | {registro[2]}")
        elif tabela == 'matriculas':
            print(f"{registro[0]:<5} | {registro[1]:<20} | {registro[2]:<20} | {registro[3]}")
        else:
            print(" | ".join(map(str, registro)))
    print("-" * 50)
    input()

def excluir(tabela, nome_tabela):
    try:
        cod = int(input(f"Código do(a) {nome_tabela} a excluir: "))
        if not indices[tabela].buscar(cod):
            print(f"\nERRO: {nome_tabela.capitalize()} com código {cod} não encontrado(a).")
            return
        
        # Lógica de validação de chave estrangeira (simplificada)
        if tabela == 'cidades':
            if any(int(aluno[2]) == cod for aluno in dados['alunos'].values()) or \
               any(int(prof[4]) == cod for prof in dados['professores'].values()):
                print("\nERRO: Não é possível excluir esta cidade, pois ela está associada a alunos ou professores.")
                input()
                return
        # Adicionar mais validações para outras tabelas se necessário

        del dados[tabela][cod]
        indices[tabela].remover(cod)
        salvar_dados(tabela)
        print(f"\n{nome_tabela.capitalize()} com código {cod} excluído(a) com sucesso.")
        input()

    except ValueError:
        print("\nERRO: Código deve ser um número inteiro.")

# 2. ALUNOS
def incluir_aluno():
    try:
        cod = int(input("Código do Aluno: "))
        if indices["alunos"].buscar(cod):
            print("\nERRO: Código de aluno já existe!")
            return
        
        nome = input("Nome: ")
        cod_cidade = int(input("Código da Cidade: "))
        if not indices["cidades"].buscar(cod_cidade):
            print("\nERRO: Código de cidade não existe!")
            return
            
        data_nasc = input("Data de Nascimento (DD/MM/AAAA): ")
        peso = float(input("Peso (kg): "))
        altura = float(input("Altura (m): "))
        
        dados["alunos"][cod] = [cod, nome, cod_cidade, data_nasc, peso, altura]
        indices["alunos"].inserir(cod)
        salvar_dados("alunos")
        print("\nAluno incluído com sucesso!")
    except ValueError:
        print("\nERRO: Verifique se os códigos, peso e altura são números válidos.")

def consultar_aluno():
    registro = consultar("alunos", "aluno")
    if registro:
        print("\n--- Dados do Aluno ---")
        cod_cidade = int(registro[2])
        cidade_info = dados["cidades"].get(cod_cidade, ["", "Cidade Desconhecida", ""])
        
        peso = float(registro[4])
        altura = float(registro[5])
        imc, diag_imc = calcular_imc(peso, altura)
        
        print(f"Código: {registro[0]}")
        print(f"Nome: {registro[1]}")
        print(f"Cidade: {cidade_info[1]} - {cidade_info[2]}") # Requisito 2
        print(f"Data de Nascimento: {registro[3]}")
        print(f"Peso: {peso} kg")
        print(f"Altura: {altura} m")
        print(f"IMC: {imc:.2f} ({diag_imc})") # Requisito 2.1
        print("---------------------\n")

# 3. PROFESSORES
def incluir_professor():
    try:
        cod = int(input("Código do Professor: "))
        if indices["professores"].buscar(cod):
            print("\nERRO: Código de professor já existe!")
            return
        
        nome = input("Nome: ")
        endereco = input("Endereço: ")
        telefone = input("Telefone: ")
        cod_cidade = int(input("Código da Cidade: "))
        if not indices["cidades"].buscar(cod_cidade):
            print("\nERRO: Código de cidade não existe!")
            return
        
        dados["professores"][cod] = [cod, nome, endereco, telefone, cod_cidade]
        indices["professores"].inserir(cod)
        salvar_dados("professores")
        print("\nProfessor incluído com sucesso!")
    except ValueError:
        print("\nERRO: Código deve ser um número inteiro.")

def consultar_professor():
    registro = consultar("professores", "professor")
    if registro:
        print("\n--- Dados do Professor ---")
        cod_cidade = int(registro[4])
        cidade_info = dados["cidades"].get(cod_cidade, ["", "Cidade Desconhecida", ""])
        
        print(f"Código: {registro[0]}")
        print(f"Nome: {registro[1]}")
        print(f"Endereço: {registro[2]}")
        print(f"Telefone: {registro[3]}")
        print(f"Cidade: {cidade_info[1]} - {cidade_info[2]}") # Requisito 3
        print("------------------------\n")

# 4. MODALIDADES
def incluir_modalidade():
    try:
        cod = int(input("Código da Modalidade: "))
        if indices["modalidades"].buscar(cod):
            print("\nERRO: Código de modalidade já existe!")
            return
            
        desc = input("Descrição da Modalidade: ")
        cod_prof = int(input("Código do Professor: "))
        if not indices["professores"].buscar(cod_prof):
            print("\nERRO: Código de professor não existe!")
            return
        
        valor_aula = float(input("Valor da Aula: "))
        limite = int(input("Limite de Alunos: "))
        
        dados["modalidades"][cod] = [cod, desc, cod_prof, valor_aula, limite, 0] # Total de alunos começa em 0
        indices["modalidades"].inserir(cod)
        salvar_dados("modalidades")
        
        # Requisito 4: Exibir nome do professor e cidade ao incluir
        prof_info = dados["professores"][cod_prof]
        cidade_info = dados["cidades"][int(prof_info[4])]
        print("\nModalidade incluída com sucesso!")
        print(f"Professor responsável: {prof_info[1]} de {cidade_info[1]}")
        
    except ValueError:
        print("\nERRO: Verifique se os códigos e valores são números válidos.")
        
def consultar_modalidade():
    registro = consultar("modalidades", "modalidade")
    if registro:
        print("\n--- Dados da Modalidade ---")
        cod_prof = int(registro[2])
        prof_info = dados["professores"].get(cod_prof, ["", "Professor Desconhecido"])
        cod_cidade_prof = int(prof_info[4])
        cidade_info_prof = dados["cidades"].get(cod_cidade_prof, ["", "Cidade Desconhecida"])
        
        print(f"Código: {registro[0]}")
        print(f"Descrição: {registro[1]}")
        print(f"Professor: {prof_info[1]} (Cidade: {cidade_info_prof[1]})") # Requisito 4
        print(f"Valor da Aula: R$ {float(registro[3]):.2f}")
        print(f"Vagas: {registro[5]} / {registro[4]}")
        print("-------------------------\n")


# 5. MATRÍCULAS
def incluir_matricula():
    try:
        cod = int(input("Código da Matrícula: "))
        if indices["matriculas"].buscar(cod):
            print("\nERRO: Código de matrícula já existe!")
            return
            
        cod_aluno = int(input("Código do Aluno: "))
        if not indices["alunos"].buscar(cod_aluno):
            print("\nERRO: Aluno não encontrado!")
            return

        cod_modalidade = int(input("Código da Modalidade: "))
        if not indices["modalidades"].buscar(cod_modalidade):
            print("\nERRO: Modalidade não encontrada!")
            return

        modalidade = dados["modalidades"][cod_modalidade]
        limite_alunos = int(modalidade[4])
        total_matriculados = int(modalidade[5])
        
        # Requisito 5.1: Verificar vagas
        if total_matriculados >= limite_alunos:
            print("\nERRO: Não há vagas disponíveis nesta modalidade.")
            return
            
        qtde_aulas = int(input("Quantidade de Aulas: "))
        
        # Requisito 5.2: Inserir e incrementar
        dados["matriculas"][cod] = [cod, cod_aluno, cod_modalidade, qtde_aulas]
        indices["matriculas"].inserir(cod)
        
        dados["modalidades"][cod_modalidade][5] = total_matriculados + 1
        
        salvar_dados("matriculas")
        salvar_dados("modalidades")

        # Requisito 5 e 5.3
        aluno_info = dados["alunos"][cod_aluno]
        cidade_aluno_info = dados["cidades"][int(aluno_info[2])]
        valor_aula = float(modalidade[3])
        valor_a_pagar = qtde_aulas * valor_aula
        
        print("\nMatrícula realizada com sucesso!")
        print(f"Aluno: {aluno_info[1]} (Cidade: {cidade_aluno_info[1]})")
        print(f"Modalidade: {modalidade[1]}")
        print(f"Valor a pagar: R$ {valor_a_pagar:.2f}")

    except ValueError:
        print("\nERRO: Verifique se os códigos são números válidos.")

def consultar_matricula():
    registro = consultar("matriculas", "matrícula")
    if registro:
        print("\n--- Dados da Matrícula ---")
        cod_aluno = int(registro[1])
        cod_modalidade = int(registro[2])
        qtde_aulas = int(registro[3])

        aluno_info = dados["alunos"].get(cod_aluno, ["", "Aluno Desconhecido"])
        cidade_aluno_info = dados["cidades"].get(int(aluno_info[2]), ["", ""])
        modalidade_info = dados["modalidades"].get(cod_modalidade, ["", "Modalidade Desconhecida"])
        valor_aula = float(modalidade_info[3])
        valor_a_pagar = qtde_aulas * valor_aula
        
        print(f"Código da Matrícula: {registro[0]}")
        print(f"Aluno: {aluno_info[1]} (Cidade: {cidade_aluno_info[1]})") # Requisito 5
        print(f"Modalidade: {modalidade_info[1]}") # Requisito 5
        print(f"Valor a pagar: R$ {valor_a_pagar:.2f}") # Requisito 5.3
        print("------------------------\n")

def excluir_matricula():
    try:
        cod = int(input("Código da Matrícula a excluir: "))
        if not indices["matriculas"].buscar(cod):
            print("\nERRO: Matrícula não encontrada.")
            return

        matricula = dados["matriculas"][cod]
        cod_modalidade = int(matricula[2])

        # Requisito 5.4: Subtrair do total de matriculados
        if cod_modalidade in dados["modalidades"]:
            dados["modalidades"][cod_modalidade][5] = int(dados["modalidades"][cod_modalidade][5]) - 1
            salvar_dados("modalidades")
            
        del dados["matriculas"][cod]
        indices["matriculas"].remover(cod)
        salvar_dados("matriculas")
        
        print("\nMatrícula excluída com sucesso.")

    except ValueError:
        print("\nERRO: Código deve ser um número inteiro.")

# --- RELATÓRIOS ---

def relatorio_faturamento_modalidade():
    print("\n--- Relatório de Faturamento por Modalidade ---")
    try:
        cod_modalidade = int(input("Digite o código da modalidade: "))
        if not indices["modalidades"].buscar(cod_modalidade):
            print("\nERRO: Modalidade não encontrada.")
            return

        modalidade = dados["modalidades"][cod_modalidade]
        cod_prof = int(modalidade[2])
        prof_info = dados["professores"][cod_prof]
        cidade_prof_info = dados["cidades"][int(prof_info[4])]
        valor_aula = float(modalidade[3])
        
        faturamento_total = 0
        for matricula in dados["matriculas"].values():
            if int(matricula[2]) == cod_modalidade:
                qtde_aulas = int(matricula[3])
                faturamento_total += qtde_aulas * valor_aula

        print("\n--- Faturamento da Modalidade ---")
        print(f"Descrição: {modalidade[1]}")
        print(f"Professor: {prof_info[1]} (Cidade: {cidade_prof_info[1]})")
        print(f"Valor Faturado: R$ {faturamento_total:.2f}")
        print("---------------------------------")
        
    except ValueError:
        print("\nERRO: Código deve ser um número inteiro.")

def relatorio_matriculas_ordenado():
    print("\n--- Relatório Geral de Matrículas (Ordenado por Código) ---")
    if not dados["matriculas"]:
        print("Nenhuma matrícula encontrada.")
        return

    # Usando o método da árvore para obter as chaves já em ordem
    chaves_ordenadas = indices["matriculas"].obter_chaves_em_ordem()
    valor_total_geral = 0
    total_alunos_matriculados = len(chaves_ordenadas)

    # Cabeçalho
    print(f"{'Cód':<5} | {'Aluno':<20} | {'Cidade Aluno':<15} | {'Modalidade':<20} | {'Professor':<20} | {'Valor Pago'}")
    print("-" * 105)

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

        print(f"{matricula[0]:<5} | {aluno_info[1]:<20} | {cidade_aluno_info[1]:<15} | {modalidade_info[1]:<20} | {prof_info[1]:<20} | R$ {valor_a_pagar:<8.2f}")

    print("-" * 105)
    print(f"Quantidade Total de Alunos Matriculados: {total_alunos_matriculados}")
    print(f"Valor Total Geral a ser Pago: R$ {valor_total_geral:.2f}")
    print("-" * 105)
    input()
# --- MENUS DE INTERFACE ---

def menu_gerenciar(tabela, nome_tabela):
    while True:
        print(f"\n--- Gerenciar {nome_tabela.capitalize()} ---")
        print(f"1. Incluir {nome_tabela}")
        print(f"2. Consultar {nome_tabela}")
        print(f"3. Excluir {nome_tabela}")
        print(f"4. Listar Todos")
        print("5. Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            if tabela == 'cidades': incluir_cidade()
            elif tabela == 'alunos': incluir_aluno()
            elif tabela == 'professores': incluir_professor()
            elif tabela == 'modalidades': incluir_modalidade()
            elif tabela == 'matriculas': incluir_matricula()
        elif opcao == '2':
            if tabela == 'cidades': print(consultar('cidades', 'cidade'))
            elif tabela == 'alunos': consultar_aluno()
            elif tabela == 'professores': consultar_professor()
            elif tabela == 'modalidades': consultar_modalidade()
            elif tabela == 'matriculas': consultar_matricula()
        elif opcao == '3':
            if tabela == 'matriculas': excluir_matricula()
            else: excluir(tabela, nome_tabela)
        elif opcao == '4':
            if tabela == 'alunos': listar_todos('alunos', f"{'Cód':<5} | {'Nome':<20} | {'Cidade'}")
            elif tabela == 'professores': listar_todos('professores', f"{'Cód':<5} | {'Nome':<20} | {'Cidade'}")
            elif tabela == 'modalidades': listar_todos('modalidades', f"{'Cód':<5} | {'Descrição':<20} | {'Professor':<20} | {'Valor':<10} | {'Vagas'}")
            elif tabela == 'cidades':listar_todos('cidades', f"{'Código':<5} | {'Descrição':<20} | {'UF'}")
            elif tabela == 'matriculas': listar_todos('matriculas', f"{'Cód':<5} | {'Cód Aluno':<20} | {'Cód Modalidade':<20} | {'Qtde Aulas'}")
        elif opcao == '5':
            
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def menu_principal():
    while True:
        print("\n===== Academia PowerOn - Sistema de Gestão =====")
        print("1. Gerenciar Cidades")
        print("2. Gerenciar Alunos")
        print("3. Gerenciar Professores")
        print("4. Gerenciar Modalidades")
        print("5. Gerenciar Matrículas")
        print("6. Relatório de Faturamento por Modalidade")
        print("7. Relatório Geral de Matrículas")
        print("8. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_gerenciar('cidades', 'cidade')
        elif opcao == '2':
            menu_gerenciar('alunos', 'aluno')
        elif opcao == '3':
            menu_gerenciar('professores', 'professor')
        elif opcao == '4':
            menu_gerenciar('modalidades', 'modalidade')
        elif opcao == '5':
            menu_gerenciar('matriculas', 'matrícula')
        elif opcao == '6':
            relatorio_faturamento_modalidade()
        elif opcao == '7':
            relatorio_matriculas_ordenado()
        elif opcao == '8':
            print("\nSalvando dados e finalizando o sistema...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")


# --- PONTO DE ENTRADA DO PROGRAMA ---
if __name__ == "__main__":
    carregar_dados()
    menu_principal()