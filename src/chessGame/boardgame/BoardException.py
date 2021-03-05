# CLasse de exceção que são apenas acessadas pelo programador
class BoardException(Exception):

    def __init__(self, message):
        super().__init__(message)