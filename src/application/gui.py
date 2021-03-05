import tkinter as tk
from .UI import UI
from chessGame.boardgame.Position import Position
from chessGame.chess import ChessException, ChessMatch
from chessGame.chess.ChessPosition import ChessPosition
from stockfish import Stockfish
from cpu.Suggestion import Suggestion
import threading

class GUI:
    pieces = {}
    focused = None
    source = None
    thread = None
    cpu_suggestions = None
    images = {}
    color1 = "#DDB88C"
    color2 = "#A66D4F"
    highlightcolor = "khaki"
    rows = 8
    columns = 8
    dim_square = 64

    def __init__(self, chess_match, stockfish): 
        self.__chess_match = chess_match
        self.__stockfish = stockfish
        self.parent = tk.Tk()
        self.parent.title("Tutor Chess")

        # Adding Top Menu
        self.menubar = tk.Menu(self.parent)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Novo Jogo", command=self.new_game)
        self.menubar.add_cascade(label="Menu", menu=self.filemenu)
        self.parent.config(menu=self.menubar)

        # Adding Frame
        # self.btmfrm = tk.Frame(self.parent, height=64)
        # self.info_label = tk.Label(self.btmfrm, text="  Peças brancas para começar  ", fg=self.color2)
        # self.info_label.pack(side=tk.RIGHT, padx=8, pady=5)
        # self.btmfrm.pack(fill="x", side=tk.BOTTOM)

        # Tabuleiro Principal
        chess_width = self.columns * self.dim_square
        chess_height = self.rows * self.dim_square
        self.chess = tk.Canvas(self.parent, width=chess_width, height=chess_height)
        self.chess.pack(padx=8, pady=8, side=tk.LEFT)
        self.chess.bind("<Button-1>", self.square_clicked)

        # Análise do Jogo
        scrollbar = tk.Scrollbar(self.parent)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lateral = tk.Listbox(
            self.parent, 
            width=39, 
            height=16, 
            borderwidth=2, 
            relief="solid", 
            yscrollcommand=scrollbar.set, 
            font=('Times', 14)
        )
        self.lateral.pack(padx=8, pady=8)
        
        # Sugestões de Movimentos
        self.lateral_suggestions = tk.Listbox(
            self.parent, 
            width=39, 
            height=6, 
            borderwidth=2, 
            relief="solid", 
            font=('Times', 14)
        )
        self.lateral_suggestions.pack(padx=8, pady=8)

    def main_loop(self):
        self.parent.update_idletasks()
        self.parent.update()

    def new_game(self):
        self.chessboard.show(chessboard.START_PATTERN)
        self.draw_board()
        self.draw_pieces()
        self.info_label.config(text="   Peças brancas para começar  ", fg='red')

    def square_clicked(self, event):
        col_size = row_size = self.dim_square
        if not self.source:
            try:
                self.source = ChessPosition._from_position(Position(int(event.y / row_size), int(event.x / col_size)))
                self.focused = self.__chess_match.possible_move(self.source)
                self.draw_board()
            except ChessException.ChessException as e:
                self.source = None
                print(e)
        else:
            try:
                target = ChessPosition._from_position(Position(int(event.y / row_size), int(event.x / col_size)))
                captured_piece = self.__chess_match.perform_chess_move(self.source, target)
                if self.thread.is_alive():
                    self.cpu_suggestions.terminate()
                    self.thread.join(0)
            except ChessException.ChessException as e:
                print(e)

            self.source = None
            self.focused = None
            self.__stockfish.set_fen_position(self.__chess_match.get_fen_notation())
            if self.__chess_match.current_player == self.__chess_match.bot_color:
                moviment = self.__stockfish.get_best_move()
                captured_piece = self.__chess_match.perform_chess_move(
                    ChessPosition(moviment[0], int(moviment[1])), 
                    ChessPosition(moviment[2], int(moviment[3]))
                )
                self.cpu_suggestions = Suggestion(self.__chess_match)
                self.thread = threading.Thread(target = self.cpu_suggestions.calculate_suggestions, args=(self,))
                self.thread.start()
                self.lateral_suggestions.delete(0, tk.END)
                self.lateral_suggestions.insert(1, "Calculando Sugestões...")
            self.draw_board()
            self.draw_pieces()
        self.show_match_moves()
        if self.__chess_match.checkmate or self.__chess_match.draw:
            if self.thread.is_alive():
                self.cpu_suggestions.terminate()
                self.thread.join(0)
            self.parent.quit()

    def show_suggestions(self, suggestions):
        self.lateral_suggestions.delete(0, tk.END)
        self.lateral_suggestions.insert(1, "Sugestões")
        for best in suggestions:
            string = ''
            if best.value == 1000.00 or best.value == -1000.00:
                string += 'CHECK -> '
            else:
                string += str(best.value) + ' -> '
            string += best.data.mostrar_frente()
            self.lateral_suggestions.insert(tk.END, string)

    def show_match_moves(self):
        self.lateral.delete(0, tk.END)
        for i in range(1, len(self.__chess_match.match_moves), 2):
            string = str(i) + '. ' + self.__chess_match.match_moves[i - 1] + '    ' + self.__chess_match.match_moves[i]
            self.lateral.insert(i, string)

    def draw_board(self):
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.dim_square)
                y1 = (row * self.dim_square)
                x2 = x1 + self.dim_square
                y2 = y1 + self.dim_square
                if (self.focused is not None and self.focused[row][col]):
                    self.chess.create_rectangle(x1, y1, x2, y2, fill=self.highlightcolor, tags="area")
                else:
                    self.chess.create_rectangle(x1, y1, x2, y2, fill=color, tags="area")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.pieces[name] = (self.pieces[name][0], self.pieces[name][1])
            x0 = (self.pieces[name][1] * self.dim_square) + int(self.dim_square / 2)
            y0 = ((7 - self.pieces[name][0]) * self.dim_square) + int(self.dim_square / 2)
            self.chess.coords(name, x0, y0)
        self.chess.tag_raise("Ocupado")
        self.chess.tag_lower("area")

    def draw_pieces(self):
        self.chess.delete("Ocupado")
        pieces = self.__chess_match.pieces()
        for i in range(len(pieces)):
            for j in range(len(pieces)):
                piece = pieces[i][j]
                if piece:
                    filename = "./src/pieces_image/%s%s.png" % (str(piece).lower(), piece.color.lower())
                    piecename = "%s%s%s" % (str(piece), i, j)
                    if filename not in self.images:
                        self.images[filename] = tk.PhotoImage(file=filename)
                    self.chess.create_image(0, 0, image=self.images[filename], tags=(piecename, "Ocupado"), anchor="c")
                    x0 = (j * self.dim_square) + int(self.dim_square / 2)
                    y0 = (i * self.dim_square) + int(self.dim_square / 2)
                    self.chess.coords(piecename, x0, y0)