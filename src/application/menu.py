import tkinter as tk
from tkinter import messagebox
from chessGame.chess.ChessPosition import ChessPosition
from chessGame.chess import ChessMatch
from application.game_gui import Game
from cpu.Suggestion import Suggestion
from stockfish import Stockfish
from PIL import Image, ImageTk
import threading

class Menu:
    bot_color = None

    def __init__(self): 
        self.parent = tk.Tk()
        self.parent.title("Tutor Chess")
        self.parent.iconphoto(False, tk.PhotoImage(file='src/application/images/icon.png'))
        self.tabuleiro = None
        self.stockfish = None
        self.game_gui = None
        
        # Imagem de fundo
        width_size = 8 * 64
        height_size = 8 * 64
        self.principal = tk.Canvas(self.parent, width=width_size, height=height_size)
        background_image = ImageTk.PhotoImage(Image.open("src/application/images/background_image.jpg").resize((725, 515)))
        label = tk.Label(self.parent, image=background_image)
        label.image = background_image
        label.place(x=0, y=0, relwidth=1, relheight=1)
        self.principal.pack()

        # Imagem da logo
        img = Image.open("src/application/images/logoProjeto.png").resize((400, 100)).convert("RGBA")
        logo_image = ImageTk.PhotoImage(img)
        label_logo = tk.Label(self.parent, image=logo_image)
        label_logo.image = logo_image
        label_logo.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        # Botões
        # PLayer vs Player
        self.novo_jogo_player = tk.Button(
            self.parent,
            text="Player vs Player",
            height=2,
            width=50,
            command=self.new_game
        )
        self.novo_jogo_player.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # PLayer vs Bot
        self.novo_jogo_bot = tk.Button(
            self.parent, 
            text="Player vs Bot",
            height=2,
            width=50,
            command=self.set_color
        )
        self.novo_jogo_bot.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Tutorial
        self.tutorial = tk.Button(
            self.parent, 
            text="Tutorial",
            height=2,
            width=50,
            command=self.tutorial_text
        )
        self.tutorial.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        # Sair
        self.finalizar = tk.Button(
            self.parent, 
            text="Finalizar",
            height=2,
            width=50,
            command=exit
        )
        self.finalizar.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        # Posicionamento da Tela Principal
        self.parent.update_idletasks()
        positionRight = int((self.parent.winfo_screenwidth() - self.parent.winfo_reqwidth())/2)
        positionDown = int((self.parent.winfo_screenheight() - self.parent.winfo_reqheight())/2)
        self.parent.geometry("+{}+{}".format(positionRight, positionDown))
        self.parent.resizable(0, 0)

    # Descrever um tutorial sobre a aplicação
    def tutorial_text(self):
        tk.messagebox.showinfo("Tutorial", "Tutorial sobre o Jogo")

    def __initial_game(self):
        # self.parent.withdraw()
        self.parent.destroy()
        self.tabuleiro = ChessMatch.ChessMatch(self.bot_color)
        self.stockfish = Stockfish("./src/cpu/stockfish_20090216_x64")
        self.stockfish.set_skill_level(0)
        self.game_gui = Game(self.tabuleiro, self.stockfish)

    def new_game(self):
        self.__initial_game()
        if self.tabuleiro.current_player == self.bot_color:
            moviment = self.stockfish.get_best_move()
            self.tabuleiro.perform_chess_move(
                ChessPosition(moviment[0], int(moviment[1])), 
                ChessPosition(moviment[2], int(moviment[3]))
            )

        self.stockfish.set_fen_position(self.tabuleiro.get_fen_notation())
        self.game_gui.cpu_suggestions = Suggestion(self.tabuleiro)
        self.game_gui.thread = threading.Thread(target = self.game_gui.cpu_suggestions.calculate_suggestions, args=(self.game_gui,))
        self.game_gui.thread.start()
        self.game_gui.lateral_suggestions.insert(1, "Calculando Sugestões...")

        self.game_gui.draw_board()
        self.game_gui.draw_pieces()
        self.game_gui.parent.mainloop()
        # self.parent.deiconify()

    def set_color(self):
        self.win = tk.Toplevel(bg="#FFFFFF")
        self.win.wm_title("Escolha a Cor")
        positionRight = int(self.win.winfo_screenwidth()/2 - 266/2)
        positionDown = int(self.win.winfo_screenheight()/2 - 100/2)
        self.win.geometry("+{}+{}".format(positionRight, positionDown))
        self.win.grab_set()
        text = tk.Text(self.win, width=30, height=1, relief=tk.FLAT)
        text.insert(tk.INSERT, "Escolha a cor do seu jogador.")
        text.configure(state=tk.DISABLED)
        text.pack(padx=8, pady=8, side=tk.TOP)

        # Cor Branca
        white_color = tk.Button(
            self.win,
            text="Brancas",
            height=2,
            width=15,
            command = self.__set_bot_black
        )
        white_color.pack(padx=8, pady=8, side=tk.LEFT)

        # Cor Negra
        black_color = tk.Button(
            self.win, 
            text="Negras",
            height=2,
            width=15,
            command = self.__set_bot_white
        )
        black_color.pack(padx=8, pady=8, side=tk.RIGHT)

    def __set_bot_black(self):
        self.bot_color = 'BLACK'
        self.win.destroy()
        self.new_game()
    
    def __set_bot_white(self):
        self.bot_color = 'WHITE'
        self.win.destroy()
        self.new_game()