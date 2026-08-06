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
             
        self.print_board()

    def print_board(self):
        for row in self.board:
            print(row)


            


class Tile:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
