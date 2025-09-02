# arvore_binaria.py

class No:
    """Nó da Árvore Binária de Busca."""
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None

class ArvoreBinariaBusca:
    """Implementação da Árvore Binária de Busca para indexação."""
    def __init__(self):
        self.raiz = None

    def inserir(self, chave):
        """Método público para inserir uma chave na árvore."""
        if self.raiz is None:
            self.raiz = No(chave)
        else:
            self._inserir_recursivo(self.raiz, chave)

    def _inserir_recursivo(self, no_atual, chave):
        """Método privado e recursivo para inserir uma chave."""
        if chave < no_atual.chave:
            if no_atual.esquerda is None:
                no_atual.esquerda = No(chave)
            else:
                self._inserir_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            if no_atual.direita is None:
                no_atual.direita = No(chave)
            else:
                self._inserir_recursivo(no_atual.direita, chave)
        # Se a chave já existe, não faz nada.

    def buscar(self, chave):
        """Método público para buscar uma chave na árvore."""
        return self._buscar_recursivo(self.raiz, chave)

    def _buscar_recursivo(self, no_atual, chave):
        """Método privado e recursivo para buscar uma chave."""
        if no_atual is None or no_atual.chave == chave:
            return no_atual is not None
        if chave < no_atual.chave:
            return self._buscar_recursivo(no_atual.esquerda, chave)
        else:
            return self._buscar_recursivo(no_atual.direita, chave)
            
    def remover(self, chave):
        """Método público para remover uma chave."""
        self.raiz = self._remover_recursivo(self.raiz, chave)

    def _remover_recursivo(self, no_atual, chave):
        """Método privado e recursivo para remover uma chave."""
        if no_atual is None:
            return no_atual

        if chave < no_atual.chave:
            no_atual.esquerda = self._remover_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._remover_recursivo(no_atual.direita, chave)
        else: # Nó a ser removido encontrado
            # Caso 1: Nó é uma folha ou tem apenas um filho
            if no_atual.esquerda is None:
                return no_atual.direita
            elif no_atual.direita is None:
                return no_atual.esquerda

            # Caso 2: Nó tem dois filhos
            # Encontra o sucessor in-order (menor na subárvore direita)
            temp = self._min_valor_no(no_atual.direita)
            no_atual.chave = temp.chave
            # Remove o sucessor in-order
            no_atual.direita = self._remover_recursivo(no_atual.direita, temp.chave)
            
        return no_atual

    def _min_valor_no(self, no):
        """Encontra o nó com o menor valor em uma subárvore."""
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def obter_chaves_em_ordem(self):
        """Retorna uma lista com todas as chaves em ordem crescente."""
        chaves = []
        self._in_order_traversal(self.raiz, chaves)
        return chaves

    def _in_order_traversal(self, no, chaves):
        """Percorre a árvore em-ordem (esquerda, raiz, direita)."""
        if no:
            self._in_order_traversal(no.esquerda, chaves)
            chaves.append(no.chave)
            self._in_order_traversal(no.direita, chaves)