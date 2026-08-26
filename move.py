class Move:
    def __init__(self, piece, origin, destination, kind, captured=None, captured_tile=None, promotion_type=None):
        self.piece = piece
        self.origin = origin
        self.destination = destination
        self.kind = kind



class Capture(Move):
    def __init__(self, piece, origin, destination, kind, captured, captured_tile, promotion_type=None):
        super().__init__(piece, origin, destination, kind)
        self.captured = captured
        self.captured_tile = captured_tile

class Castle(Move):
    def __init__(self, piece, origin, destination, kind, rook_origin, rook_destination):
        super().__init__(piece, origin, destination, kind)
        self.rook_origin = rook_origin
        self.rook_destination = rook_destination



    