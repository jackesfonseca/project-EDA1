import copy

class No:
    # Construtor da classe Nó
    def __init__(self, valor):
        self.__valor = valor
        self.proximo = None
        self.anterior = None

    # Getter do atributo valor
    @property
    def valor(self):
        return self.__valor

    # Setter do atributo valor
    @valor.setter
    def valor(self, valor):
        self.__valor = valor

    # Apenas printa o valor desse Nó
    def __str__(self):
        return str(self.valor)

class Lista:
    # Construtor da lista
    def __init__(self, tamanho = 0, valor_inicial = None):
        # Primeiro elemento (No) da lista
        self.__primeiro = None
        # Ultimo elemento (No) da lista
        self.__ultimo = None
        # Tamanho da lista
        self.__tamanho = 0
        if tamanho != 0:
            self.__initial_lista(tamanho, valor_inicial)
    
    # len 
    def __len__(self):
        return self.__tamanho

    # ex: list[index] = value
    def __setitem__(self, index, valor):
        self.altera_valor(valor, index)

    # ex: list[index]
    def __getitem__(self, index):
        return self.retorna_elemento(index)

    # Getter do atributo tamanho
    @property
    def _tamanho(self):
        return self.__tamanho

    def __initial_lista(self, tamanho, valor_inicial):
        if tamanho < 0:
            raise Warning('Erro, lista vazia.')

        for _ in range(tamanho):
            self.insere_final(copy.deepcopy(valor_inicial))

    def _apaga_lista(self):
        self.__primeiro = None
        self.__ultimo = None
        self.__tamanho = 0

    # Retorna se a lista está vazia
    def __lista_vazia(self):
        return self.__tamanho == 0

    # Função que altera o valor do nó
    def altera_valor(self, valor, indice):
        if indice > self.__tamanho or indice < 0:
            raise IndexError('Erro, elemento fora do array.')

        # Se a lista ja estiver vazia, jogar exceção
        if self.__lista_vazia():
            raise Warning('Erro, lista vazia.')

        node = self.__primeiro
        elemento = 0
        while elemento != indice:
            node = node.proximo
            elemento += 1
        node.valor = valor

    # Insere um termo em cima dos outros (no inicio da lista) O(1)
    def insere_inicio(self, valor):
        # Cria um novo nó
        node = No(valor)
        
        # Caso a lista esteja vazia, esse nó será o ultimo
        if self.__lista_vazia():
            self.__ultimo = node
        # Caso ele nao seja o primeiro elemento inserido,
        # Então o primeiro da lista vai apontar para esse novo elemento
        else:
            self.__primeiro.anterior = node
            
        # Agora, esse novo elemento é o primeiro da lista
        node.proximo = self.__primeiro
        self.__primeiro = node
        self.__tamanho += 1

    # Insere um novo elemento no fim da lista O(1)
    def insere_final(self, valor):
        node = No(valor)

        # Caso a lista esteja vazia, esse será o primeiro termo
        if self.__lista_vazia():
            self.__primeiro = node
        # Apontar o "ponteiro" do nosso ultimo valor para o novo
        else:
            self.__ultimo.proximo = node

        # Agora, o novo é o ultimo elemento da lista
        node.anterior = self.__ultimo
        self.__ultimo = node
        self.__tamanho += 1
    
    # Insere valor na posição desejada O(n)
    def insere_posicao(self, valor, indice):
        if indice > self.__tamanho or indice < 0:
            raise IndexError('Erro, elemento fora do array.')

        # Valor temporário que recebe o endereço do primeiro
        temp = self.__primeiro
        # Posição de insereção é a primeira O(1)
        if indice == 0:
            self.insere_inicio(valor)
        # Posição de inserção é a última O(1)
        elif indice == self.__tamanho:
            self.insere_final(valor)
        # Posição no meio da Lista O(n)
        else:
            elemento = 0
            while elemento != indice - 1:
                temp = temp.proximo
                elemento += 1

            node = No(valor)
            node.anterior = temp
            node.proximo = temp.proximo
            temp.proximo.anterior = node
            temp.proximo = node
            
        # Aumenta o tamanho da Lista
        self.__tamanho += 1

    # Exclução do Início O(1)
    def excluir_inicio(self):
        # Se a lista ja estiver vazia, jogar exceção
        if self.__lista_vazia():
            raise Warning('Erro, lista vazia.')

        # Criar uma variavel temporaria para guardar o primeiro elemento (vai ser apagado)
        temp = self.__primeiro

        # Se o primeiro elemento não aponta pra ninguem, apenas esvaziar a lista, não tem um proximo (1 elemento)
        if self.__primeiro.proximo == None:
            self.__ultimo = None
        # Resetar o ponteiro do próximo termo que apontava pra ele
        else:
            self.__primeiro.proximo.anterior = None
        
        # Agora o primeiro termo é o próximo
        self.__primeiro = self.__primeiro.proximo
        self.__tamanho -= 1
        return temp

    # Exclui o elemento final da lista O(1)
    def excluir_final(self):
        # Se a lista ja estiver vazia, jogar exceção
        if self.__lista_vazia():
            raise Warning('Erro, lista vazia.')

        # Criar uma variavel temporaria para guardar o ultimo elemento (vai ser apagado)
        temp = self.__ultimo

        # Se o ultimo elemento não é aponta por ninguem, apenas esvaziar a lista, não tem um anterior (1 elemento)
        if self.__ultimo.anterior == None:
            self.__primeiro = None
        # Resetar o ponteiro do anterior termo que apontava pra ele
        else:
            self.__ultimo.anterior.proximo = None
        
        # Depois de resetar o ultimo, lembrar de sincronizar o ponteiro
        self.__ultimo = self.__ultimo.anterior
        self.__tamanho -= 1
        return temp
    
    # Exclui o elemento na posicao O(n)
    def excluir_posicao(self, valor):
        # Se a lista ja estiver vazia, jogar exceção
        if self.__lista_vazia():
            raise Warning('Erro, lista vazia.')

        # Elemento temporário, começa do inicio da lista
        temp = self.__primeiro

        # Encontrar o elemento
        while temp.valor != valor:
            # Elemento não encontrado
            temp = temp.proximo
            if temp == None:
                raise Warning('Erro, valor fora da lista.')
        
        # Verificar se esse termo é o primeiro da lista
        # Sincronizar os ponteiros (esquerda)
        if temp == self.__primeiro:
            self.__primeiro = temp.proximo
        else:
            temp.anterior.proximo = temp.proximo

        # Sincronizar os ponteiros (direita)
        if temp == self.__ultimo:
            self.__ultimo = temp.anterior
        else:
            temp.proximo.anterior = temp.anterior
        
        # Retornar o valor removido
        self.__tamanho -= 1
        return temp
    
    # Retorna o elemento selecionado pelo indice O(n)
    def retorna_elemento(self, indice):
        # Indice fora do tamanho do array
        if indice > self.__tamanho or indice < 0:
            raise IndexError('Erro, elemento fora do array.')

        # Se a lista ja estiver vazia, jogar exceção
        if self.__lista_vazia():
            raise Warning('Erro, lista vazia.')

        node = self.__primeiro
        elemento = 0
        # Percorre os elementos até encontrar o indice
        while elemento != indice:
            node = node.proximo
            elemento += 1

        return node.valor

    # Printa do primeiro elemento ao ultimo
    def mostrar_frente(self):
        # Começar do primeiro elemento e ir até o ultimo
        string = ''
        atual = self.__primeiro
        while atual:
            string += str(atual) + ' '
            atual = atual.proximo
        return string

    # Printa do ultimo elemento ao primeiro
    def mostrar_tras(self):
        # Começar do ultimo elemento e ir até o primeiro
        string = ''
        atual = self.__ultimo
        while atual:
            string += str(atual) + ' '
            atual = atual.anterior
        return string