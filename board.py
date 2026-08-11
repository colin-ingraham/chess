class Board:
    def __init__(self):
        self.board = [[] for _ in range(8)]
        file = 'a'
        rank = 9
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

    def get_tile(self, file, rank):
        x = ord(file) - 97
        y = (rank - 8) * - 1
        #print(f"Accessing board position ({x},{y})")
        if x < 0 or x > 7:
            return None
        if y < 0 or y > 7:
            return None
        return self.board[y][x]

    # Takes a current tile and returns a new tile with a specified shift. Used for piece movements.
    def find_tile(self, current, shift_right, shift_up):
        new_rank = current.rank + shift_up
        if new_rank < 1 or new_rank > 8:
            return None
        ord_file = ord(current.file) + shift_right
        if ord_file < 97 or ord_file > 104:
            return None
        new_file = chr(ord_file)
        return self.get_tile(new_file, new_rank)

    def sort_graveyard(self, graveyard):
        whites = []
        blacks = []
        print_whites = []
        print_blacks = []
        for piece in graveyard:
            if piece.color == "White":
                whites.append(piece)
                print_whites.append(piece.icon)
            else:
                blacks.append(piece)
                print_blacks.append(piece.icon)
        return whites, blacks, print_whites, print_blacks

    def calculate_diff(self, whites, blacks):
        scores = {"Pawn": 1, "Knight": 3, "Bishop": 3, "Rook": 6, "Queen": 9}
        w_score = 0
        b_score = 0
        for piece in whites:
            w_score += scores[piece.name]
        for piece in blacks:
            b_score += scores[piece.name]
        if w_score > b_score:
            winning = "Black"
        elif w_score < b_score:
            winning = "White"
        else:
            winning = "None"
        return abs(w_score - b_score), winning
        

    def print_board(self, graveyard, p1, p2):
        whites, blacks, print_whites, print_blacks = self.sort_graveyard(graveyard)
        diff, winning = self.calculate_diff(whites, blacks)
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
            

            if i == 6:
                print("|", end="")
                black = p1 if p1.color == "Black" else p2
                print(f"   {black.name}: ", end=" ")
                print("".join(print_whites), end="")
                if winning == "Black":
                    print(f" (+{diff})")
                else:
                    print("")
            elif i == 3:
                print("|", end="")
                white = p1 if p1.color == "White" else p2
                print(f"   {white.name}: ", end=" ")
                print("".join(print_blacks), end="")
                if winning == "White":
                    print(f" (+{diff})")
                else:
                    print("")
            else:
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

    def left_file(self):
        if self.file == 'a':
            return None
        else:
            return chr(ord(self.file) - 1)

    def right_file(self):
        if self.file == 'h':
            return None
        else:
            return chr(ord(self.file) + 1)

    
    