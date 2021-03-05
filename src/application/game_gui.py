import tkinter as tk
from chessGame.boardgame.Position import Position
from chessGame.chess import ChessException, ChessMatch
from chessGame.chess.ChessPosition import ChessPosition
from stockfish import Stockfish
from cpu.Suggestion import Suggestion
from PIL import Image, ImageTk
import threading

class Game:
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
    index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def __init__(self, chess_match, stockfish): 
        self.__chess_match = chess_match
        self.__stockfish = stockfish
        self.parent = tk.Tk()
        self.parent.title("Tutor Chess")

        # Container Jogo
        self.game_container = tk.Frame(self.parent)
        self.game_container.pack(padx=8, side=tk.LEFT)

        # Peças Brancas Capturadas
        self.count_white = 0
        captured_width = 16 * self.dim_square / 2
        self.captured_white = tk.Canvas(
            self.game_container, 
            width=captured_width, 
            height=self.dim_square/2, 
            highlightbackground="black", 
            highlightthickness=2)
        self.captured_white.pack(pady=8, side=tk.TOP)

        # Container tabuleiro
        self.board_container = tk.Frame(self.game_container)
        self.board_container.pack()
        chess_width = self.columns * self.dim_square
        chess_height = self.rows * self.dim_square

        # Index letras inferior
        label_widht = 15
        label_height = 25
        self.index_inferior = tk.Canvas(self.board_container, width=chess_width+label_widht, height=label_height)
        self.index_inferior.pack(side=tk.BOTTOM)

        # Index numero lateral
        self.index_lateral = tk.Canvas(self.board_container, width=label_widht, height=chess_height)
        self.index_lateral.pack(side=tk.LEFT)

        # Labels de index
        for n in range(8):
            c0 = n*self.dim_square + self.dim_square/2
            self.index_lateral.create_text(int(label_widht/2)+1, c0, font="Times 20 italic bold", text=str(8-n))
            self.index_inferior.create_text(c0+label_widht, int(label_height/2)+1, font="Times 20 italic bold", text=self.index[n])

        # Tabuleiro Principal
        self.chess = tk.Canvas(self.board_container, width=chess_width, height=chess_height)
        self.chess.pack()
        self.chess.bind("<Button-1>", self.square_clicked)

        # Peças Pretas Capturadas
        self.count_black = 0
        self.captured_black = tk.Canvas(
            self.game_container, 
            width=captured_width, 
            height=self.dim_square/2, 
            highlightbackground="black", 
            highlightthickness=2)
        self.captured_black.pack(pady=8, side=tk.BOTTOM)

        # Container Auxiliar
        self.aux_container = tk.Frame(self.parent)
        self.aux_container.pack(padx=8, side=tk.RIGHT)

        # Container da Análize do jogo
        self.analyze_container = tk.Frame(self.aux_container)
        self.analyze_container.pack(pady=8, side=tk.TOP)

        # Análise do Jogo
        scrollbar_analize = tk.Scrollbar(self.analyze_container)
        scrollbar_analize.pack(side=tk.RIGHT, fill=tk.Y)
        self.lateral_analize = tk.Listbox(
            self.analyze_container, 
            width=39, 
            height=20, 
            borderwidth=2, 
            relief="solid", 
            yscrollcommand=scrollbar_analize.set, 
            font=('Times', 14)
        )
        self.lateral_analize.pack()
        scrollbar_analize.config(command = self.lateral_analize.yview)
        
        # Container de Sugestões
        self.suggest_container = tk.Frame(self.aux_container)
        self.suggest_container.pack(pady=8 ,side=tk.TOP)

        # Sugestões de Movimentos
        scrollbar_suggest = tk.Scrollbar(self.suggest_container, orient='horizontal')
        scrollbar_suggest.pack(side=tk.BOTTOM, fill=tk.X)
        self.lateral_suggestions = tk.Listbox(
            self.suggest_container, 
            width=41, 
            height=4, 
            borderwidth=2, 
            relief="solid", 
            xscrollcommand=scrollbar_suggest.set, 
            font=('Times', 14)
        )
        self.lateral_suggestions.pack()
        scrollbar_suggest.config(command = self.lateral_suggestions.xview)

        # Label do jogador atual
        self.btm_frame = tk.Frame(self.aux_container)
        self.current_player_label = tk.Label(self.btm_frame, text="Peças brancas para começar", fg=self.color2, anchor="center")
        self.current_player_label.pack(padx=8, pady=5)
        self.btm_frame.pack(fill="x", side=tk.BOTTOM)

        # Conficurações da Janela
        self.parent.update_idletasks()
        positionRight = int((self.parent.winfo_screenwidth() - self.parent.winfo_reqwidth())/2)
        positionDown = int((self.parent.winfo_screenheight() - self.parent.winfo_reqheight() - 25)/2)
        self.parent.geometry("+{}+{}".format(positionRight, positionDown))
        self.parent.resizable(0, 0)
        self.parent.iconphoto(False, tk.PhotoImage(file='src/application/images/icon.png'))
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if self.thread.is_alive():
            self.cpu_suggestions.terminate()
            self.thread.join(0)
        if self.__chess_match.checkmate or self.__chess_match.draw:
            self.parent.quit()
            self._end_game()
        else:
            self.parent.destroy()

    def square_clicked(self, event):
        col_size = row_size = self.dim_square
        if not self.source:
            try:
                self.source = ChessPosition._from_position(Position(int(event.y / row_size), int(event.x / col_size)))
                self.focused = self.__chess_match.possible_move(self.source)
                self.draw_board()
            except ChessException.ChessException as e:
                self.current_player_label.configure(text=e)
                self.source = None
        else:
            try:
                target = ChessPosition._from_position(Position(int(event.y / row_size), int(event.x / col_size)))
                captured_piece = self.__chess_match.perform_chess_move(self.source, target)
                self.draw_captured_pieces(captured_piece)
                self.current_player_label.configure(text='Vez das ' + ('Brancas' if self.__chess_match.current_player == 'WHITE' else 'Negras'))
                if self.thread != None and self.thread.is_alive():
                    self.cpu_suggestions.terminate()
                    self.thread.join(0)
            except ChessException.ChessException as e:
                self.current_player_label.configure(text=e)

            self.source = None
            self.focused = None
            self.__stockfish.set_fen_position(self.__chess_match.get_fen_notation())
            if self.__chess_match.current_player == self.__chess_match.bot_color:
                moviment = self.__stockfish.get_best_move()
                captured_piece = self.__chess_match.perform_chess_move(
                    ChessPosition(moviment[0], int(moviment[1])), 
                    ChessPosition(moviment[2], int(moviment[3]))
                )
                self.draw_captured_pieces(captured_piece)
                self.current_player_label.configure(text='Vez das ' + ('Brancas' if self.__chess_match.current_player == 'WHITE' else 'Negras'))

            # Evita que entre em processo de threading
            if not self.__chess_match.checkmate and not self.__chess_match.draw:
                self.cpu_suggestions = Suggestion(self.__chess_match)
                self.thread = threading.Thread(target = self.cpu_suggestions.calculate_suggestions, args=(self,))
                self.thread.start()
                self.lateral_suggestions.delete(0, tk.END)
                self.lateral_suggestions.insert(1, "Calculando Sugestões...")
       
            self.draw_board()
            self.draw_pieces()
        self.show_match_moves()
        if self.__chess_match.checkmate or self.__chess_match.draw:
            self.on_closing()

    def show_suggestions(self, suggestions):
        self.lateral_suggestions.delete(0, tk.END)
        self.lateral_suggestions.insert(1, "Sugestões")
        n = 1
        for best in suggestions:
            if best.value == None:
                continue
            string = ' ' + str(n) + 'º:  '
            string += str(best.value) + ' -> '
            string += best.data.mostrar_frente()
            self.lateral_suggestions.insert(tk.END, string)
            n += 1

    def show_match_moves(self):
        self.lateral_analize.delete(0, tk.END)
        if self.__chess_match.bot_color:
            for i in range(1, len(self.__chess_match.match_moves), 2):
                string = str(i // 2 + 1) + '. ' + self.__chess_match.match_moves[i - 1] + '    ' + self.__chess_match.match_moves[i]
                self.lateral_analize.insert(tk.END, string)
        else:
            for i in range(len(self.__chess_match.match_moves)):
                string = str(i+1) + '. ' + self.__chess_match.match_moves[i]
                self.lateral_analize.insert(tk.END, string)

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
                    filename = "src/application/images/%s%s.png" % (str(piece).lower(), piece.color.lower())
                    piecename = "%s%s%s" % (str(piece), i, j)
                    if filename not in self.images:
                        self.images[filename] = ImageTk.PhotoImage(Image.open(filename))
                    self.chess.create_image(0, 0, image=self.images[filename], tags=(piecename, "Ocupado"), anchor="c")
                    x0 = (j * self.dim_square) + int(self.dim_square / 2)
                    y0 = (i * self.dim_square) + int(self.dim_square / 2)
                    self.chess.coords(piecename, x0, y0)

    def draw_captured_pieces(self, captured_piece=None):
        if captured_piece:
            filename = "./src/application/images/c_%s%s.png" % (str(captured_piece).lower(), captured_piece.color.lower())
            if filename not in self.images:
                self.images[filename] = tk.PhotoImage(file=filename)
            if captured_piece.color == "WHITE":
                x0 = ( self.count_white * self.dim_square/2) + int(self.dim_square / 4)
                self.captured_white.create_image(x0, int(self.dim_square / 4), image=self.images[filename], anchor="c")
                self.count_white += 1
            else:
                x0 = ( self.count_black * self.dim_square/2) + int(self.dim_square / 4)
                self.captured_black.create_image(x0, int(self.dim_square / 4), image=self.images[filename], anchor="c")
                self.count_black += 1

    def _end_game(self):
        def end_button():
            self.win.destroy()

        self.win = tk.Toplevel(bg="#FFFFFF")
        self.win.wm_title("Xeque-mate")
        positionRight = int(self.win.winfo_screenwidth()/2 - 266/2)
        positionDown = int(self.win.winfo_screenheight()/2 - 100/2)
        self.win.geometry("+{}+{}".format(positionRight, positionDown))
        self.win.grab_set()
        text = tk.Text(self.win, width=45, height=2, relief=tk.FLAT)
        text.tag_config("w", font="Times 20 italic bold", justify=tk.CENTER)
        if self.__chess_match.current_player == 'WHITE':
            winner = "AS BRANCAS GANHARAM"
        else:
            winner = "AS PRETAS GANHARAM"
        text.insert(tk.INSERT, winner, "w")
        text.configure(state=tk.DISABLED)
        text.pack(padx=8, pady=8, side=tk.TOP)

        # Botão final
        ok = tk.Button(
            self.win,
            text="OK",
            height=2,
            width=15,
            command = end_button
        )
        ok.pack(padx=8, pady=8)
        