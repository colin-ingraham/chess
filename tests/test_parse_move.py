"""Notation parsing and legality filtering in ``Game.parse_move``.

``parse_move`` is the whole rules gate: it resolves algebraic notation to a
piece, applies the move, and rolls it back if the mover's own king would be
left in check.  It returns ``True`` when the move stuck and ``False`` otherwise.

Only the notation the parser supports today is exercised here.  Captures
written as ``exd5`` / ``Nxe5``, check marks (``+``, ``#``), castling (``O-O``),
promotion suffixes (``=Q``) and file/rank disambiguation are all still open
items in todo.txt, so they are deliberately left untested.
"""

import unittest

from tests.helpers import (
    BLACK,
    WHITE,
    ChessTestCase,
    piece_at,
    position,
    set_turn,
    square_tile,
    standard_game,
)


class AcceptedMovesTest(ChessTestCase):
    def setUp(self):
        self.game = standard_game()

    def test_pawn_double_step(self):
        self.assertTrue(self.game.parse_move("e4"))
        self.assertEmpty(self.game, "e2")
        self.assertOccupied(self.game, "e4", "Pawn", WHITE)

    def test_pawn_single_step(self):
        self.assertTrue(self.game.parse_move("e3"))
        self.assertEmpty(self.game, "e2")
        self.assertOccupied(self.game, "e3", "Pawn", WHITE)

    def test_knight_development(self):
        self.assertTrue(self.game.parse_move("Nf3"))
        self.assertEmpty(self.game, "g1")
        self.assertOccupied(self.game, "f3", "Knight", WHITE)

    def test_the_other_knight_is_chosen_for_the_other_square(self):
        self.assertTrue(self.game.parse_move("Nc3"))
        self.assertEmpty(self.game, "b1")
        self.assertOccupied(self.game, "c3", "Knight", WHITE)

    def test_black_moves_when_it_is_black_to_play(self):
        set_turn(self.game, BLACK)
        self.assertTrue(self.game.parse_move("e5"))
        self.assertEmpty(self.game, "e7")
        self.assertOccupied(self.game, "e5", "Pawn", BLACK)

    def test_parsing_does_not_change_whose_turn_it_is(self):
        """Turn order belongs to the game loop, not to the parser."""
        self.assertTrue(self.game.parse_move("e4"))
        self.assertEqual(self.game.current_player.color, WHITE)

    def test_bishop_queen_rook_and_king_letters_are_understood(self):
        game = position("Ke1 Qd4 Ra1 Bc1", "Ke8")
        self.assertTrue(game.parse_move("Qd7"))
        self.assertTrue(game.parse_move("Ra5"))
        self.assertTrue(game.parse_move("Bf4"))
        self.assertTrue(game.parse_move("Ke2"))
        self.assertOccupied(game, "d7", "Queen", WHITE)
        self.assertOccupied(game, "a5", "Rook", WHITE)
        self.assertOccupied(game, "f4", "Bishop", WHITE)
        self.assertOccupied(game, "e2", "King", WHITE)

    def test_a_capture_written_as_a_plain_destination_is_accepted(self):
        """``exd5`` is not supported yet (todo.txt); ``d5`` reaches the same move."""
        game = standard_game()
        game.parse_move("e4")
        set_turn(game, BLACK)
        game.parse_move("d5")
        set_turn(game, WHITE)
        victim = piece_at(game, "d5")

        self.assertTrue(game.parse_move("d5"))
        self.assertOccupied(game, "d5", "Pawn", WHITE)
        self.assertIn(victim, game.graveyard)
        self.assertNotIn(victim, game.pieces)


class RejectedMovesTest(ChessTestCase):
    def snapshot(self, game):
        return {
            f"{tile.file}{tile.rank}": tile.piece
            for row in game.board.board
            for tile in row
        }

    def assertRejected(self, game, notation):
        before = self.snapshot(game)
        self.assertFalse(game.parse_move(notation), f"{notation} should be rejected")
        self.assertEqual(
            self.snapshot(game), before, f"{notation} disturbed the board"
        )

    def test_pawn_cannot_reach_a_distant_square(self):
        self.assertRejected(standard_game(), "e5")

    def test_a_player_cannot_move_the_opponents_piece(self):
        """White to move: e5 is only reachable by Black's e7 pawn."""
        game = standard_game()
        self.assertEqual(game.current_player.color, WHITE)
        self.assertRejected(game, "e5")

    def test_knight_cannot_reach_an_unrelated_square(self):
        self.assertRejected(standard_game(), "Nd5")

    def test_blocked_back_rank_pieces_cannot_move_at_the_start(self):
        game = standard_game()
        for notation in ("Bc4", "Qd4", "Ra3", "Ke2"):
            self.assertRejected(game, notation)

    def test_squares_off_the_board_are_rejected(self):
        self.assertRejected(standard_game(), "e9")

    def test_a_move_that_leaves_the_king_in_check_is_rejected(self):
        """The knight on e2 is pinned to e1 by the rook on e8."""
        game = position("Ke1 Ne2", "Kh8 Re8")
        self.assertRejected(game, "Nc3")

    def test_the_pinned_piece_may_still_move_along_the_pin(self):
        game = position("Ke1 Re2", "Kh8 Re8")
        self.assertTrue(game.parse_move("Re5"))
        self.assertOccupied(game, "e5", "Rook", WHITE)

    def test_the_king_cannot_walk_into_check(self):
        game = position("Ke1", "Kh8 Rd8")
        self.assertRejected(game, "Kd1")
        self.assertRejected(game, "Kd2")

    def test_the_king_cannot_stay_in_check_by_moving_something_else(self):
        game = position("Ke1 Ra1", "Kh8 Re8")
        self.assertTrue(game.is_in_check(WHITE))
        self.assertRejected(game, "Ra5")

    def test_a_rejected_move_leaves_move_history_intact(self):
        game = position("Ke1 Ne2", "Kh8 Re8")
        knight = piece_at(game, "e2")
        history = list(knight.past_tiles)

        game.parse_move("Nc3")

        self.assertEqual(knight.past_tiles, history)
        self.assertIs(knight.tile, square_tile(game, "e2"))


class CheckEvasionThroughTheParserTest(ChessTestCase):
    """Getting out of check has to go through ``parse_move`` like any other move."""

    def setUp(self):
        # Rook on e8 checks the White king down the open e-file.
        self.game = position("Ke1 Nd5 Rh1", "Kh8 Re8")
        self.assertTrue(self.game.is_in_check(WHITE))

    def test_stepping_out_of_the_line_is_accepted(self):
        self.assertTrue(self.game.parse_move("Kd1"))
        self.assertFalse(self.game.is_in_check(WHITE))

    def test_interposing_is_accepted(self):
        self.assertTrue(self.game.parse_move("Ne3"))
        self.assertFalse(self.game.is_in_check(WHITE))

    def test_an_unrelated_move_is_rejected(self):
        self.assertFalse(self.game.parse_move("Rh5"))
        self.assertTrue(self.game.is_in_check(WHITE))


if __name__ == "__main__":
    unittest.main()
