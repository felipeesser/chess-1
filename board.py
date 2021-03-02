import tkinter as tk
from PIL import Image, ImageTk
from player import Player, COLORS
from utils import convertCoord

class Board(tk.Frame):

    def __init__(self, parent, rows=8, columns=8, size=32, color1="grey", color2="blue"):
        
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.squares = {} #this dict will be populated with the board grid using tuple(row, col) as key
        global sprites
        sprites = []

        for i in range(8):
            for j in range(8):
                newSquareInfo = {'piece': None, 'coord':(i, j)} #each entry in self.squares has a piece and a coordinate
                self.squares[(i,j)] = newSquareInfo

        canvas_width = columns * size
        canvas_height = rows * size

        #print(self.squares)

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="black")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        self.canvas.bind("<Configure>", self.refresh)

    def addPiece(self, piece, row=0, column=0):
        sprites.append(tk.PhotoImage(file = piece.spriteDir))
        piece.spriteID = len(sprites)-1 #saves the sprite position in global sprites array
        self.canvas.create_image(0,0, image=sprites[piece.spriteID], tags=(piece.name, "piece_name"), anchor="c")
        self.placePiece(piece, row, column)

    def placePiece(self, piece, row, column):
        self.squares[(row, column)]['piece'] = piece
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
       # print(self.squares[(row, column)])
        self.canvas.coords(piece.name, x0, y0)

    def refresh(self, event):
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        
        for item in self.squares.items(): #iterates through the self.squares dict, attributing key to item[0] and value to item[1]
            
            if item[1]['piece']: #if statement is only true if square isn't empty
                piece = item[1]['piece']
                self.placePiece(piece, item[0][0], item[0][1])
        
        # puts piece over the square
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    
    def positionPieces(self, player):
        
        firstLine = 0
        secondLine = 1
        
        if (player.color != 0):
            firstLine = 7
            secondLine = 6
        
        self.addPiece(player.pieces[0], firstLine, 3)
        self.addPiece(player.pieces[1], firstLine, 4)
        rooks = player.pieces[2:4]
        bishops = player.pieces[4:6]
        knights = player.pieces[6:8]
        pawns = player.pieces[8:16]

        for i in range (2):
            self.addPiece(rooks[i], firstLine, i*7)
            self.addPiece(bishops[i], firstLine, 2 + 3*i)
            self.addPiece(knights[i], firstLine, 1 + 5*i)
        
        for i in range(8):
            self.addPiece(pawns[i], secondLine, i)