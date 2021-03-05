from .. import ChessPiece
from chessGame.boardgame.Position import Position
from estruturasDeDados import ListaDuplamenteEncadeada as Lista
import copy

class Pawn(ChessPiece.ChessPiece):

    def __init__(self, board, color, chess_match):
        super().__init__(board, color)
        self.__chess_match = chess_match

    # Sobrecarga toString
    def __str__(self):
        return 'p' if self.color == 'BLACK' else 'P'

    # Sobrecarga possible_moves
    def possible_moves(self):
        mat = Lista.Lista(8, copy.copy(Lista.Lista(8, False)))

        if self.color == 'WHITE':
            # Movimento para cima (1 casa)
            p = Position(self._position.row - 1, self._position.column)
            if self.board.is_position_exists(p.row, p.column) and not self.board.is_there_a_piece(p):
                mat[p.row][p.column] = True

            # Movimento para cima (2 casa)
            p = Position(self._position.row - 2, self._position.column)
            p2 = Position(self._position.row - 1, self._position.column)
            if self.board.is_position_exists(p.row, p.column) and not self.board.is_there_a_piece(p) and self.board.is_position_exists(p2.row, p2.column) and not self.board.is_there_a_piece(p2) and self.move_count == 0:
                mat[p.row][p.column] = True
            
            # Movimento para comer peça adversária (esquerda)
            p = Position(self._position.row - 1, self._position.column - 1)
            if self.board.is_position_exists(p.row, p.column) and self._is_there_opponent_piece(p):
                mat[p.row][p.column] = True

            # Movimento para comer peça adversária (direita)
            p = Position(self._position.row - 1, self._position.column + 1)
            if self.board.is_position_exists(p.row, p.column) and self._is_there_opponent_piece(p):
                mat[p.row][p.column] = True

            # Movimento especial en passant
            if self._position.row == 3:
                left_pawn = Position(self._position.row, self._position.column - 1)
                if self.board.is_position_exists(left_pawn.row, left_pawn.column) and self._is_there_opponent_piece(left_pawn) and self.board.piece(left_pawn.row, left_pawn.column) == self.__chess_match.en_passant_vulnerable:
                    mat[left_pawn.row - 1][left_pawn.column] = True

                right_pawn = Position(self._position.row, self._position.column + 1)
                if self.board.is_position_exists(right_pawn.row, right_pawn.column) and self._is_there_opponent_piece(right_pawn) and self.board.piece(right_pawn.row, right_pawn.column) == self.__chess_match.en_passant_vulnerable:
                    mat[right_pawn.row - 1][right_pawn.column] = True

        else:
            # Movimento para cima (1 casa)
            p = Position(self._position.row + 1, self._position.column)
            if self.board.is_position_exists(p.row, p.column) and not self.board.is_there_a_piece(p):
                mat[p.row][p.column] = True

            # Movimento para cima (2 casa)
            p = Position(self._position.row + 2, self._position.column)
            p2 = Position(self._position.row + 1, self._position.column)
            if self.board.is_position_exists(p.row, p.column) and not self.board.is_there_a_piece(p) and self.board.is_position_exists(p2.row, p2.column) and not self.board.is_there_a_piece(p2) and self.move_count == 0:
                mat[p.row][p.column] = True
            
            # Movimento para comer peça adversária (esquerda)
            p = Position(self._position.row + 1, self._position.column - 1)
            if self.board.is_position_exists(p.row, p.column) and self._is_there_opponent_piece(p):
                mat[p.row][p.column] = True

            # Movimento para comer peça adversária (direita)
            p = Position(self._position.row + 1, self._position.column + 1)
            if self.board.is_position_exists(p.row, p.column) and self._is_there_opponent_piece(p):
                mat[p.row][p.column] = True

            # Movimento especial en passant
            if self._position.row == 4:
                left_pawn = Position(self._position.row, self._position.column - 1)
                if self.board.is_position_exists(left_pawn.row, left_pawn.column) and self._is_there_opponent_piece(left_pawn) and self.board.piece(left_pawn.row, left_pawn.column) == self.__chess_match.en_passant_vulnerable:
                    mat[left_pawn.row + 1][left_pawn.column] = True

                right_pawn = Position(self._position.row, self._position.column + 1)
                if self.board.is_position_exists(right_pawn.row, right_pawn.column) and self._is_there_opponent_piece(right_pawn) and self.board.piece(right_pawn.row, right_pawn.column) == self.__chess_match.en_passant_vulnerable:
                    mat[right_pawn.row + 1][right_pawn.column] = True
            
        return mat