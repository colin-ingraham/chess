"""The starting position: piece placement, counts and board/piece consistency."""

import unittest

from tests.helpers import BLACK, WHITE, ChessTestCase, square_name, standard_game

BACK_RANK = {
    "a": "Rook",
    "b": "Knight",
    "c": "Bishop",
    "d": "Queen",
    "e": "King",
    "f": "Bishop",
    "g": "Knight",
    "h": "Rook",
}

FILES = "abcdefgh"


class StartingPositionTest(ChessTestCase):
    def setUp(self):
        self.game = standard_game()

    def test_board_holds_thirty_two_pieces(self):
        self.assertEqual(len(self.game.pieces), 32)
        self.assertEqual(self.game.graveyard, [])

    def test_each_side_has_sixteen_pieces(self):
        by_color = {WHITE: 0, BLACK: 0}
        for piece in self.game.pieces:
            by_color[piece.color] += 1
        self.assertEqual(by_color, {WHITE: 16, BLACK: 16})

    def test_white_back_rank(self):
        for file, name in BACK_RANK.items():
            self.assertOccupied(self.game, f"{file}1", name, WHITE)

    def test_black_back_rank(self):
        for file, name in BACK_RANK.items():
            self.assertOccupied(self.game, f"{file}8", name, BLACK)

    def test_pawns_fill_the_second_and_seventh_ranks(self):
        for file in FILES:
            self.assertOccupied(self.game, f"{file}2", "Pawn", WHITE)
            self.assertOccupied(self.game, f"{file}7", "Pawn", BLACK)

    def test_middle_of_the_board_is_empty(self):
        for rank in range(3, 7):
            for file in FILES:
                self.assertEmpty(self.game, f"{file}{rank}")

    def test_queens_start_on_their_own_colour_file(self):
        self.assertOccupied(self.game, "d1", "Queen", WHITE)
        self.assertOccupied(self.game, "d8", "Queen", BLACK)

    def test_every_piece_agrees_with_the_tile_it_stands_on(self):
        for piece in self.game.pieces:
            self.assertIs(
                piece.tile.piece,
                piece,
                f"{piece.color} {piece.name} on {square_name(piece.tile)} is out of sync",
            )

    def test_no_piece_starts_with_move_history(self):
        for piece in self.game.pieces:
            self.assertEqual(len(piece.past_tiles), 1)

    def test_white_moves_first(self):
        self.assertEqual(self.game.current_player.color, WHITE)


class StartingPositionRulesTest(ChessTestCase):
    """The rules layer should consider the opening position quiet and playable."""

    def setUp(self):
        self.game = standard_game()

    def test_neither_king_starts_in_check(self):
        self.assertFalse(self.game.is_in_check(WHITE))
        self.assertFalse(self.game.is_in_check(BLACK))

    def test_both_sides_have_legal_moves(self):
        self.assertPlayable(self.game, WHITE)
        self.assertPlayable(self.game, BLACK)

    def test_opening_position_offers_twenty_moves_per_side(self):
        for color in (WHITE, BLACK):
            total = sum(
                len(piece.possible_moves(self.game.board))
                for piece in self.game.pieces
                if piece.color == color
            )
            self.assertEqual(total, 20, f"{color} should have 20 opening moves")

    def test_blocked_back_rank_pieces_cannot_move(self):
        for file in FILES:
            if file in ("b", "g"):  # knights jump over the pawns
                continue
            self.assertMovesEqual(self.game, f"{file}1", "")
            self.assertMovesEqual(self.game, f"{file}8", "")


if __name__ == "__main__":
    unittest.main()
