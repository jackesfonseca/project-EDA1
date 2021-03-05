# Cores possíveis
BLACK = 'BLACK'
RED = 'RED'
NIL = 'NIL'

class Node:
    def __init__(self, value, color, data, parent, left = None, right = None):
        self.value = value
        self.color = color
        self.data = data
        self.parent = parent
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.value}: {self.data}'

    # Comparação de nós
    def __eq__(self, other):
        # Comparacao do nó com nada
        if other == None:
            return False

        # Nó é uma folha (cor NIL) e o outro nó também é uma folha
        if self.color == NIL and self.color == other.color:
            return True

        # Se o pai de qualquer um dos nós for None ou seja raiz
        if self.parent is None or other.parent is None:
            # Se ambos pais forem a raiz, eles possuem o mesmo pai
            parents_are_same = self.parent is None and other.parent is None
        else:
            # Se ambos pais tiverem o mesmo valor e mesma cor, então possuem o mesmo pai
            parents_are_same = self.parent.value == other.parent.value and self.parent.color == other.parent.color
        # Assim, se ambos possuirem o mesmo valor, mesma cor e mesmo pai, eles são iguais (True)
        return self.value == other.value and self.color == other.color and parents_are_same

class RedBlackTree:
    NIL_LEAF = Node(None, color = NIL, data=None, parent = None)

    def __init__(self):
        self.count = 0
        self.root = None
    
    def inOrder(self, node = None):
        result = []
        node = self.root if node is None else node
        if node != self.NIL_LEAF:
            result += self.inOrder(node.left)
            result += [str(node) + ', color: ' + str(node.color)]
            result += self.inOrder(node.right)
        return result

    # Adição normal de uma Árvore Binária
    def add(self, value, data):
        # Não exite raiz
        if not self.root:
            self.root = Node(value, color = BLACK, data=data, parent = None, left = self.NIL_LEAF, right = self.NIL_LEAF)
            self.count += 1
            return
        
        # Valor ja se encontra na arvore
        parent, node_dir = self.__find_parent(value, data, self.root)
        if node_dir is None:
            return
        
        # Adição do valor
        new_node = Node(value, color = RED, data=data, parent = parent, left = self.NIL_LEAF, right = self.NIL_LEAF)
        if node_dir == 'R':
            parent.right = new_node
        else:
            parent.left = new_node

        self.__try_rebance(new_node)
        self.count += 1

    def __try_rebance(self, node):
        parent = node.parent
        value = node.value

        # Se o pai do nó adicionado é a raiz ou se a cor do pai não for vermelha, não é necessário rebalancear
        if (parent is None) or (parent.parent is None) or (node.color != RED or parent.color != RED):
            return

        grandparent = parent.parent
        node_dir = 'L' if value < parent.value else 'R'
        parent_dir = 'L' if parent.value < grandparent.value else 'R'
        uncle = grandparent.right if parent_dir == 'L' else grandparent.left
        general_dir = node_dir + parent_dir

        # EM AMBOS CASOS É NECESSÁRIO FAZER A ROTAÇÃO E A COLORAÇÃO (ordens diferentes)
        # Primeiro caso (rotação), caso o tio seja um folha ou se o tio for black
        if uncle == self.NIL_LEAF or uncle.color == BLACK:
            # Ambos para a esquerda
            if general_dir == 'LL':
                self.__right_rotation(node, parent, grandparent, to_recolor = True)
            # Ambos para a direita
            elif general_dir == 'RR':
                self.__left_rotation(node, parent, grandparent, to_recolor = True)
            # Filho para a esquerda e pai para a direita
            elif general_dir == 'LR':
                self.__right_rotation(node = None, parent = node, grandparent = parent)
                self.__left_rotation(node = parent, parent = node, grandparent = grandparent, to_recolor = True)
            # Filho para a direita e pai para a esquerda
            elif general_dir == 'RL':
                self.__left_rotation(node = None, parent = node, grandparent = parent)
                self.__right_rotation(node = parent, parent = node, grandparent = grandparent, to_recolor = True)
            else:
                raise Exception(f'{general_dir} não é uma direção válida!')
        # Segundo caso (recoloração), o tio é red
        else:
            self.__recolor(grandparent)

    def __update_parent(self, node, parent_old_child, new_parent):
        node.parent = new_parent
        if new_parent:
            # Valor do novo pai é maior que o do filho antigo
            if new_parent.value > parent_old_child.value:
                # filho a esquerda é o nó
                new_parent.left = node
            else:
                # filho a direita é o nó
                new_parent.right = node
        else:
            self.root = node

    def __right_rotation(self, node, parent, grandparent, to_recolor = False):
        grand_grandparent = grandparent.parent
        # O novo pai do pai vira o pai do avô, e o avô vira filho do pai
        # Faz a ligação pai do avô -> pai
        self.__update_parent(node = parent, parent_old_child = grandparent, new_parent = grand_grandparent)

        # Faz a ligação pai -> avô e avô -> pai
        old_right = parent.right
        parent.right = grandparent
        grandparent.parent = parent

        # Valores que antes se encontravam a direita do pai, são jogados para a esquerda do avô
        grandparent.left = old_right
        old_right.parent = grandparent
        
        # Caso seja necessário recolorir, LL e RL (ou seja, direção do pai para a esquerda)
        if to_recolor:
            parent.color = BLACK
            node.color = RED
            grandparent.color = RED
    
    def __left_rotation(self, node, parent, grandparent, to_recolor = False):
        grand_grandparent = grandparent.parent
        # O novo pai do pai vira o pai do avô, e o avô vira filho do pai
        # Faz a ligação pai do avô -> pai
        self.__update_parent(node = parent, parent_old_child = grandparent, new_parent = grand_grandparent)

        # Faz a ligação pai -> avô e avô -> pai
        old_left = parent.left
        parent.left = grandparent
        grandparent.parent = parent

        # Valores que antes se encontravam a esquerda do pai, são jogados para a direita do avô
        grandparent.right = old_left
        old_left.parent = grandparent
        
        # Caso seja necessário recolorir, RR e LR (ou seja, direção do pai para a direita)
        if to_recolor:
            parent.color = BLACK
            node.color = RED
            grandparent.color = RED

    def __recolor(self, grandparent):
        grandparent.right.color = BLACK
        grandparent.left.color = BLACK
        if grandparent != self.root:
            grandparent.color = RED
        self.__try_rebance(grandparent)

    # Checa se um nó ja está na árvore e se não estiver retorna a direção que deve ser inserido
    def __find_parent(self, value, data, parent):
        if data == parent.data:
            return None, None
        elif value >= parent.value:
            if parent.right.color == NIL:
                return parent, 'R'
            return self.__find_parent(value, data, parent.right)
        else:
            if parent.left.color == NIL:
                return parent, 'L'
            return self.__find_parent(value, data, parent.left)

    def max3(self) -> (Node, Node, Node):
        """ Retorna os tres maiores valores da arvore """
        node = self.root
        # Caso nao haja elementos na arvore
        if node is None:
            return self.NIL_LEAF, self.NIL_LEAF, self.NIL_LEAF

        ########################### Primeiro node return sempre o max
        # Encontra o no mais a direita
        while node.right != self.NIL_LEAF:
            node = node.right

        ########################### Segundo node return left ou parente caso nao tenha left
        if node.left != self.NIL_LEAF:
            node2 = self.max(node.left)
        elif node.parent:
            node2 = node.parent   
        else:
            node2 = self.NIL_LEAF

        ########################### Terceiro depende do caso do segundo
        ## Testa se tem left ou parent, caso left retorna max
        if node2.left != self.NIL_LEAF and node2 != self.NIL_LEAF:
            node3 = self.max(node2.left)
        elif node2.parent:
            ## Caso parent testa se eh o mesmo que node, se for retorna parent de node
            if node2.parent == node:
                if node.parent:
                    node3 = node.parent   
                else:
                    node3 = self.NIL_LEAF
            else:
                node3 = node2.parent
        else:
            node3 = self.NIL_LEAF

        return node, node2, node3

    def max(self, node=None):
        """ Retorna o no com o valor maximo na arvore """
        if not node:
            node = self.root
        # Encontra o no mais a direita
        while node.right != self.NIL_LEAF:
            node = node.right
        return node

    def min3(self) -> (Node, Node, Node):
        """ Retorna os tres menores valores da arvore """
        node = self.root
        # Caso nao haja elementos na arvore
        if node is None:
            return self.NIL_LEAF, self.NIL_LEAF, self.NIL_LEAF

        ########################### Primeiro node return sempre o min
        # Encontra o no mais a direita
        while node.left != self.NIL_LEAF:
            node = node.left

        ########################### Segundo node return right ou parente caso nao tenha right
        if node.right != self.NIL_LEAF:
            node2 = self.min(node.right)
        elif node.parent:
            node2 = node.parent   
        else:
            node2 = self.NIL_LEAF

        ########################### Terceiro depende do caso do segundo
        ## Testa se tem right ou parent
        # caso right retorna min
        if node2.right != self.NIL_LEAF and node2 != self.NIL_LEAF:
            node3 = self.min(node2.right)
        elif node2.parent:
            ## Caso parent testa se eh o mesmo que node, se for retorna parent de node
            if node2.parent == node:
                if node.parent:
                    node3 = node.parent   
                else:
                    node3 = self.NIL_LEAF
            else:
                node3 = node2.parent
        else:
            node3 = self.NIL_LEAF

        return node, node2, node3

    def min(self, node=None):
        """ Retorna o no com o valor menor na arvore """
        if not node:
            node = self.root
        # Encontra o no mais a direita
        while node.left != self.NIL_LEAF:
            node = node.left
        return node