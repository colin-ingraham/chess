class Piece:
    def __init__(self, color, icon, file, rank):
        self.color = color
        self.icon = icon
        self.file = file
        self.rank = rank

    def update_position(self, file, rank):
        self.file = file
        self.rank = rank

class Pawn(Piece):
    def __init__(self, color, file, rank):
        icon = "♟" if color == "White" else "♙"
        super().__init__(color, icon, file, rank)

class Knight(Piece):
    def __init__(self, color, file, rank):
        icon = "♞" if color == "White" else "♘"
        super().__init__(color, icon, file, rank)

class Rook(Piece):
    def __init__(self, color, file, rank):
        icon = "♜" if color == "White" else "♖"
        super().__init__(color, icon, file, rank)

class Bishop(Piece):
    def __init__(self, color, file, rank):
        icon = "♝" if color == "White" else "♗"
        super().__init__(color, icon, file, rank)

class Queen(Piece):
    def __init__(self, color, file, rank):
        icon = "♛" if color == "White" else "♕"
        super().__init__(color, icon, file, rank)

class King(Piece):
    def __init__(self, color, file, rank):
        icon = "♚" if color == "White" else "♔"
        super().__init__(color, icon, file, rank)