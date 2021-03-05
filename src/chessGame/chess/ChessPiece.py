from abc import ABC, abstractmethod
from .ChessPosition import ChessPosition
from chessGame.boardgame.Piece import Piece

# Classe peça que é visível para o jogador
class ChessPiece(Piece, ABC):
    
    def __init__(self, board, color):
        super().__init__(board)
        self.__color = color
        self.__move_count = 0

    # Getter do atributor cor
    @property
    def color(self):
        return self.__color

    # Getter do atributo contador de movimentos
    @property
    def move_count(self):
        return self.__move_count

    # Recolhe o atributo posição da peça e manda ja no formato char/int
    def chess_position(self):
        return ChessPosition._from_position(self._position)

    # Checa para ver se a peça na posição é do oponente
    def _is_there_opponent_piece(self, position):
        p = self.board.piece(position.row, position.column)
        return (p != None) and (p.color != self.__color)

    # Aumenta um no contador
    def increase_move_count(self):
        self.__move_count += 1

    # Diminui um no contador
    def decrease_move_count(self):
        self.__move_count -= 1