import io

import chess
import chess.engine
import chess.pgn

from offbook.models import FlaggedMove

# drops in the mover's winning chance (0 to 1), same thresholds as Lichess
MISTAKE_DROP = 0.10
BLUNDER_DROP = 0.15
LINE_LENGTH = 4


def classify(drop: float) -> str | None:
    if drop >= BLUNDER_DROP:
        return "blunder"
    if drop >= MISTAKE_DROP:
        return "mistake"
    return None


def winning_chance(board: chess.Board, info: dict | None, color: chess.Color) -> float:
    if board.is_checkmate():
        return 0.0 if board.turn == color else 1.0
    if board.is_game_over():
        return 0.5
    return info["score"].pov(color).wdl(model="lichess", ply=board.ply()).expectation()


def san_line(board: chess.Board, moves: list[chess.Move]) -> list[str]:
    board = board.copy()
    line = []
    for move in moves:
        line.append(board.san(move))
        board.push(move)
    return line


def positions_from_pgn(pgn: str) -> tuple[list[chess.Board], list[chess.Move]]:
    # every position of the game from start to end, and the moves between them
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is None or game.errors:
        raise ValueError("invalid PGN")

    board = game.board()
    boards = [board.copy()]
    moves = list(game.mainline_moves())
    for move in moves:
        board.push(move)
        boards.append(board.copy())

    return boards, moves


def analyse_positions(boards: list[chess.Board], engine: chess.engine.SimpleEngine, depth: int) -> list[dict | None]:
    # a new game id makes python-chess send ucinewgame, so nothing carries over from the last game
    game_id = object()

    analyses = []
    for board in boards:
        if board.is_game_over():
            analyses.append(None)
        else:
            analyses.append(engine.analyse(board, chess.engine.Limit(depth=depth), game=game_id))

    return analyses


def find_mistakes(pgn: str, engine: chess.engine.SimpleEngine, depth: int) -> list[FlaggedMove]:
    boards, moves = positions_from_pgn(pgn)
    analyses = analyse_positions(boards, engine, depth)

    flagged = []
    for i, move in enumerate(moves):
        before_board = boards[i]
        after_board = boards[i + 1]
        mover = before_board.turn

        before = winning_chance(before_board, analyses[i], mover)
        after = winning_chance(after_board, analyses[i + 1], mover)
        classification = classify(before - after)

        best_line = analyses[i].get("pv", [])[:LINE_LENGTH]
        if classification is None or not best_line or best_line[0] == move:
            continue

        flagged.append(
            FlaggedMove(
                ply=i + 1,
                color="white" if mover == chess.WHITE else "black",
                fen_before=before_board.fen(),
                played_san=before_board.san(move),
                classification=classification,
                best_san=before_board.san(best_line[0]),
                best_line=san_line(before_board, best_line),
                win_chance_before=round(before, 3),
                win_chance_after=round(after, 3),
            )
        )

    return flagged
