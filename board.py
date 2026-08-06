class Board:
    def __init__(self):
        self.board = [[] for _ in range(8)]
        x, y = 0, -1
        color = 1 # White is 1, Black is 0
        for i in range(64):
            if i % 8 == 0:
                y += 1
                x = 0
                color ^= 1
            self.board[y].append(Tile("White" if color == 1 else "Black", x, y))
            x += 1
            color ^= 1
             
        
    def print_board(self):
        for row in self.board:
            print("|", end="")
            for tile in row:
                if tile.piece != None: 
                    print(tile.piece.icon + "  ", end="")
                else:
                    print(".  ", end="")
            print("|")


    def print_default_board(self):

        b = """ 
            8 | ♜  ♞  ♝  ♛  ♚  ♝  ♞  ♜ |
            7 | ♟  ♟  ♟  ♟  ♟  ♟  ♟  ♟ |
            6 | .  .  .  .  .  .  .  . |
            5 | .  .  .  .  .  .  .  . |
            4 | .  .  .  .  .  .  .  . |
            3 | .  .  .  .  .  .  .  . |
            2 | ♙  ♙  ♙  ♙  ♙  ♙  ♙  ♙ |
            1 | ♖  ♘  ♗  ♕  ♔  ♗  ♘  ♖ |
        """
        print(b)


class Tile:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.piece = None

    def add_piece(self, piece):
        self.piece = piece

    def remove_piece(self, piece):
        self.piece = None
