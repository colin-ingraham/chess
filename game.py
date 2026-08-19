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
            legal_moves = self.has_any_legal_move(self.current_player.color)
            if in_check and legal_moves: # Player is in check
                check_symbol = "!X!"
            elif in_check and not legal_moves: # Player is in checkmate
                self.game_over = True
                print(f"Checkmate! {self.enemy_color(self.current_player.color)} wins!")
                break
            elif not in_check and not legal_moves: # Player is in stalemate
                self.game_over = True
                print("Stalemate draw! Game over.")
                break
            
            move = input(f"\nNext Move ({self.current_player.color}) {check_symbol} :: ")
            if self.parse_move(move):
                time.sleep(0.25)
                self.board.print_board(self.graveyard, self.player1, self.player2)
                self.current_player = self.player1 if self.player1 != self.current_player else self.player2
            else:
                print("Move not available. Please try again.")


    def parse_move(self, move):
        standing_tile = None
        if len(move) == 2: # Simple pawn movement
            target_tile = self.board.get_tile(move[0], int(move[1]))
            for piece in self.pieces:
                if isinstance(piece, Pawn) and target_tile in piece.possible_moves(self.board) and self.current_player.color == piece.color:
                    standing_tile = piece.tile
        elif len(move) == 3:
            target_tile = self.board.get_tile(move[1], int(move[2]))
            if move[0] == 'N':
                for piece in self.pieces:
                    if isinstance(piece, Knight) and target_tile in piece.possible_moves(self.board) and self.current_player.color == piece.color:
                        standing_tile = piece.tile
            elif move[0] == "R":
                for piece in self.pieces:
                    if isinstance(piece, Rook) and target_tile in piece.possible_moves(self.board) and self.current_player.color == piece.color:
                        standing_tile = piece.tile
            elif move[0] == "B":
                for piece in self.pieces:
                    if isinstance(piece, Bishop) and target_tile in piece.possible_moves(self.board) and self.current_player.color == piece.color:
                        standing_tile = piece.tile
            elif move[0] == "Q":
                for piece in self.pieces:
                    if isinstance(piece, Queen) and target_tile in piece.possible_moves(self.board) and self.current_player.color == piece.color:
                        standing_tile = piece.tile
            elif move[0] == "K":
                for piece in self.pieces:
                    if isinstance(piece, King) and target_tile in piece.possible_moves(self.board) and self.current_player.color == piece.color:
                        standing_tile = piece.tile

        if standing_tile:
            movement = self.move_piece(standing_tile, target_tile)
            if self.is_in_check(self.current_player.color): # King is still in check after move
                self.undo_move(movement)
                return False
            else:
                return True
        else:
            return False

        
            
    def move_piece(self, standing_tile, target_tile):
        #print(f"Moving from {standing_tile.file}{standing_tile.rank} to {target_tile.file}{target_tile.rank}")
        piece = standing_tile.piece
        standing_tile.remove_piece()
        if target_tile.piece != None: # Opponent piece is killed
            targeted_piece = target_tile.piece
            t_index = self.pieces.index(targeted_piece)
            self.destroy_piece(target_tile.piece)
        else:
            targeted_piece = None
            t_index = None
        target_tile.add_piece(piece)
        piece.update_position(target_tile)
        return {"piece": piece, "st": standing_tile, "t_piece": targeted_piece, "tt": target_tile, "t_index": t_index}


    def undo_move(self, move):
        """ This function reverts the movement previously made with the move_piece function"""
        move["st"].add_piece(move["piece"])
        move["piece"].tile = move["st"]
        move["piece"].past_tiles.pop()
        move["tt"].add_piece(move["t_piece"])
        if move["t_piece"] != None:
            move["t_piece"].tile = move["tt"]
            self.pieces.insert(move["t_index"], move["t_piece"])
            self.graveyard.remove(move["t_piece"])

    
    def destroy_piece(self, piece):
        self.pieces.remove(piece)
        piece.tile = None
        self.graveyard.append(piece)

    # --- Checkmate Helper Functions --- #

    def is_attacked(self, tile, by_color):
        """ This function determines if a given tile is being attacked by a specific color."""
        for piece in self.pieces:
            if piece.color == by_color:
                if tile in piece.possible_moves(self.board):
                    return True
        return False

    def is_in_check(self, color):
        """ This function determines if a given color is in check."""
        king = None
        for piece in self.pieces:
            if piece.name == "King" and piece.color == color:
                king = piece
        return self.is_attacked(king.tile, self.enemy_color(color))

    def has_any_legal_move(self, color):
        """ This function determines if a given color has the ability to make a move that doesn't leave their king in check. Determines checkmate"""
        for piece in self.pieces:
            if piece.color == color:
                for target in piece.possible_moves(self.board):
                    record = self.move_piece(piece.tile, target)
                    king_is_safe = not self.is_in_check(color)
                    self.undo_move(record)
                    if king_is_safe: 
                        return True
        return False

        


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