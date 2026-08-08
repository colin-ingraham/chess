from board import Board
from piece import *
import time

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.game_over = False
        self.board = Board()
        self.pieces = []
        self.setup_pieces()
        self.board.print_board()
        self.game_loop()


    def game_loop(self):
        while not self.game_over:
            move = input(f"\nNext Move ({self.current_player.color}) :: ")
            self.parse_move(move)
            time.sleep(0.25)
            self.board.print_board()
            self.current_player = self.player1 if self.player1 != self.current_player else self.player2

    def parse_move(self, move):
        if len(move) == 2: # Simple pawn movement
            target_tile = self.board.get_tile(move[0], int(move[1]))
        
            for piece in self.pieces:
                if piece.color == self.current_player.color and isinstance(piece, Pawn) and piece.file == target_tile.file:
                    standing_tile = self.board.get_tile(target_tile.file, piece.rank)
                    break

        self.move_piece(standing_tile, target_tile)

    def move_piece(self, standing_tile, target_tile):
        #print(f"Moving from {standing_tile.file}{standing_tile.rank} to {target_tile.file}{target_tile.rank}")
        piece = standing_tile.piece
        standing_tile.remove_piece()
        target_tile.add_piece(piece)
        piece.update_position(target_tile.file, target_tile.rank)


        




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

    