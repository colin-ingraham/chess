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
        self.graveyard = []
        self.setup_pieces()
        self.board.print_board(self.graveyard, self.player1, self.player2)
        self.game_loop()



    def game_loop(self):
        while not self.game_over:
            move = input(f"\nNext Move ({self.current_player.color}) :: ")
            if self.parse_move(move):
                time.sleep(0.25)
                self.board.print_board(self.graveyard, self.player1, self.player2)
                self.current_player = self.player1 if self.player1 != self.current_player else self.player2

    def parse_move(self, move):
        target_tile = self.board.get_tile(move[0], int(move[1]))
        standing_tile = None
        if len(move) == 2: # Simple pawn movement
            for piece in self.pieces:
                if isinstance(piece, Pawn) and target_tile in piece.possible_moves(self.board, self.current_player) and self.current_player.color == piece.color:
                    standing_tile = piece.tile

        if standing_tile:
            self.move_piece(standing_tile, target_tile)
            return True
        else:
            print("Move not available. Please try again.")
            return False

    def move_piece(self, standing_tile, target_tile):
        #print(f"Moving from {standing_tile.file}{standing_tile.rank} to {target_tile.file}{target_tile.rank}")
        piece = standing_tile.piece
        if target_tile in piece.possible_moves(self.board, self.current_player):
            standing_tile.remove_piece()
            if target_tile.piece != None: # Piece is killed
                self.destroy_piece(target_tile.piece)
            target_tile.add_piece(piece)
            piece.update_position(target_tile)

    def destroy_piece(self, piece):
        self.pieces.remove(piece)
        piece.tile = None
        self.graveyard.append(piece)

    def setup_pieces(self):
        
        # Setup Opponent Pawns:
        for i in range(8):
            self.pieces.append(self.board.board[1][i].add_piece(Pawn("Black", self.board.get_tile(chr(ord('a') + i), 7))))
        # Setup Player Pawns:
        for i in range(8):
            self.pieces.append(self.board.board[6][i].add_piece(Pawn("White", self.board.get_tile(chr(ord('a') + i), 2))))
        # Setup Opponent Back Row:
        self.pieces.append(self.board.board[0][0].add_piece(Rook("Black", self.board.get_tile('a', 8))))
        self.pieces.append(self.board.board[0][7].add_piece(Rook("Black", self.board.get_tile('h', 8))))
        self.pieces.append(self.board.board[0][1].add_piece(Knight("Black", self.board.get_tile('b', 8))))
        self.pieces.append(self.board.board[0][6].add_piece(Knight("Black", self.board.get_tile('g', 8))))
        self.pieces.append(self.board.board[0][2].add_piece(Bishop("Black", self.board.get_tile('c', 8))))
        self.pieces.append(self.board.board[0][5].add_piece(Bishop("Black", self.board.get_tile('f', 8))))
        self.pieces.append(self.board.board[0][3].add_piece(Queen("Black", self.board.get_tile('d', 8))))
        self.pieces.append(self.board.board[0][4].add_piece(King("Black", self.board.get_tile('e', 8))))
        # Setup Player Back Row:
        self.pieces.append(self.board.board[7][0].add_piece(Rook("White", self.board.get_tile('a', 1))))
        self.pieces.append(self.board.board[7][7].add_piece(Rook("White", self.board.get_tile('h', 1))))
        self.pieces.append(self.board.board[7][1].add_piece(Knight("White", self.board.get_tile('b', 1))))
        self.pieces.append(self.board.board[7][6].add_piece(Knight("White", self.board.get_tile('g', 1))))
        self.pieces.append(self.board.board[7][2].add_piece(Bishop("White", self.board.get_tile('c', 1))))
        self.pieces.append(self.board.board[7][5].add_piece(Bishop("White", self.board.get_tile('f', 1))))
        self.pieces.append(self.board.board[7][3].add_piece(Queen("White", self.board.get_tile('d', 1))))
        self.pieces.append(self.board.board[7][4].add_piece(King("White", self.board.get_tile('e', 1))))

    