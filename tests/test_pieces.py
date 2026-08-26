"""Per-piece move generation (``possible_moves``).

These are pseudo-legal moves: pins and checks are not considered here, that
filtering happens in ``Game.has_any_legal_move`` and ``Game.parse_move``.
"""

import unittest

from tests.helpers import BLACK, WHITE, ChessTestCase, mark_moved, piece_at, position


class RookTest(ChessTestCase):
    def test_rook_sweeps_both_axes_from_an_empty_board(self):
        game = position("Rd4", "")
        self.assertMovesEqual(
            game, "d4", "d1 d2 d3 d5 d6 d7 d8 a4 b4 c4 e4 f4 g4 h4"
        )

    def test_rook_in_a_corner_reaches_fourteen_squares(self):
        game = position("Ra1", "")
        self.assertEqual(len(piece_at(game, "a1").possible_moves(game.board)), 14)

    def test_rook_stops_before_a_friendly_piece(self):
        game = position("Rd4 Bd6", "")
        self.assertMovesEqual(game, "d4", "d1 d2 d3 d5 a4 b4 c4 e4 f4 g4 h4")

    def test_rook_stops_on_an_enemy_piece(self):
        game = position("Rd4", "Bd6")
        self.assertMovesEqual(game, "d4", "d1 d2 d3 d5 d6 a4 b4 c4 e4 f4 g4 h4")

    def test_rook_boxed_in_has_no_moves(self):
        game = position("Ra1 a2 Nb1", "")
        self.assertMovesEqual(game, "a1", "")


class BishopTest(ChessTestCase):
    def test_bishop_sweeps_both_diagonals(self):
        game = position("Bd4", "")
        self.assertMovesEqual(
            game, "d4", "a1 b2 c3 e5 f6 g7 h8 a7 b6 c5 e3 f2 g1"
        )

    def test_bishop_in_a_corner_reaches_seven_squares(self):
        game = position("Ba1", "")
        self.assertMovesEqual(game, "a1", "b2 c3 d4 e5 f6 g7 h8")

    def test_bishop_stops_before_a_friendly_piece_and_on_an_enemy(self):
        game = position("Bd4 c3", "Bf6")
        self.assertMovesEqual(game, "d4", "e5 f6 a7 b6 c5 e3 f2 g1")

    def test_bishop_never_leaves_its_starting_colour_complex(self):
        game = position("Bd4", "")
        light = {"a1", "c3", "e5", "g7", "b2", "d4", "f6", "h8"}
        dark = {"a7", "b6", "c5", "e3", "f2", "g1"}
        reachable = {
            f"{tile.file}{tile.rank}"
            for tile in piece_at(game, "d4").possible_moves(game.board)
        }
        self.assertTrue(reachable <= (light | dark))


class QueenTest(ChessTestCase):
    def test_queen_combines_rook_and_bishop_lines(self):
        game = position("Qd4", "")
        self.assertEqual(len(piece_at(game, "d4").possible_moves(game.board)), 27)

    def test_queen_in_a_corner(self):
        game = position("Qa1", "")
        self.assertEqual(len(piece_at(game, "a1").possible_moves(game.board)), 21)

    def test_queen_respects_blockers(self):
        game = position("Qd4 d5 c3", "Bf6")
        moves = piece_at(game, "d4").possible_moves(game.board)
        names = {f"{tile.file}{tile.rank}" for tile in moves}
        self.assertNotIn("d5", names)
        self.assertNotIn("d6", names)
        self.assertNotIn("c3", names)
        self.assertIn("f6", names)
        self.assertNotIn("g7", names)


class KnightTest(ChessTestCase):
    def test_knight_reaches_eight_squares_from_the_centre(self):
        game = position("Nd4", "")
        self.assertMovesEqual(game, "d4", "b3 b5 c2 c6 e2 e6 f3 f5")

    def test_knight_in_a_corner_reaches_two_squares(self):
        game = position("Na1", "")
        self.assertMovesEqual(game, "a1", "b3 c2")

    def test_knight_jumps_over_pieces_but_not_onto_friends(self):
        game = position("Nb1 a2 b2 c2 d2", "")
        self.assertMovesEqual(game, "b1", "a3 c3")

    def test_knight_may_capture_on_its_landing_square(self):
        game = position("Nb1", "d2")
        self.assertMovesEqual(game, "b1", "a3 c3 d2")


