from . import ListaDuplamenteEncadeada

class Pilha(ListaDuplamenteEncadeada.Lista):
    def __init__(self):
        super().__init__()

    def __eq__(self, other):
        for elemento in range(self._tamanho):
            if self.retorna_elemento(elemento) != other[elemento]:
                return False
        return True

    # Empilha um novo valor no topo da pilha O(1)
    def empilhar(self, valor):
        self.insere_final(valor)

    # Retira o valor do topo da pilha O(1)
    # caso seja passado o segundo atributo, seram retirados n elementos O(n)
    def desempilha(self, quantidade = 1):
        if quantidade == 1:
            self.excluir_final()
        else:
            for _ in range(quantidade):
                self.excluir_final()

    # Visualiza o elemento do topo O(1)
    def retorna_topo(self):
        if self._tamanho == 0:
            return None
        return self.retorna_elemento(self._tamanho - 1)

    # Altera valor do topo O(1)
    def altera_topo(self, valor):
        self.altera_valor(valor, self._tamanho - 1)

    def limpa_pilha(self):
        self._apaga_lista()