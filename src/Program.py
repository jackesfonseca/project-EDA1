from chessGame.chess import ChessException, ChessMatch
from chessGame.chess.ChessPosition import ChessPosition
# from application.UI import UI
from application.gui import GUI
from cpu.Suggestion import Suggestion
from stockfish import Stockfish
import threading

def main():
    if tabuleiro.current_player == tabuleiro.bot_color:
        moviment = stockfish.get_best_move()
        captured_piece = tabuleiro.perform_chess_move(
            ChessPosition(moviment[0], int(moviment[1])), 
            ChessPosition(moviment[2], int(moviment[3]))
        )
        stockfish.set_fen_position(tabuleiro.get_fen_notation())

    gui.cpu_suggestions = Suggestion(tabuleiro)
    gui.thread = threading.Thread(target = gui.cpu_suggestions.calculate_suggestions, args=(gui,))
    gui.thread.start()
    gui.draw_board()
    gui.draw_pieces()
    gui.parent.mainloop()
    UI.print_match(tabuleiro, stockfish)

if __name__ == "__main__":
    print('Escolha a Cor:')
    print('[1] BRANCAS')
    print('[2] NEGRAS')
    player_color = int(input())
    tabuleiro = ChessMatch.ChessMatch('BLACK' if player_color == 1 else 'WHITE')
    stockfish = Stockfish("./src/cpu/stockfish_20090216_x64")
    stockfish.set_skill_level(0)
    gui = GUI(tabuleiro, stockfish)
    main()