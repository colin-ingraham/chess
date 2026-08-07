from board import Board
from piece import *
import time

class Game:
    def __init__(self):
        self.game_over = False
        self.board = Board()
        self.pieces = []
        self.setup_pieces()
        self.board.print_board()
        self.game_loop()


    def game_loop(self):
        while not self.game_over:
            move = input("\nNext Move (White) :: ")
            self.move_piece(move)
            time.sleep(1)
            self.board.print_board()

    def move_piece(self, move):
        if self.validate_move(move):
            if len(move) == 2: # Simple pawn movement
                file = move[0]
                rank = move[1]

                for piece in self.pieces:
                    if piece.color == "White" and isinstance(piece, Pawn) and piece.file == file:
                        old_rank = piece.rank
                        x = ord(piece.file) - 97
                        y = (old_rank - 8) * - 1
                        self.board.board[y][x].remove_piece()
                        break
    
                # Add piece to new tile
                x = ord(file) - 97
                y = (int(rank) - 8) * -1
                new_tile = self.board.board[y][x]
                new_tile.add_piece(piece)

            #TODO Need to update piece rank/file




    def validate_move(self, move):
        return True

    def setup_pieces(self):

        # Setup Opponent Pawns:
        for i in range(8):
            self.pieces.append(self.board.board[1][i].add_piece(Pawn("Black", chr(ord('a') + i), 7)))
        # Setup Player Pawns:
        for i in range(8):
            self.pieces.append(self.board.board[6][i].add_piece(Pawn("White", chr(ord('a') + i), 2)))
        # Setup Opponent Back Row:
        self.pieces.append(self.board.board[0][0].add_piece(Rook("Black", 'a', 8)))
        self.pieces.append(self.board.board[0][7].add_piece(Rook("Black", 'h', 8)))
        self.pieces.append(self.board.board[0][1].add_piece(Knight("Black", 'b', 8)))
        self.pieces.append(self.board.board[0][6].add_piece(Knight("Black", 'g', 8)))
        self.pieces.append(self.board.board[0][2].add_piece(Bishop("Black", 'c', 8)))
        self.pieces.append(self.board.board[0][5].add_piece(Bishop("Black", 'f', 8)))
        self.pieces.append(self.board.board[0][3].add_piece(Queen("Black", 'd', 8)))
        self.pieces.append(self.board.board[0][4].add_piece(King("Black", 'e', 8)))
        # Setup Player Back Row:
        self.pieces.append(self.board.board[7][0].add_piece(Rook("White", 'a', 1)))
        self.pieces.append(self.board.board[7][7].add_piece(Rook("White", 'h', 1)))
        self.pieces.append(self.board.board[7][1].add_piece(Knight("White", 'b', 1)))
        self.pieces.append(self.board.board[7][6].add_piece(Knight("White", 'g', 1)))
        self.pieces.append(self.board.board[7][2].add_piece(Bishop("White", 'c', 1)))
        self.pieces.append(self.board.board[7][5].add_piece(Bishop("White", 'f', 1)))
        self.pieces.append(self.board.board[7][3].add_piece(Queen("White", 'd', 1)))
        self.pieces.append(self.board.board[7][4].add_piece(King("White", 'e', 1)))

    