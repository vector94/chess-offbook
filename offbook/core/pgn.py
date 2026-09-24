import io
from dataclasses import dataclass

import chess
import chess.pgn


@dataclass
class PlyMove:
    ply: int
    side_to_move: str
    fen_before: str
    san: str
    uci: str


def replay_moves(pgn_text: str) -> list[PlyMove]:
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    if game is None:
        raise ValueError("no game found in PGN")

    board = game.board()
    plies = []
    for ply, move in enumerate(game.mainline_moves(), start=1):
        plies.append(
            PlyMove(
                ply=ply,
                side_to_move="white" if board.turn == chess.WHITE else "black",
                fen_before=board.fen(),
                san=board.san(move),
                uci=move.uci(),
            )
        )
        board.push(move)

    return plies
