from .ChessException import ChessException
from chessGame.boardgame.Position import Position

class ChessPosition:

    def __init__(self, column, row):
        if (row < 1 or row > 8) or (column < 'a' or column > 'h'):
            raise ChessException(f'Posição {column}{row} invalida, apenas a1 até h8')
        self.__row = row
        self.__column = column

    # Getter do atributo row(int)
    @property
    def row(self):
        return self.__row

    # Getter do atributo column(char)
    @property
    def column(self):
        return self.__column

    # Conversão do formato char/int para int/int(matriz)
    def _to_position(self):
        return Position(8 - self.__row, ord(self.__column) - ord('a'))
    
    # Conversão do formato int/int(matriz) para char/int
    @staticmethod
    def _from_position(position):
        return ChessPosition(chr(ord('a') + position.column), 8 - position.row)

    def __str__(self):
        return f'{self.__column}{self.__row}'