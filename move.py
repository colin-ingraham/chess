QUIET = "QUIET"
CAPTURE = "CAPTURE"
DOUBLE_PAWN_PUSH = "DOUBLE_PAWN_PUSH"
CASTLE = "CASTLE"
EN_PASSANT = "EN_PASSANT"
PROMOTION = "PROMOTION"

class Move:
    def __init__(self, piece, origin, destination, kind, captured=None, captured_index=None, captured_tile=None, promotion_type=None):
        self.piece = piece
        self.origin = origin
        self.destination = destination
        self.kind = kind
        self.captured = captured
        self.captured_index = captured_index
        self.captured_tile = captured_tile
        self.promotion_type = promotion_type

    def key(self): 
        return (self.origin, self.destination, self.promotion_type)

    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return self.key() == other.key()

    def __hash__(self):
        return hash(self.key())

    def __repr__(self):
        return (f"<Move {self.piece.name} "
                f"{self.origin.file}{self.origin.rank}->"
                f"{self.destination.file}{self.destination.rank} {self.kind}>")
    


class Castle(Move):
    def __init__(self, piece, origin, destination, kind, rook_origin, rook_destination):
        super().__init__(piece, origin, destination, kind)
        self.rook_origin = rook_origin
        self.rook_destination = rook_destination



    