"""Check detection: ``is_attacked`` and ``is_in_check``."""

import unittest

from tests.helpers import BLACK, WHITE, ChessTestCase, position, square_tile


class IsInCheckTest(ChessTestCase):
    def assertCheck(self, white, black, color, expected, message=""):
        game = position(white, black)
        self.assertEqual(game.is_in_check(color), expected, message)
        return game

    def test_rook_checks_along_a_file(self):
        self.assertCheck("Ka1 Re4", "Ke8", BLACK, True)

    def test_rook_checks_along_a_rank(self):
        self.assertCheck("Ka1 Ra8", "Ke8", BLACK, True)

    def test_rook_line_blocked_by_a_friendly_piece_is_not_check(self):
        self.assertCheck("Ka1 Re1 Be4", "Ke8", BLACK, False)

    def test_rook_line_blocked_by_an_enemy_piece_is_not_check(self):
        self.assertCheck("Ka1 Re1", "Ke8 Ne4", BLACK, False)

    def test_bishop_checks_along_a_diagonal(self):
        self.assertCheck("Ka1 Ba4", "Ke8", BLACK, True)

    def test_blocked_diagonal_is_not_check(self):
        self.assertCheck("Ka1 Ba4 c6", "Ke8", BLACK, False)

    def test_knight_check_cannot_be_blocked_by_adjacent_pieces(self):
        self.assertCheck("Ka1 Nf6", "Ke8 d7 e7 f7", BLACK, True)

    def test_queen_checks_on_both_the_line_and_the_diagonal(self):
        self.assertCheck("Ka1 Qe4", "Ke8", BLACK, True)
        self.assertCheck("Ka1 Qa4", "Ke8", BLACK, True)

    def test_pawn_checks_diagonally(self):
        """A White pawn on d4 attacks c5 and e5."""
        self.assertCheck("Ka1 d4", "Kc5", BLACK, True)
        self.assertCheck("Ka1 d4", "Ke5", BLACK, True)
        self.assertCheck("Ka1 d4", "Kc3", BLACK, False)  # pawns do not attack backwards

    def test_pawn_does_not_check_the_square_straight_ahead(self):
        self.assertCheck("Ka1 e4", "Ke5", BLACK, False)

    def test_black_pawn_checks_downwards(self):
        self.assertCheck("Kd4", "Ke8 e5", WHITE, True)
        self.assertCheck("Kd6", "Ke8 e5", WHITE, False)

    def test_adjacent_enemy_king_counts_as_an_attacker(self):
        self.assertCheck("Ke4", "Ke5", WHITE, True)

    def test_a_friendly_piece_never_gives_check(self):
        """A White rook on the same file as the White king is harmless."""
        self.assertCheck("Ke1 Re4", "Ke8", WHITE, False)

    def test_quiet_position_is_not_check_for_either_side(self):
        game = position("Ke1 Nb1", "Ke8 Nb8")
        self.assertFalse(game.is_in_check(WHITE))
        self.assertFalse(game.is_in_check(BLACK))

    def test_check_is_reported_for_the_right_king(self):
        """Both kings are on the board; only the attacked one is in check."""
        game = position("Ke1 Ra8", "Ke8")
        self.assertTrue(game.is_in_check(BLACK))
        self.assertFalse(game.is_in_check(WHITE))


class IsAttackedTest(ChessTestCase):
    def test_attacked_squares_are_filtered_by_colour(self):
        game = position("Ke1 Rd1", "Ke8 Rd8")
        d4 = square_tile(game, "d4")
        self.assertTrue(game.is_attacked(d4, WHITE))
        self.assertTrue(game.is_attacked(d4, BLACK))

        a4 = square_tile(game, "a4")
        self.assertFalse(game.is_attacked(a4, WHITE))
        self.assertFalse(game.is_attacked(a4, BLACK))

    def test_empty_square_beyond_a_blocker_is_not_attacked(self):
        game = position("Ke1 Ra1 Bd1", "Ke8")
        self.assertTrue(game.is_attacked(square_tile(game, "c1"), WHITE))
        self.assertFalse(game.is_attacked(square_tile(game, "e1"), WHITE))

    def test_knight_attacks_ignore_occupancy_in_between(self):
        game = position("Ke1 Nb1 a2 b2 c2 d2", "Ke8")
        for square in ("a3", "c3", "d2"):
            tile = square_tile(game, square)
            occupied_by_friend = tile.piece is not None and tile.piece.color == WHITE
            self.assertEqual(
                game.is_attacked(tile, WHITE),
                not occupied_by_friend,
                f"knight attack on {square} misreported",
            )


if __name__ == "__main__":
    unittest.main()
