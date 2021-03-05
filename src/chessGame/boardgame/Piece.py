from estruturasDeDados import ListaDuplamenteEncadeada as Lista
from abc import ABC, abstractmethod
import copy

# Classe responsável por implementa a classe Peça abstrata
class Piece(ABC):

    def __init__(self, board):
        self.__board = board
        self._position = None

    # Getter do atributo position
    @property
    def board(self):
        return self.__board

    # Método abstrato a ser implementado em classes filhas
    @abstractmethod
    def possible_moves(self):
        pass

    #  Retorna True ou False para a posição passada
    def is_possible_move(self, position):
        return self.possible_moves()[position.row][position.column]

    # Checa se existe pelo menos 1 movimento possível
    def is_there_any_possible_move(self):
        mat = self.possible_moves()
        for i in range(len(mat)):
            for j in range(len(mat)):
                if mat[i][j]:
                    return True
        return False