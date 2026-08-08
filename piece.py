class Piece:
    def __init__(self, color, icon, tile):
        self.color = color
        self.icon = icon
        self.tile

    def update_position(self, tile):
        self.tile = tile

class Pawn(Piece):
    def __init__(self, color, tile):
        icon = "♟" if color == "White" else "♙"
        super().__init__(color, icon, tile)

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