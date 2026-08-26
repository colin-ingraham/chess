"""Shared test helpers for building headless games and positions.

``Game.__init__`` sets up a full board, prints it, and then enters an
interactive ``game_loop`` that blocks on ``input()``.  None of that is usable
from a test, so the helpers here build a ``Game`` instance without running the
constructor and populate only the state the rules code actually reads:
``board``, ``pieces``, ``graveyard``, the two players and ``current_player``.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from board import Board
from game import Game
from piece import Bishop, King, Knight, Pawn, Queen, Rook
from player import Player

# Piece letters follow standard algebraic notation; a bare square means a pawn.
PIECE_TYPES = {
    "K": King,
    "Q": Queen,
    "R": Rook,
    "B": Bishop,
    "N": Knight,
    "P": Pawn,
}

WHITE = "White"
BLACK = "Black"


def bare_game():
    """A ``Game`` with an empty board and no pieces, bypassing ``__init__``."""
    game = Game.__new__(Game)
    game.player1 = Player("WhitePlayer", WHITE)
    game.player2 = Player("BlackPlayer", BLACK)
    game.current_player = game.player1
    game.game_over = False
    game.board = Board()
    game.pieces = []
    game.whites = []
    game.blacks = []
    game.graveyard = []
    return game


def standard_game():
    """A ``Game`` in the normal starting position, with no game loop running."""
    game = bare_game()
    game.setup_pieces()
    return game


def parse_placement(token):
    """Split a placement token such as ``"Qd1"`` or ``"e2"`` into (letter, square)."""
    if len(token) == 3:
        letter, square = token[0], token[1:]
    elif len(token) == 2:
        letter, square = "P", token
    else:
        raise ValueError(f"Malformed placement token: {token!r}")
    if letter not in PIECE_TYPES:
        raise ValueError(f"Unknown piece letter {letter!r} in {token!r}")
    return letter, square


def place(game, color, token):
    """Create one piece from a placement token and put it on the board."""
    letter, square = parse_placement(token)
    tile = square_tile(game, square)
    if tile is None:
        raise ValueError(f"Placement token {token!r} names a square off the board")
    if tile.piece is not None:
        raise ValueError(f"Two pieces placed on {square}")
    piece = PIECE_TYPES[letter](color, tile)
    tile.add_piece(piece)
    game.pieces.append(piece)
    return piece


def position(white, black, turn=WHITE):
    """Build a game from two space-separated placement strings.

    ``position("Ke1 Qd1 e2", "Ke8 Ra8")`` gives White a king, queen and pawn and
    Black a king and rook.  Both kings must be present: ``is_in_check`` looks the
    king up unconditionally and would raise without one.
    """
    game = bare_game()
    for token in white.split():
        place(game, WHITE, token)
    for token in black.split():
        place(game, BLACK, token)
    set_turn(game, turn)
    return game


def set_turn(game, color):
    game.current_player = game.player1 if game.player1.color == color else game.player2
    return game.current_player


def square_tile(game, square):
    """Look a tile up by name, e.g. ``"e4"``."""
    return game.board.get_tile(square[0], int(square[1:]))


def piece_at(game, square):
    tile = square_tile(game, square)
    return None if tile is None else tile.piece


def square_name(tile):
    return f"{tile.file}{tile.rank}"


def squares(tiles):
    """Normalise a list of tiles into a set of square names for comparison."""
    return {square_name(tile) for tile in tiles}


def moves_from(game, square):
    """Square names a piece claims it can move to (pseudo-legal: pins ignored)."""
    piece = piece_at(game, square)
    if piece is None:
        raise AssertionError(f"No piece on {square}")
    return squares(piece.possible_moves(game.board))


class ChessTestCase(unittest.TestCase):
    """Base class adding assertions that report squares rather than objects."""

    def assertMovesEqual(self, game, square, expected):
        expected = set(expected.split()) if isinstance(expected, str) else set(expected)
        self.assertEqual(moves_from(game, square), expected)

    def assertOccupied(self, game, square, name, color):
        piece = piece_at(game, square)
        self.assertIsNotNone(piece, f"expected a piece on {square}, found none")
        self.assertEqual((piece.name, piece.color), (name, color))

    def assertEmpty(self, game, square):
        self.assertIsNone(piece_at(game, square), f"expected {square} to be empty")

    def assertCheckmate(self, game, color):
        self.assertTrue(game.is_in_check(color), f"{color} is not in check")
        self.assertFalse(
            game.has_any_legal_move(color), f"{color} still has a legal move"
        )

    def assertStalemate(self, game, color):
        self.assertFalse(game.is_in_check(color), f"{color} is in check")
        self.assertFalse(
            game.has_any_legal_move(color), f"{color} still has a legal move"
        )

    def assertPlayable(self, game, color):
        """In check or not, the side to move can still make some legal move."""
        self.assertTrue(
            game.has_any_legal_move(color), f"{color} has no legal move available"
        )


def mark_moved(piece):
    """Make a piece look like it has already moved.

    ``Pawn.possible_moves`` infers "has not moved yet" from
    ``len(past_tiles) == 1`` rather than from a flag, so a pawn dropped onto a
    non-home square by ``position()`` would still offer a double step.  Tests
    that need a pawn away from its home rank call this to fake the history.
    """
    piece.past_tiles.append(piece.tile)
    return piece


def play(game, *moves):
    """Apply a sequence of algebraic moves, alternating players as the loop does.

    Raises ``AssertionError`` if the parser rejects a move, so a test failure
    points at the move that broke rather than at a later assertion.
    """
    for move in moves:
        accepted = game.parse_move(move)
        if not accepted:
            raise AssertionError(
                f"parse_move({move!r}) rejected the move for {game.current_player.color}"
            )
        game.current_player = (
            game.player1 if game.current_player is game.player2 else game.player2
        )
    return game


def move(game, origin, destination):
    """Apply a raw board move, bypassing notation parsing and legality checks."""
    return game.move_piece(square_tile(game, origin), square_tile(game, destination))
