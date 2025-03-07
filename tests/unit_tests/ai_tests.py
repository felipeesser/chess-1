import tkinter as tk
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../src')

from ai import Ai
from board import Board

class AiTest(unittest.TestCase):

    def test_update(self):
        board = Board(tk.Toplevel())
        ai = Ai('black', board.squares, board, None, None)
        ai.update((1,0))
        self.assertEqual(ai.contpieces, 15)

    def test_random(self):
        board = Board(tk.Toplevel())
        ai = Ai('black', board.squares, board, None, None)
        ai.random() 
        piece = board.squares[(ai.rowpiece, ai.colpiece)]['piece'] 
        if piece is not None:
            self.assertTrue(piece.color == 'black')