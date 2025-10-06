class No:
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None

class ArvoreBinariaBusca:
    def __init__(self):
        self.raiz = None

    def inserir(self, chave):
        if self.raiz is None:
            self.raiz = No(chave)
        else:
            self._inserir_recursivo(self.raiz, chave)

    def _inserir_recursivo(self, no_atual, chave):
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

    def buscar(self, chave):
        return self._buscar_recursivo(self.raiz, chave)

    def _buscar_recursivo(self, no_atual, chave):
        if no_atual is None or no_atual.chave == chave:
            return no_atual is not None
        if chave < no_atual.chave:
            return self._buscar_recursivo(no_atual.esquerda, chave)
        else:
            return self._buscar_recursivo(no_atual.direita, chave)
            
    def remover(self, chave):
        self.raiz = self._remover_recursivo(self.raiz, chave)

    def _remover_recursivo(self, no_atual, chave):
        if no_atual is None:
            return no_atual

        if chave < no_atual.chave:
            no_atual.esquerda = self._remover_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._remover_recursivo(no_atual.direita, chave)
        else:
            if no_atual.esquerda is None:
                return no_atual.direita
            elif no_atual.direita is None:
                return no_atual.esquerda
            temp = self._min_valor_no(no_atual.direita)
            no_atual.chave = temp.chave
            no_atual.direita = self._remover_recursivo(no_atual.direita, temp.chave)
            
        return no_atual

    def _min_valor_no(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def obter_chaves_em_ordem(self):
        chaves = []
        self._in_order_traversal(self.raiz, chaves)
        return chaves

    def _in_order_traversal(self, no, chaves):
        if no:
            self._in_order_traversal(no.esquerda, chaves)
            chaves.append(no.chave)
            self._in_order_traversal(no.direita, chaves)