from .. import ChessPiece
from chessGame.boardgame.Position import Position
from estruturasDeDados import ListaDuplamenteEncadeada as Lista
import copy

class Rook(ChessPiece.ChessPiece):

    def __init__(self, board, color):
        super().__init__(board, color)

    # Sobrecarga toString
    def __str__(self):
        return 'r' if self.color == 'BLACK' else 'R'

    # Sobrecarga possible_moves
    def possible_moves(self):
        mat = Lista.Lista(8, copy.copy(Lista.Lista(8, False)))

        # Movimentos pra cima
        p = Position(self._position.row - 1, self._position.column)
        while self.board.is_position_exists(p.row, p.column) and not self.board.is_there_a_piece(p):
            mat[p.row][p.column] = True
            p.row -= 1
        if self.board.is_position_exists(p.row, p.column) and self._is_there_opponent_piece(p):
            mat[p.row][p.column] = True

        # Movimentos pra baixo
        p = Position(self._position.row + 1, self._position.column)
        while self.board.is_position_exists(p.row, p.column) and not self.board.is_there_a_piece(p):
            mat[p.row][p.column] = True
            p.row += 1
        if self.board.is_position_exists(p.row, p.column) and self._is_there_opponent_piece(p):
            mat[p.row][p.column] = True

        # Movimentos pra direita
        p = Position(self._position.row, self._position.column + 1)
        while self.board.is_position_exists(p.row, p.column) and not self.board.is_there_a_piece(p):
            mat[p.row][p.column] = True
            p.column += 1
        if self.board.is_position_exists(p.row, p.column) and self._is_there_opponent_piece(p):
            mat[p.row][p.column] = True

        # Movimentos pra esquerda
        p = Position(self._position.row, self._position.column - 1)
        while self.board.is_position_exists(p.row, p.column) and not self.board.is_there_a_piece(p):
            mat[p.row][p.column] = True
            p.column -= 1
        if self.board.is_position_exists(p.row, p.column) and self._is_there_opponent_piece(p):
            mat[p.row][p.column] = True

        return mat