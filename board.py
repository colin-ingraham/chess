class Board:
    def __init__(self):
        self.board = [[] for _ in range(8)]
        file = 'a'
        rank = 8
        y = -1
        color = 1 # White is 1, Black is 0
        for i in range(64):
            if i % 8 == 0:
                y += 1
                rank -= 1
                file = 'a'
                color ^= 1
            self.board[y].append(Tile("White" if color == 1 else "Black", file, rank))
            file = chr(ord(file) + 1)
            color ^= 1
        
    def print_board(self):
        i = 8
        print("   ────────────────────────")
        for row in self.board:
            print(f"{i} ", end="")
            print("| ", end="")
            for tile in row:
                if tile.piece != None: 
                    print(tile.piece.icon + "  ", end="")
                else:
                    print(".  ", end="")
            print("|")
            i -= 1
        print("   ────────────────────────")
        print("    a  b  c  d  e  f  g  h ")


class Tile:
    def __init__(self, color, file, rank):
        self.color = color
        self.file = file
        self.rank = rank
        self.piece = None

    def add_piece(self, piece):
        self.piece = piece
        return self.piece

    def remove_piece(self):
        self.piece = None

    def get_piece(self, piece):
        return piece