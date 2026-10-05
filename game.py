from board import Board
from piece import *
from move import *
import time

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.game_over = False
        self.board = Board()
        self.pieces = []
        self.whites = []
        self.blacks = []
        self.graveyard = []
        self.setup_pieces()
        self.board.print_board(self.graveyard, self.player1, self.player2)
        self.game_loop()



    def game_loop(self):
        while not self.game_over:
            check_symbol = ""
            in_check = self.is_in_check(self.current_player.color)
            legal_moves = self.generate_legal_moves(self.current_player.color)
            if in_check and len(legal_moves) > 0: # Player is in check
                check_symbol = "!X!"
            elif in_check and len(legal_moves) == 0: # Player is in checkmate
                self.game_over = True
                print(f"Checkmate! {self.enemy_color(self.current_player.color)} wins!")
                break
            elif not in_check and len(legal_moves) == 0: # Player is in stalemate
                self.game_over = True
                print("Stalemate draw! Game over.")
                break
            
            notation = input(f"\nNext Move ({self.current_player.color}) {check_symbol} :: ")
            if self.parse_move(notation):
                time.sleep(0.25)
                self.board.print_board(self.graveyard, self.player1, self.player2)
                self.current_player = self.player1 if self.player1 != self.current_player else self.player2
            else:
                print("Move not available. Please try again.")

    PIECE_LETTERS = {"N": "Knight", "R": "Rook", "B": "Bishop",
                    "Q": "Queen", "K": "King"}

    def tokenize(self, notation):
        piece = None
        tile = None
        if notation[0] in self.PIECE_LETTERS.keys(): # High piece movement
            piece = self.PIECE_LETTERS[notation[0]]
            if notation[1] == "x":
                tile = notation[2] + notation[3]
                target = self.board.get_tile(tile[0], int(tile[1:]))
                if target.piece == None:
                    tile = None
            else:
                tile = notation[1] + notation[2]

        elif notation[0].lower() == "o" or notation[0] == "0": # Castle
            print("Castle not implemented.")
        else: # Pawn movement
            piece = "Pawn"
            if notation[0] == "x":
                tile = notation[1] + notation[2]
                target = self.board.get_tile(tile[0], int(tile[1:]))
                if target.piece == None:
                    tile = None
            else:
                tile = notation[0] + notation[1]

        return (piece, tile)
        
    def parse_move(self, notation, legal_moves=None):
        name, square = self.tokenize(notation) # ("Pawn", "e4") / ("Knight", "f3")
        if name is None or square is None:
            return False
        target = self.board.get_tile(square[0], int(square[1:]))
        if target is None:
            return False
        if legal_moves is None:
            legal_moves = self.generate_legal_moves(self.current_player.color)
        matches = [m for m in legal_moves if m.piece.name == name and m.destination is target]
        if len(matches) != 1:
            return False # 0 = illegal, >1 = ambigious notation
        self.apply_move(matches[0])
        return True
       
    def move_piece(self, standing_tile, target_tile): # A deprecated function for moving a piece
        #print(f"Moving from {standing_tile.file}{standing_tile.rank} to {target_tile.file}{target_tile.rank}")
        if target_tile.piece:
            move = Move(standing_tile.piece, standing_tile, target_tile, "CAPTURE", target_tile.piece, self.pieces.index(target_tile.piece), target_tile)
        else:
            move = Move(standing_tile.piece, standing_tile, target_tile, "QUIET")

        move.origin.remove_piece()
        if move.kind == "CAPTURE":
            self.destroy_piece(move.destination.piece)
        move.destination.add_piece(move.piece)
        move.piece.update_position(move.destination)
        return move

    def apply_move(self, move): # The preferred method for moving a piece.
        target = move.destination.piece
        if target is not None:
            move.captured = target
            move.captured_index = self.pieces.index(target)
            move.captured_tile = move.destination
            move.kind = CAPTURE
        move.origin.remove_piece()
        if move.captured is not None:
            self.destroy_piece(move.captured)
        move.destination.add_piece(move.piece)
        move.piece.update_position(move.destination)
        return move
    
    def undo_move(self, move):
        """ This function reverts the movement previously made with the move_piece function"""

        move.origin.add_piece(move.piece)
        move.piece.tile = move.origin
        move.piece.past_tiles.pop()
        move.destination.add_piece(move.captured)
        if move.captured != None: 
            move.captured.tile = move.destination
            self.pieces.insert(move.captured_index, move.captured)
            self.graveyard.remove(move.captured)

    
    def destroy_piece(self, piece):
        self.pieces.remove(piece)
        piece.tile = None
        self.graveyard.append(piece)

    # --- Checkmate Helper Functions --- #

    def is_attacked(self, tile, by_color):
        """ This function determines if a given tile is being attacked by a specific color."""
        for piece in self.pieces:
            if piece.color == by_color:
                if any(m.destination is tile for m in piece.possible_moves(self.board)):
                    return True
        return False

    def is_in_check(self, color):
        """ This function determines if a given color is in check."""
        king = None
        for piece in self.pieces:
            if piece.name == "King" and piece.color == color:
                king = piece
        return self.is_attacked(king.tile, self.enemy_color(color))

    def generate_legal_moves(self, color):
        """ This function returns the moves that doesn't leave color king in check. Determines checkmate"""
        legal_moves = []
        for piece in list(self.pieces):
            if piece.color != color:
                continue
            for candidate in piece.possible_moves(self.board):
                self.apply_move(candidate)
                king_is_safe = not self.is_in_check(color)
                self.undo_move(candidate)
                if king_is_safe:
                    legal_moves.append(candidate)
        return legal_moves


    # --- Board Setup --- #
                                
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

    def enemy_color(self, color): 
        if color == "White":
            return "Black"
        else:
            return "White"