class Piece:
    def __init__(self, color, icon, tile):
        self.color = color
        self.icon = icon
        self.tile = tile
        self.past_tiles = [tile]

    def update_position(self, tile):
        self.past_tiles.append(self.tile)
        self.tile = tile

    def possible_moves(self, board):
        return []

class Pawn(Piece):
    def __init__(self, color, tile):
        icon = "♟" if color == "White" else "♙"
        self.direction = 1 if color == "White" else -1
        super().__init__(color, icon, tile)

    def possible_moves(self, board):
        moves = []
        # Generic pawn movements
        if board.get_tile(self.tile.file, self.tile.rank + (1 * self.direction)).piece == None: 
            moves.append(board.get_tile(self.tile.file, self.tile.rank + (1 * self.direction)))
            if len(self.past_tiles) == 1 and board.get_tile(self.tile.file, self.tile.rank + (2 * self.direction)).piece == None:
                moves.append(board.get_tile(self.tile.file, self.tile.rank + (2 * self.direction)))
        # Capture movements
        if self.tile.left_file() != None:
            if board.get_tile(self.tile.left_file(), self.tile.rank + (1 * self.direction)).piece: 
                moves.append(board.get_tile(self.tile.left_file(), self.tile.rank + (1 * self.direction)))
        if self.tile.right_file() != None:
            if board.get_tile(self.tile.right_file(), self.tile.rank + (1 * self.direction)).piece: 
                moves.append(board.get_tile(self.tile.right_file(), self.tile.rank + (1 * self.direction)))
        return moves
        


class Knight(Piece):
    def __init__(self, color, tile):
        icon = "♞" if color == "White" else "♘"
        super().__init__(color, icon, tile)

class Rook(Piece):
    def __init__(self, color, tile):
        icon = "♜" if color == "White" else "♖"
        super().__init__(color, icon, tile)

class Bishop(Piece):
    def __init__(self, color, tile):
        icon = "♝" if color == "White" else "♗"
        super().__init__(color, icon, tile)

class Queen(Piece):
    def __init__(self, color, tile):
        icon = "♛" if color == "White" else "♕"
        super().__init__(color, icon, tile)

class King(Piece):
    def __init__(self, color, tile):
        icon = "♚" if color == "White" else "♔"
        super().__init__(color, icon, tile)