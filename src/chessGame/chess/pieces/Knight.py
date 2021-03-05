from .. import ChessPiece
from chessGame.boardgame.Position import Position
from estruturasDeDados import ListaDuplamenteEncadeada as Lista
import copy

class Knight(ChessPiece.ChessPiece):

    def __init__(self, board, color):
        super().__init__(board, color)

    # Sobrecarga toString
    def __str__(self):
        return 'n' if self.color == 'BLACK' else 'N'

    # Checa se é possível se movimentar
    def __can_move(self, position):
        p = self.board.piece(position.row, position.column)
        return p == None or p.color != self.color

    # Sobrecarga possible_moves
    def possible_moves(self):
        mat = Lista.Lista(8, copy.copy(Lista.Lista(8, False)))

        # Movimentos pra cima/direita
        p = Position(self._position.row - 2, self._position.column + 1)
        if self.board.is_position_exists(p.row, p.column) and self.__can_move(p):
            mat[p.row][p.column] = True

        # Movimentos pra direita/cima
        p = Position(self._position.row - 1, self._position.column + 2)
        if self.board.is_position_exists(p.row, p.column) and self.__can_move(p):
            mat[p.row][p.column] = True

        # Movimentos pra direita/baixo
        p = Position(self._position.row + 1, self._position.column + 2)
        if self.board.is_position_exists(p.row, p.column) and self.__can_move(p):
            mat[p.row][p.column] = True

        # Movimentos pra baixo/direita
        p = Position(self._position.row + 2, self._position.column + 1)
        if self.board.is_position_exists(p.row, p.column) and self.__can_move(p):
            mat[p.row][p.column] = True

        # Movimentos pra baixo/esquerda
        p = Position(self._position.row + 2, self._position.column - 1)
        if self.board.is_position_exists(p.row, p.column) and self.__can_move(p):
            mat[p.row][p.column] = True

        # Movimentos pra esquerda/baixo
        p = Position(self._position.row + 1, self._position.column - 2)
        if self.board.is_position_exists(p.row, p.column) and self.__can_move(p):
            mat[p.row][p.column] = True

        # Movimentos pra esquerda/cima
        p = Position(self._position.row - 1, self._position.column - 2)
        if self.board.is_position_exists(p.row, p.column) and self.__can_move(p):
            mat[p.row][p.column] = True

        # Movimentos pra cima/esquerda
        p = Position(self._position.row - 2, self._position.column - 1)
        if self.board.is_position_exists(p.row, p.column) and self.__can_move(p):
            mat[p.row][p.column] = True

        return mat