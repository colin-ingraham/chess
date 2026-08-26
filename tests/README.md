# Test suite

Plain `unittest` — no dependencies to install. Run everything from the repo root:

```
python -m unittest discover          # or: venv/Scripts/python.exe -m unittest discover
python -m unittest discover -v       # per-test names
python -m unittest tests.test_checkmate               # one module
python -m unittest tests.test_checkmate.StalemateTest # one class
```

## Layout

| File | Covers |
| --- | --- |
| `helpers.py` | Headless `Game` construction, position building, custom assertions |
| `test_setup.py` | The starting position: placement, counts, board/piece consistency |
| `test_checkmate.py` | Checkmate, stalemate, and the three escapes from check |
| `test_check.py` | `is_attacked` / `is_in_check` per piece type |
| `test_pieces.py` | `possible_moves` for each piece, including blockers and edges |
| `test_moves.py` | `move_piece` / `undo_move` / `destroy_piece` state handling |
| `test_parse_move.py` | Notation parsing and the "may not leave the king in check" gate |

## Writing a new test

`Game.__init__` prints a board and then blocks on `input()`, so tests never call
it. `helpers.position()` builds a game directly from placement strings:

```python
game = position("Kg1 Ra8 f2 g2 h2", "Kg8 f7 g7 h7", turn=BLACK)
self.assertCheckmate(game, BLACK)
```

White pieces first, then Black. A token is a piece letter plus a square
(`Qd1`, `Nf3`); a bare square is a pawn (`e2`). Include both kings whenever the
test touches check detection — `is_in_check` looks the king up unconditionally.

`ChessTestCase` adds `assertCheckmate`, `assertStalemate`, `assertPlayable`,
`assertMovesEqual`, `assertOccupied` and `assertEmpty`, all of which report
square names rather than object reprs.

## Deliberately not covered

Unimplemented features from `todo.txt` are out of scope: castling, en passant,
promotion, draw conditions, move disambiguation, FEN, clocks. Notation the
parser does not accept yet (`exd5`, `Nxe5`, `+`, `#`, `O-O`, `=Q`) is not
tested either.

Two tests are marked `@unittest.expectedFailure` because they pin down real
bugs that are *not* on the todo list — inverted `Tile.color`, and a rook scored
at 6 points in `calculate_diff`. A green run reports them as "expected
failures"; when either bug is fixed the decorator should be removed.
