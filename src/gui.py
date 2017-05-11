import tkinter as tk

import chess
from PIL import ImageTk


class Gui(tk.Frame):
    pieces = {}
    icons = {}

    white = '#F0D9B5'
    black = '#B58863'

    rows = 8
    columns = 8

    square_size = 64

    def __init__(self, parent, board):
        self.board = board
        self.parent = parent

        # frame
        tk.Frame.__init__(self, parent)

        # canvas
        canvas_width = self.columns * self.square_size
        canvas_height = self.rows * self.square_size

        self.canvas = tk.Canvas(
            self, width=canvas_width, height=canvas_height, background='grey')
        self.canvas.pack(side='top', fill='both', anchor='c', expand=True)

        # drawing
        self.refresh()
        self.draw_pieces()

        # status bar
        self.statusbar = tk.Frame(self, height=64)

        entry = tk.Entry(self.statusbar, width=10)
        entry.pack(side=tk.BOTTOM, padx=10, pady=10)

        label = tk.Label(self.statusbar, text='Your move:')
        label.pack(side=tk.BOTTOM, padx=10, pady=10)

        def ok_button():
            print('OK')

        tk.Button(self.parent, text='OK', command=ok_button).pack(side=tk.BOTTOM)

        self.statusbar.pack(expand=False, fill='x', side='bottom')

    def refresh(self, event={}):
        if event:
            x_size = int((event.width - 1) / self.columns)
            y_size = int((event.height - 1) / self.rows)
            self.square_size = min(x_size, y_size)

        self.canvas.delete('square')
        color = self.black

        for row in range(self.rows):
            color = self.white if color == self.black else self.black

            for col in range(self.columns):
                start_column = (col * self.square_size)
                start_row = ((7 - row) * self.square_size)
                end_column = start_column + self.square_size
                end_row = start_row + self.square_size

                self.canvas.create_rectangle(
                    start_column,
                    start_row,
                    end_column,
                    end_row,
                    outline='black',
                    fill=color,
                    tags='square')
                color = self.white if color == self.black else self.black

        for name in self.pieces:
            self.place_piece(name, self.pieces[name][0], self.pieces[name][1])

        self.canvas.tag_raise('piece')
        self.canvas.tag_lower('square')

    def draw_pieces(self):
        self.canvas.delete('piece')

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)

            if piece is not None:
                image_name = 'img/%s.png' % (piece.symbol())
                piece_name = '%s%s' % (piece.symbol(), square)

                if image_name not in self.icons:
                    self.icons[image_name] = ImageTk.PhotoImage(
                        file=image_name, width=32, height=32)

                self.add_piece(piece_name, self.icons[image_name], square // 8,
                               square % 8)
                self.place_piece(piece_name, square // 8, square % 8)

    def add_piece(self, name, image, row=0, column=0):
        self.canvas.create_image(
            0, 0, image=image, tags=(name, 'piece'), anchor='c')
        self.place_piece(name, row, column)

    def place_piece(self, name, row, column):
        self.pieces[name] = (row, column)

        true_row = (column * self.square_size) + int(self.square_size / 2)
        true_column = ((7 - row) * self.square_size) + int(self.square_size / 2)
        self.canvas.coords(name, true_row, true_column)


def display(board):
    root = tk.Tk()
    root.title('Yachess')

    gui = Gui(root, board)
    gui.pack(side='top', fill='both', expand='true', padx=4, pady=4)

    root.mainloop()


BOARD = chess.Board()
display(BOARD)
