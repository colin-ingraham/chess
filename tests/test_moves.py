"""Applying and reverting moves: ``move_piece``, ``undo_move``, ``destroy_piece``.

``has_any_legal_move`` explores the whole move tree by making and unmaking
moves, so undo has to restore the board *exactly* - including the order of
``Game.pieces``, which is what ``t_index`` in the move record is for.
"""

import unittest

from tests.helpers import (
    BLACK,
    WHITE,
    ChessTestCase,
    move,
    piece_at,
    position,
    square_tile,
    standard_game,
)


class MovePieceTest(ChessTestCase):
    def test_quiet_move_updates_both_tiles_and_the_piece(self):
        game = position("Ke1 Ra1", "Ke8")
        rook = piece_at(game, "a1")
        move(game, "a1", "a5")

        self.assertEmpty(game, "a1")
        self.assertIs(piece_at(game, "a5"), rook)
        self.assertIs(rook.tile, square_tile(game, "a5"))

    def test_quiet_move_records_the_previous_square(self):
        game = position("Ke1 Ra1", "Ke8")
        rook = piece_at(game, "a1")
        move(game, "a1", "a5")

        self.assertEqual(len(rook.past_tiles), 2)
        self.assertIs(rook.past_tiles[-1], square_tile(game, "a1"))

    def test_quiet_move_leaves_the_piece_list_untouched(self):
        game = position("Ke1 Ra1", "Ke8")
        before = list(game.pieces)
        move(game, "a1", "a5")

        self.assertEqual(game.pieces, before)
        self.assertEqual(game.graveyard, [])

    def test_capture_sends_the_victim_to_the_graveyard(self):
        game = position("Ke1 Ra1", "Ke8 Ra8")
        victim = piece_at(game, "a8")
        capturer = piece_at(game, "a1")
        move(game, "a1", "a8")

        self.assertIs(piece_at(game, "a8"), capturer)
        self.assertNotIn(victim, game.pieces)
        self.assertEqual(game.graveyard, [victim])
        self.assertIsNone(victim.tile)
        self.assertEqual(len(game.pieces), 3)

    def test_move_record_describes_the_move(self):
        game = position("Ke1 Ra1", "Ke8 Ra8")
        victim = piece_at(game, "a8")
        capturer = piece_at(game, "a1")
        record = move(game, "a1", "a8")

        self.assertIs(record["piece"], capturer)
        self.assertIs(record["t_piece"], victim)
        self.assertIs(record["st"], square_tile(game, "a1"))
        self.assertIs(record["tt"], square_tile(game, "a8"))
        self.assertIsNotNone(record["t_index"])

    def test_quiet_move_record_has_no_victim(self):
        game = position("Ke1 Ra1", "Ke8")
        record = move(game, "a1", "a5")

        self.assertIsNone(record["t_piece"])
        self.assertIsNone(record["t_index"])


class UndoMoveTest(ChessTestCase):
    def snapshot(self, game):
        return {
            "squares": {
                f"{tile.file}{tile.rank}": tile.piece
                for row in game.board.board
                for tile in row
            },
            "pieces": list(game.pieces),
            "graveyard": list(game.graveyard),
            "tiles": {piece: piece.tile for piece in game.pieces},
            "history": {piece: list(piece.past_tiles) for piece in game.pieces},
        }

    def assertRestored(self, game, before):
        self.assertEqual(self.snapshot(game), before)

    def test_undoing_a_quiet_move_restores_everything(self):
        game = position("Ke1 Ra1 Nb1", "Ke8 Ra8")
        before = self.snapshot(game)
        game.undo_move(move(game, "a1", "a5"))
        self.assertRestored(game, before)

    def test_undoing_a_capture_restores_everything(self):
        game = position("Ke1 Ra1 Nb1", "Ke8 Ra8")
        before = self.snapshot(game)
        game.undo_move(move(game, "a1", "a8"))
        self.assertRestored(game, before)

    def test_undo_puts_the_captured_piece_back_at_its_old_index(self):
        """``t_index`` exists so the piece list keeps a stable order."""
        game = position("Ke1 Ra1", "Ke8 Ra8 Nb8 Bc8")
        victim = piece_at(game, "b8")
        index_before = game.pieces.index(victim)

        game.undo_move(move(game, "a1", "b8"))

        self.assertEqual(game.pieces.index(victim), index_before)

    def test_undo_revives_the_captured_piece(self):
        game = position("Ke1 Ra1", "Ke8 Ra8")
        victim = piece_at(game, "a8")
        game.undo_move(move(game, "a1", "a8"))

        self.assertIn(victim, game.pieces)
        self.assertNotIn(victim, game.graveyard)
        self.assertIs(victim.tile, square_tile(game, "a8"))
        self.assertIs(piece_at(game, "a8"), victim)

    def test_repeated_make_and_unmake_does_not_drift(self):
        game = standard_game()
        before = self.snapshot(game)
        for _ in range(5):
            game.undo_move(move(game, "g1", "f3"))
        self.assertRestored(game, before)

    def test_undo_restores_a_full_capture_sequence_in_reverse(self):
        game = position("Ke1 Ra1 Rh1", "Ke8 Ra8 Rh8")
        before = self.snapshot(game)
        first = move(game, "a1", "a8")
        second = move(game, "h1", "h8")

        game.undo_move(second)
        game.undo_move(first)

        self.assertRestored(game, before)


class DestroyPieceTest(ChessTestCase):
    def test_destroyed_pieces_leave_the_roster_for_the_graveyard(self):
        game = position("Ke1 Ra1", "Ke8")
        rook = piece_at(game, "a1")
        game.destroy_piece(rook)

        self.assertNotIn(rook, game.pieces)
        self.assertIn(rook, game.graveyard)
        self.assertIsNone(rook.tile)

    def test_a_destroyed_piece_no_longer_attacks(self):
        game = position("Ke1 Ra1", "Ke8")
        game.destroy_piece(piece_at(game, "a1"))
        self.assertFalse(game.is_attacked(square_tile(game, "a5"), WHITE))


class EnemyColorTest(ChessTestCase):
    def test_colours_are_opposites(self):
        game = position("Ke1", "Ke8")
        self.assertEqual(game.enemy_color(WHITE), BLACK)
        self.assertEqual(game.enemy_color(BLACK), WHITE)


if __name__ == "__main__":
    unittest.main()
