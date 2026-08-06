class Piece:
    def __init__(self, color, icon):
        self.color = color
        self.icon = icon



class Pawn(Piece):
    def __init__(self, color):
        icon = "♟" if color == "White" else "♙"
        super().__init__(color, icon)
        