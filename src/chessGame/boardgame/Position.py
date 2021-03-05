# Classe responspável por armazenar 1 espaço no tabuleiro
class Position:

    def __init__(self, row, column):
        self.__row = row
        self.__column = column

    # Getter do atributo row
    @property
    def row(self):
        return self.__row

    # Getter do atributo column
    @property
    def column(self):
        return self.__column
    
    # Setter do atributo row
    @row.setter
    def row(self, row):
        self.__row = row

    # Setter do atributo column
    @column.setter
    def column(self, column):
        self.__column = column

    # Função que seta ambos row e column
    def values(self, row, column):
        self.__row = row
        self.__column = column

    # Sobrecarga toString
    def __str__(self):
        return f'{self.__row}, {self.__column}'