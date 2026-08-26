"""Checkmate, stalemate, and the three ways out of a check.

``Game`` has no single "is checkmate" call: the game loop derives it from
``is_in_check`` plus ``has_any_legal_move``.  These tests exercise that pair
directly through the ``assertCheckmate`` / ``assertStalemate`` helpers.
"""

import unittest

from tests.helpers import BLACK, WHITE, ChessTestCase, play, position, standard_game


class CheckmateTest(ChessTestCase):
    def test_fools_mate(self):
        """1. f3 e5 2. g4 Qh4# - the fastest mate in chess."""
        game = standard_game()
        play(game, "f3", "e5", "g4", "Qh4")
        self.assertCheckmate(game, WHITE)
        self.assertPlayable(game, BLACK)

    def test_scholars_mate_position(self):
        """Qf7#, propped up by the bishop on c4, with the king boxed in."""
        game = position(
            "Ke1 Qf7 Bc4 Ng1 Nb1 Ra1 Rh1 a2 b2 c2 d2 e4 f2 g2 h2",
            "Ke8 Qd8 Bc8 Bf8 Nc6 Nf6 Ra8 Rh8 a7 b7 c7 d7 e5 g7 h7",
            turn=BLACK,
        )
        self.assertCheckmate(game, BLACK)

    def test_back_rank_mate(self):
        """The king is walled in by its own pawns and the rook sweeps the rank."""
        game = position("Kg1 Ra8 f2 g2 h2", "Kg8 f7 g7 h7", turn=BLACK)
        self.assertCheckmate(game, BLACK)

    def test_back_rank_mate_covers_the_square_behind_the_king(self):
        """h8 only becomes attacked once the king vacates g8 - an x-ray escape."""
        game = position("Kg1 Ra8 f2 g2 h2", "Kg8 f7 g7 h7", turn=BLACK)
        h8 = game.board.get_tile("h", 8)
        self.assertFalse(
            game.is_attacked(h8, WHITE),
            "h8 is shielded by the king, so it is not attacked yet",
        )
        self.assertCheckmate(game, BLACK)  # ...but it is still not an escape

    def test_back_rank_check_is_not_mate_when_a_luft_exists(self):
        """The same position with h7 pushed: the king simply steps up to h7."""
        game = position("Kg1 Ra8 f2 g2 h2", "Kg8 f7 g7 h6", turn=BLACK)
        self.assertTrue(game.is_in_check(BLACK))
        self.assertPlayable(game, BLACK)

    def test_smothered_mate(self):
        """The knight checks from f7; every flight square is blocked by friends."""
        game = position("Kg1 Nf7 a2", "Kh8 Rg8 g7 h7", turn=BLACK)
        self.assertCheckmate(game, BLACK)

    def test_queen_and_king_mate_on_the_edge(self):
        game = position("Ke6 Qe7", "Ke8", turn=BLACK)
        self.assertCheckmate(game, BLACK)

    def test_two_rooks_ladder_mate(self):
        """Ra1 checks along the first rank while Rb2 fences off the second."""
        game = position("Kc5 Ra1 Rb2", "Kh1", turn=BLACK)
        self.assertCheckmate(game, BLACK)

    def test_white_can_be_mated_too(self):
        """Qxf2#, defended by the bishop on c5 - mate detection is colour-blind."""
        game = position(
            "Ke1 Qd1 Ra1 Rh1 Bc1 Bf1 Nb1 Ng1 a2 b2 c2 d2 e4 g2 h2",
            "Ke8 Qf2 Bc5",
            turn=WHITE,
        )
        self.assertCheckmate(game, WHITE)


