class Piece:
    def __init__(self, color, icon, tile, name):
        self.color = color
        self.icon = icon
        self.tile = tile
        self.past_tiles = [tile]
        self.name = name

    def update_position(self, tile):
        self.past_tiles.append(self.tile)
        self.tile = tile

    def possible_moves(self, board):
        return []
    
    def add_move(self, moves, tile): # Works for all movements except for generic pawn movements
        if tile != None and (tile.piece == None or tile.piece.color != self.color):
            moves.append(tile)

class Pawn(Piece):
    def __init__(self, color, tile):
        icon = "♟" if color == "White" else "♙"
        self.direction = 1 if color == "White" else -1
        super().__init__(color, icon, tile, "Pawn")

    def possible_moves(self, board):
        moves = []
        # Generic pawn movements
        if board.get_tile(self.tile.file, self.tile.rank + (1 * self.direction)).piece == None: 
            moves.append(board.get_tile(self.tile.file, self.tile.rank + (1 * self.direction)))
            if len(self.past_tiles) == 1 and board.get_tile(self.tile.file, self.tile.rank + (2 * self.direction)).piece == None:
                moves.append(board.get_tile(self.tile.file, self.tile.rank + (2 * self.direction)))
        # Capture movements
        self.add_move(board.find_tile(self.tile, -1, (1 * self.direction)))
        self.add_move(board.find_tile(self.tile, 1, (1 * self.direction)))
        return moves
        


class Knight(Piece):
    def __init__(self, color, tile):
        icon = "♞" if color == "White" else "♘"
        super().__init__(color, icon, tile, "Knight")

    def possible_moves(self, board):
        moves = []
        self.add_move(board.find_tile(self.tile, -1, 2))
        self.add_move(board.find_tile(self.tile, -1, -2))
        self.add_move(board.find_tile(self.tile, -2, 1))
        self.add_move(board.find_tile(self.tile, -2, -1))
        self.add_move(board.find_tile(self.tile, 1, 2))
        self.add_move(board.find_tile(self.tile, 1, -2))
        self.add_move(board.find_tile(self.tile, 2, 1))
        self.add_move(board.find_tile(self.tile, 2, -1))
        return moves


class Rook(Piece):
    def __init__(self, color, tile):
        icon = "♜" if color == "White" else "♖"
        super().__init__(color, icon, tile, "Rook")

class Bishop(Piece):
    def __init__(self, color, tile):
        icon = "♝" if color == "White" else "♗"
        super().__init__(color, icon, tile, "Bishop")

class Queen(Piece):
    def __init__(self, color, tile):
        icon = "♛" if color == "White" else "♕"
        super().__init__(color, icon, tile, "Queen")

class King(Piece):
    def __init__(self, color, tile):
        icon = "♚" if color == "White" else "♔"
        super().__init__(color, icon, tile, "King")