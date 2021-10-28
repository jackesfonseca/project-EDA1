from chessGame.chess.ChessPosition import ChessPosition
from estruturasDeDados import ArvoreRedBlack as Arvore
from stockfish import Stockfish
import copy

class Suggestion:
    def __init__(self, chess_match):
        self.__chess_match = chess_match
        self.__moviment_tree = Arvore.RedBlackTree()
        self.__stop_thread = False

    def terminate(self):
        self.__stop_thread = True

    def calculate_suggestions(self, gui):
        for _ in range(5):
            stockfish = Stockfish("./src/cpu/stockfish_20090216_x64", 3)
            new_chess_match = copy.deepcopy(self.__chess_match)
            stockfish.set_fen_position(new_chess_match.get_fen_notation())
            new_chess_match.match_moves.limpa_pilha()
            rounds = 0 
            while rounds < 18 and (not new_chess_match.checkmate and not new_chess_match.draw):
                if self.__stop_thread:
                    return
                moviment = stockfish.get_best_move()
                new_chess_match.perform_chess_move(
                    ChessPosition(moviment[0], int(moviment[1])), 
                    ChessPosition(moviment[2], int(moviment[3]))
                )
                stockfish.set_fen_position(new_chess_match.get_fen_notation())
                rounds += 1
            self.__moviment_tree.add(self.get_eval(stockfish, new_chess_match), new_chess_match.match_moves)
        if self.__stop_thread:
                return
        moviments = self.__moviment_tree.max3() if new_chess_match.current_player == 'WHITE' else self.__moviment_tree.min3()
        gui.show_suggestions(moviments)

    def get_eval(self, stockfish, chess_match=None, fen=None) -> float:
        if fen:
            stockfish._put(f"position fen {fen}\n eval")
        elif chess_match:
            stockfish._put(f"position fen {chess_match.get_fen_notation()}\n eval")
        else:
            ValueError('Fen notation nao especificada')
            
        while True:
            text = stockfish._read_line()
            splitted_text = text.split(" ")
            if splitted_text[0] == "Total":
                if float(splitted_text[-1]) < 0.0 or float(splitted_text[-1]) >= 10.0:
                    eval = (float(splitted_text[-1]) + float(splitted_text[-2]))
                else:
                    eval = (float(splitted_text[-1]) + float(splitted_text[-3]))
                return float('%.2f'%eval)
            elif splitted_text[0] == "Final":
                move_list = []
                for n in range(len(self.__chess_match.match_moves)):
                    move_list.append(self.__chess_match.match_moves[n])
                for n in range(len(chess_match.match_moves)-1):
                    move_list.append(chess_match.match_moves[n])
                stockfish.set_position(move_list)
                return self.get_eval(stockfish, fen=stockfish.get_fen_position())

                NameError('Eval nao encontrado')