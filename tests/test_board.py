"""Board geometry, tile helpers and the scoreboard maths behind ``print_board``."""

import io
import unittest
from contextlib import redirect_stdout

from board import Board, Tile
from piece import Pawn, Queen, Rook
from tests.helpers import (
    BLACK,
    WHITE,
    ChessTestCase,
    position,
    square_name,
    standard_game,
)

FILES = "abcdefgh"


class GetTileTest(ChessTestCase):
    def setUp(self):
        self.board = Board()

    def test_every_square_reports_its_own_coordinates(self):
        for file in FILES:
            for rank in range(1, 9):
                tile = self.board.get_tile(file, rank)
                self.assertEqual(square_name(tile), f"{file}{rank}")

    def test_the_grid_holds_sixty_four_distinct_tiles(self):
        tiles = [tile for row in self.board.board for tile in row]
        self.assertEqual(len(tiles), 64)
        self.assertEqual(len({id(tile) for tile in tiles}), 64)

    def test_rows_run_from_rank_eight_down_to_rank_one(self):
        self.assertIs(self.board.board[0][0], self.board.get_tile("a", 8))
        self.assertIs(self.board.board[7][0], self.board.get_tile("a", 1))
        self.assertIs(self.board.board[7][7], self.board.get_tile("h", 1))

    def test_ranks_outside_the_board_return_none(self):
        for rank in (0, 9, -1, 100):
            self.assertIsNone(self.board.get_tile("a", rank))

    def test_files_outside_the_board_return_none(self):
        for file in (chr(96), "i", "A", "z"):
            self.assertIsNone(self.board.get_tile(file, 1))

    def test_squares_alternate_colour_along_a_rank_and_a_file(self):
        for rank in range(1, 9):
            for index in range(7):
                left = self.board.get_tile(FILES[index], rank)
                right = self.board.get_tile(FILES[index + 1], rank)
                self.assertNotEqual(
                    left.color,
                    right.color,
                    f"{square_name(left)} and {square_name(right)} share a colour",
                )
        for file in FILES:
            for rank in range(1, 8):
                lower = self.board.get_tile(file, rank)
                upper = self.board.get_tile(file, rank + 1)
                self.assertNotEqual(lower.color, upper.color)

    def test_diagonally_adjacent_squares_share_a_colour(self):
        self.assertEqual(
            self.board.get_tile("a", 1).color, self.board.get_tile("b", 2).color
        )
        self.assertEqual(
            self.board.get_tile("h", 8).color, self.board.get_tile("a", 1).color
        )

    @unittest.expectedFailure
    def test_tile_colours_follow_the_light_square_on_the_right_convention(self):
        """KNOWN BUG: ``Tile.color`` is inverted.

        In chess a1 is a dark square and h1 is light.  ``Board.__init__`` flips
        the toggle before placing a8, so the whole board comes out reversed
        (a1 -> "White", h1 -> "Black").  Nothing reads ``Tile.color`` today, so
        the bug is latent, but it will surface as soon as squares are rendered.
        """
        self.assertEqual(self.board.get_tile("a", 1).color, BLACK)
        self.assertEqual(self.board.get_tile("h", 1).color, WHITE)


class FindTileTest(ChessTestCase):
    def setUp(self):
        self.board = Board()

    def test_shifts_move_right_and_up(self):
        d4 = self.board.get_tile("d", 4)
        self.assertEqual(square_name(self.board.find_tile(d4, 1, 0)), "e4")
        self.assertEqual(square_name(self.board.find_tile(d4, -1, 0)), "c4")
        self.assertEqual(square_name(self.board.find_tile(d4, 0, 1)), "d5")
        self.assertEqual(square_name(self.board.find_tile(d4, 0, -1)), "d3")
        self.assertEqual(square_name(self.board.find_tile(d4, 2, 3)), "f7")

    def test_zero_shift_returns_the_same_square(self):
        d4 = self.board.get_tile("d", 4)
        self.assertIs(self.board.find_tile(d4, 0, 0), d4)

    def test_shifts_off_the_edge_return_none(self):
        a1 = self.board.get_tile("a", 1)
        h8 = self.board.get_tile("h", 8)
        self.assertIsNone(self.board.find_tile(a1, -1, 0))
        self.assertIsNone(self.board.find_tile(a1, 0, -1))
        self.assertIsNone(self.board.find_tile(h8, 1, 0))
        self.assertIsNone(self.board.find_tile(h8, 0, 1))

    def test_files_do_not_wrap_around_the_board(self):
        """h4 shifted one to the right must not reappear on the a-file."""
        h4 = self.board.get_tile("h", 4)
        self.assertIsNone(self.board.find_tile(h4, 1, 0))
        self.assertIsNone(self.board.find_tile(h4, 1, 1))