class EscapingCheckTest(ChessTestCase):
    """A check is only mate when none of capture, block or flight is available."""

    def test_check_escaped_by_moving_the_king(self):
        game = position("Ke1 Re7", "Ke5", turn=BLACK)
        self.assertTrue(game.is_in_check(BLACK))
        self.assertPlayable(game, BLACK)

    def test_check_escaped_by_capturing_the_checker(self):
        """The undefended queen gives check next to the king and is simply taken."""
        game = position("Ka1 Qd8", "Ke7", turn=BLACK)
        self.assertTrue(game.is_in_check(BLACK))
        self.assertPlayable(game, BLACK)

    def test_check_escaped_by_blocking_the_line(self):
        """Every flight square is taken, so only the knight interposing on e7 saves it."""
        game = position("Ka1 Re1", "Ke8 Rd8 Rf8 Nd5 d7 f7", turn=BLACK)
        self.assertTrue(game.is_in_check(BLACK))
        self.assertPlayable(game, BLACK)

    def test_interposing_on_e7_actually_clears_the_check(self):
        game = position("Ka1 Re1", "Ke8 Rd8 Rf8 Nd5 d7 f7", turn=BLACK)
        game.move_piece(game.board.get_tile("d", 5), game.board.get_tile("e", 7))
        self.assertFalse(game.is_in_check(BLACK))

    def test_blocking_piece_removed_turns_the_same_check_into_mate(self):
        """Same position without the knight: nothing can reach the e-file."""
        game = position("Ka1 Re1", "Ke8 Rd8 Rf8 d7 f7", turn=BLACK)
        self.assertCheckmate(game, BLACK)

    def test_double_check_cannot_be_blocked_or_captured(self):
        """Re1 and Bh5 both check; one interposition cannot stop two lines."""
        game = position("Ka1 Re1 Bh5", "Ke8 Rd8 Rf8 Nd5 d7", turn=BLACK)
        self.assertTrue(game.is_in_check(BLACK))
        self.assertCheckmate(game, BLACK)


class StalemateTest(ChessTestCase):
    def test_classic_king_and_queen_stalemate(self):
        """Qg6 takes every flight square but never touches h8."""
        game = position("Kf7 Qg6", "Kh8", turn=BLACK)
        self.assertStalemate(game, BLACK)

    def test_cornered_king_stalemated_by_a_queen(self):
        game = position("Ka1", "Ke8 Qc2", turn=WHITE)
        self.assertStalemate(game, WHITE)

    def test_stalemate_breaks_once_the_side_to_move_has_a_spare_piece(self):
        """Adding a free pawn turns the same stalemate into an ordinary position."""
        game = position("Ka1 h2", "Ke8 Qc2", turn=WHITE)
        self.assertFalse(game.is_in_check(WHITE))
        self.assertPlayable(game, WHITE)

    def test_blocked_pawn_does_not_rescue_a_stalemate(self):
        """The extra pawn is frozen by an enemy pawn, so White is still stuck."""
        game = position("Ka1 a2", "Ke8 Qc2 a3", turn=WHITE)
        self.assertStalemate(game, WHITE)


class LegalMoveSearchTest(ChessTestCase):
    """``has_any_legal_move`` must leave the board exactly as it found it."""

    def test_search_restores_the_position(self):
        game = position("Kg1 Ra8 f2 g2 h2", "Kg8 f7 g7 h7", turn=BLACK)
        before = {
            f"{tile.file}{tile.rank}": tile.piece
            for row in game.board.board
            for tile in row
        }
        pieces_before = list(game.pieces)

        game.has_any_legal_move(BLACK)

        after = {
            f"{tile.file}{tile.rank}": tile.piece
            for row in game.board.board
            for tile in row
        }
        self.assertEqual(before, after, "the mate search left the board disturbed")
        self.assertEqual(pieces_before, game.pieces)
        self.assertEqual(game.graveyard, [])

    def test_search_restores_move_history(self):
        game = position("Kg1 Ra8 f2 g2 h2", "Kg8 f7 g7 h7", turn=BLACK)
        history = {piece: len(piece.past_tiles) for piece in game.pieces}

        game.has_any_legal_move(BLACK)

        for piece, length in history.items():
            self.assertEqual(len(piece.past_tiles), length)

    def test_a_side_with_only_a_trapped_king_reports_no_moves(self):
        game = position("Kf7 Qg6", "Kh8", turn=BLACK)
        self.assertFalse(game.has_any_legal_move(BLACK))
        self.assertTrue(game.has_any_legal_move(WHITE))


if __name__ == "__main__":
    unittest.main()
