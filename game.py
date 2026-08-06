from board import Board
from piece import *

class Game:
    def __init__(self):
        self.board = Board()
        self.setup_pieces()
        self.board.print_board()


    def setup_pieces(self):

        # Setup Opponent Pawns:
        for i in range(8):
            self.board.board[1][i].add_piece(Pawn("Black"))
        # Setup Player Pawns:
        for i in range(8):
            self.board.board[6][i].add_piece(Pawn("White"))
        