class TileTest(ChessTestCase):
    def test_add_and_remove_piece(self):
        tile = Tile(WHITE, "e", 4)
        self.assertIsNone(tile.piece)
        pawn = Pawn(WHITE, tile)
        self.assertIs(tile.add_piece(pawn), pawn)
        self.assertIs(tile.piece, pawn)
        tile.remove_piece()
        self.assertIsNone(tile.piece)

    def test_neighbouring_files(self):
        tile = Tile(WHITE, "e", 4)
        self.assertEqual(tile.left_file(), "d")
        self.assertEqual(tile.right_file(), "f")

    def test_neighbouring_files_stop_at_the_edges(self):
        self.assertIsNone(Tile(WHITE, "a", 4).left_file())
        self.assertIsNone(Tile(WHITE, "h", 4).right_file())
        self.assertEqual(Tile(WHITE, "a", 4).right_file(), "b")
        self.assertEqual(Tile(WHITE, "h", 4).left_file(), "g")


class GraveyardTest(ChessTestCase):
    def setUp(self):
        self.board = Board()
        self.tile = self.board.get_tile("e", 4)

    def test_graveyard_is_split_by_colour(self):
        white_pawn = Pawn(WHITE, self.tile)
        black_queen = Queen(BLACK, self.tile)
        whites, blacks, print_whites, print_blacks = self.board.sort_graveyard(
            [white_pawn, black_queen]
        )
        self.assertEqual(whites, [white_pawn])
        self.assertEqual(blacks, [black_queen])
        self.assertEqual(print_whites, [white_pawn.icon])
        self.assertEqual(print_blacks, [black_queen.icon])

    def test_empty_graveyard_sorts_to_empty_lists(self):
        self.assertEqual(self.board.sort_graveyard([]), ([], [], [], []))

    def test_material_difference_favours_the_side_that_lost_less(self):
        diff, winning = self.board.calculate_diff(
            [Queen(WHITE, self.tile)], [Pawn(BLACK, self.tile)]
        )
        self.assertEqual(diff, 8)
        self.assertEqual(winning, BLACK)

    def test_material_difference_is_symmetric(self):
        diff, winning = self.board.calculate_diff(
            [Pawn(WHITE, self.tile)], [Queen(BLACK, self.tile)]
        )
        self.assertEqual(diff, 8)
        self.assertEqual(winning, WHITE)

    def test_equal_material_has_no_leader(self):
        diff, winning = self.board.calculate_diff(
            [Pawn(WHITE, self.tile)], [Pawn(BLACK, self.tile)]
        )
        self.assertEqual(diff, 0)
        self.assertEqual(winning, "None")

    @unittest.expectedFailure
    def test_rook_is_worth_five_points(self):
        """KNOWN BUG: ``calculate_diff`` scores a rook as 6 instead of 5.

        With the current table a rook plus a bishop (6 + 3) outweigh a queen
        (9), so the material readout beside the board misreports common
        endgames.
        """
        diff, _ = self.board.calculate_diff([Rook(WHITE, self.tile)], [])
        self.assertEqual(diff, 5)


class PrintBoardTest(ChessTestCase):
    def render(self, game):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            game.board.print_board(game.graveyard, game.player1, game.player2)
        return buffer.getvalue()

    def test_printing_the_opening_position_renders_all_files_and_ranks(self):
        output = self.render(standard_game())
        for rank in range(1, 9):
            self.assertIn(str(rank), output)
        self.assertIn("a  b  c  d  e  f  g  h", output)
        self.assertIn("♟", output)  # a white pawn
        self.assertIn("♔", output)  # the black king
        self.assertIn(".", output)  # empty squares in the middle

    def test_printing_shows_captured_material_for_both_players(self):
        game = position("Ke1 Ra1", "Ke8 a7")
        game.move_piece(game.board.get_tile("a", 1), game.board.get_tile("a", 7))
        output = self.render(game)

        self.assertIn(game.player1.name, output)
        self.assertIn(game.player2.name, output)
        self.assertIn("(+1)", output)


if __name__ == "__main__":
    unittest.main()