class KingTest(ChessTestCase):
    def test_king_reaches_eight_neighbours(self):
        game = position("Kd4", "")
        self.assertMovesEqual(game, "d4", "c3 c4 c5 d3 d5 e3 e4 e5")

    def test_king_on_the_home_square(self):
        game = position("Ke1", "")
        self.assertMovesEqual(game, "e1", "d1 d2 e2 f1 f2")

    def test_king_in_a_corner(self):
        game = position("Ka1", "")
        self.assertMovesEqual(game, "a1", "a2 b1 b2")

    def test_king_cannot_step_onto_a_friendly_piece(self):
        game = position("Ke1 d1 d2 e2 f2", "")
        self.assertMovesEqual(game, "e1", "f1")

    def test_king_may_capture_an_adjacent_enemy(self):
        game = position("Ke1", "Qe2")
        self.assertMovesEqual(game, "e1", "d1 d2 e2 f1 f2")


class PawnTest(ChessTestCase):
    def test_white_pawn_may_step_once_or_twice_from_home(self):
        game = position("e2", "")
        self.assertMovesEqual(game, "e2", "e3 e4")

    def test_black_pawn_moves_down_the_board(self):
        game = position("", "e7")
        self.assertMovesEqual(game, "e7", "e6 e5")

    def test_pawn_that_has_already_moved_takes_a_single_step(self):
        game = position("e3", "")
        mark_moved(piece_at(game, "e3"))
        self.assertMovesEqual(game, "e3", "e4")

    def test_pawn_directly_blocked_cannot_move_at_all(self):
        game = position("e2", "Ne3")
        self.assertMovesEqual(game, "e2", "")

    def test_pawn_cannot_jump_over_a_piece_on_its_double_step(self):
        game = position("e2", "Ne4")
        self.assertMovesEqual(game, "e2", "e3")

    def test_pawn_captures_diagonally_forward(self):
        game = position("e4", "d5 f5")
        mark_moved(piece_at(game, "e4"))
        self.assertMovesEqual(game, "e4", "e5 d5 f5")

    def test_pawn_does_not_capture_a_friendly_piece(self):
        game = position("e4 d5 f5", "")
        mark_moved(piece_at(game, "e4"))
        self.assertMovesEqual(game, "e4", "e5")

    def test_pawn_does_not_capture_straight_ahead(self):
        game = position("e4", "Ne5")
        mark_moved(piece_at(game, "e4"))
        self.assertMovesEqual(game, "e4", "")

    def test_pawn_does_not_capture_backwards(self):
        game = position("e4", "d3 f3")
        mark_moved(piece_at(game, "e4"))
        self.assertMovesEqual(game, "e4", "e5")

    def test_edge_pawn_has_only_one_capture_diagonal(self):
        game = position("a4", "b5")
        mark_moved(piece_at(game, "a4"))
        self.assertMovesEqual(game, "a4", "a5 b5")

    def test_black_pawn_captures_downwards(self):
        game = position("c4 e4", "d5")
        mark_moved(piece_at(game, "d5"))
        self.assertMovesEqual(game, "d5", "d4 c4 e4")


class PieceIdentityTest(ChessTestCase):
    def test_pieces_know_their_colour_and_name(self):
        game = position("Ke1 Qd1 Ra1 Bc1 Nb1 e2", "Ke8")
        expected = {
            "e1": ("King", WHITE),
            "d1": ("Queen", WHITE),
            "a1": ("Rook", WHITE),
            "c1": ("Bishop", WHITE),
            "b1": ("Knight", WHITE),
            "e2": ("Pawn", WHITE),
            "e8": ("King", BLACK),
        }
        for square, (name, color) in expected.items():
            self.assertOccupied(game, square, name, color)

    def test_white_and_black_pieces_use_different_icons(self):
        game = position("Ke1", "Ke8")
        self.assertNotEqual(piece_at(game, "e1").icon, piece_at(game, "e8").icon)

    def test_pawn_direction_depends_on_colour(self):
        game = position("e2", "e7")
        self.assertEqual(piece_at(game, "e2").direction, 1)
        self.assertEqual(piece_at(game, "e7").direction, -1)


if __name__ == "__main__":
    unittest.main()
