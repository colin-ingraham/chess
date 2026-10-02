from move import *
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

    def add_move(self, moves, origin, destination): # Works for all movements except pawn movements.
        if destination is None:
            return
        if destination.piece is None:
            moves.append(Move(self, origin, destination, QUIET))
        elif destination.piece.color != self.color:
            moves.append(Move(self, origin, destination, CAPTURE))

class Pawn(Piece):
    def __init__(self, color, tile):
        icon = "♟" if color == "White" else "♙"
        self.direction = 1 if color == "White" else -1
        super().__init__(color, icon, tile, "Pawn")

    def possible_moves(self, board):
        moves = []
        origin = board.get_tile(self.tile.file, self.tile.rank)
        # Generic pawn movements
        if board.get_tile(self.tile.file, self.tile.rank + (1 * self.direction)).piece == None: 
            destination = board.get_tile(self.tile.file, self.tile.rank + (1 * self.direction))
            move = Move(piece=self, origin=origin, destination=destination, kind=QUIET)
            moves.append(move)
            if len(self.past_tiles) == 1 and board.get_tile(self.tile.file, self.tile.rank + (2 * self.direction)).piece == None:
                move = Move(piece=self, origin=origin, destination=board.get_tile(self.tile.file, self.tile.rank + (2 * self.direction)), kind="DOUBLE_PAWN_PUSH")
                moves.append(move)
        # Capture movements
        destination = board.find_tile(self.tile, -1, (1 * self.direction))
        move = Move(piece=self, origin=origin, destination=destination, kind=CAPTURE)
        if move.destination != None and (move.destination.piece != None and move.destination.piece.color != self.color):
            moves.append(move)
        destination = board.find_tile(self.tile, 1, (1 * self.direction))
        move = Move(piece=self, origin=origin, destination=destination, kind=CAPTURE)
        if move.destination != None and (move.destination.piece != None and move.destination.piece.color != self.color):
            moves.append(move)
        return moves
        


class Knight(Piece):
    def __init__(self, color, tile):
        icon = "♞" if color == "White" else "♘"
        super().__init__(color, icon, tile, "Knight")

    def possible_moves(self, board):
        moves = []
        origin = board.get_tile(self.tile.file, self.tile.rank)
        self.add_move(moves, origin, board.find_tile(self.tile, -1, 2))
        self.add_move(moves, origin, board.find_tile(self.tile, -1, -2))
        self.add_move(moves, origin, board.find_tile(self.tile, -2, 1))
        self.add_move(moves, origin, board.find_tile(self.tile, -2, -1))
        self.add_move(moves, origin, board.find_tile(self.tile, 1, 2))
        self.add_move(moves, origin, board.find_tile(self.tile, 1, -2))
        self.add_move(moves, origin, board.find_tile(self.tile, 2, 1))
        self.add_move(moves, origin, board.find_tile(self.tile, 2, -1))
        return moves


class Rook(Piece):
    def __init__(self, color, tile):
        icon = "♜" if color == "White" else "♖"
        super().__init__(color, icon, tile, "Rook")

    def possible_moves(self, board):
        moves = []
        origin = board.get_tile(self.tile.file, self.tile.rank)
        shifts = [[0, 1, 1], [0, -1, 1], [1, 0, 0], [-1, 0, 0]]
        for shift in shifts:
            tile = board.find_tile(self.tile, shift[0], shift[1])
            while tile != None:
                if tile.piece != None:
                    if tile.piece.color != self.color:
                        self.add_move(moves, origin, tile)
                        break
                    else:
                        break
                self.add_move(moves, origin, tile)
                if shift[shift[2]] > 0:
                    shift[shift[2]] += 1
                else:
                    shift[shift[2]] -= 1
                tile = board.find_tile(self.tile, shift[0], shift[1])
        return moves      


class Bishop(Piece):
    def __init__(self, color, tile):
        icon = "♝" if color == "White" else "♗"
        super().__init__(color, icon, tile, "Bishop")

    def possible_moves(self, board): 
        moves = []
        origin = board.get_tile(self.tile.file, self.tile.rank)
        shifts = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
        for shift in shifts:
            tile = board.find_tile(self.tile, shift[0], shift[1])
            while tile != None:
                if tile.piece != None:
                    if tile.piece.color != self.color:
                        self.add_move(moves, origin, tile)
                        break
                    else:
                        break
                self.add_move(moves, origin, tile)
                if shift[0] > 0:
                    shift[0] += 1
                else:
                    shift[0] -= 1
                if shift[1] > 0:
                    shift[1] += 1
                else:
                    shift[1] -= 1
                tile = board.find_tile(self.tile, shift[0], shift[1])
        return moves

class Queen(Piece):
    def __init__(self, color, tile):
        icon = "♛" if color == "White" else "♕"
        super().__init__(color, icon, tile, "Queen")

    def possible_moves(self, board):
        moves = []
        moves += Rook.possible_moves(self, board)
        moves += Bishop.possible_moves(self, board)
        return moves

class King(Piece):
    def __init__(self, color, tile):
        icon = "♚" if color == "White" else "♔"
        super().__init__(color, icon, tile, "King")

    def possible_moves(self, board):
        moves = []
        origin = board.get_tile(self.tile.file, self.tile.rank)
        self.add_move(moves, origin, board.find_tile(self.tile, 0, 1))
        self.add_move(moves, origin, board.find_tile(self.tile, 1, 1))
        self.add_move(moves, origin, board.find_tile(self.tile, 1, 0))
        self.add_move(moves, origin, board.find_tile(self.tile, 1, -1))
        self.add_move(moves, origin, board.find_tile(self.tile, 0, -1))
        self.add_move(moves, origin, board.find_tile(self.tile, -1, -1))
        self.add_move(moves, origin, board.find_tile(self.tile, -1, 0))
        self.add_move(moves, origin, board.find_tile(self.tile, -1, 1))
        return moves