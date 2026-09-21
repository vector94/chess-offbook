import { DEFAULT_POSITION } from "chess.js";
import { useMemo, useState } from "react";
import { Chessboard } from "react-chessboard";
import type { Game } from "../lib/models";
import { replayPgn } from "../lib/pgnReplay";

export function GameReview({ game }: { game: Game }) {
  const moves = useMemo(() => replayPgn(game.pgn), [game.pgn]);

  // the board shows the position after this many half moves
  const [currentPly, setCurrentPly] = useState(game.deviation_ply ?? 0);

  const deviationMove = game.deviation_ply !== null ? moves[game.deviation_ply - 1] : undefined;

  const position = currentPly === 0 ? DEFAULT_POSITION : moves[currentPly - 1].fenAfter;
  const atStart = currentPly === 0;
  const atEnd = currentPly === moves.length;

  const goBack = () => setCurrentPly((ply) => Math.max(0, ply - 1));
  const goForward = () => setCurrentPly((ply) => Math.min(moves.length, ply + 1));

  return (
    <div className="game-review">
      <div className="game-review-board">
        <Chessboard options={{ position, allowDragging: false }} />
        <div className="game-review-controls">
          <button type="button" onClick={() => setCurrentPly(0)} disabled={atStart}>
            {"|<"}
          </button>
          <button type="button" onClick={goBack} disabled={atStart}>
            {"<"}
          </button>
          <button type="button" onClick={goForward} disabled={atEnd}>
            {">"}
          </button>
          <button type="button" onClick={() => setCurrentPly(moves.length)} disabled={atEnd}>
            {">|"}
          </button>
        </div>
      </div>

      <div className="game-review-info">
        <p>
          <strong>{game.opening_name ?? "Unknown opening"}</strong>, {game.game_result}
        </p>

        {deviationMove && currentPly === deviationMove.ply && (
          <div>
            <p>
              <strong>Left book here.</strong>
            </p>
            <p>
              Played <strong>{deviationMove.san}</strong>; book plays{" "}
              {game.book_moves && game.book_moves.length > 0
                ? game.book_moves.map((m) => m.san).join(", ")
                : "(no book moves recorded)"}
            </p>
          </div>
        )}
        {game.deviation_ply === null && <p>Stayed in book the whole game.</p>}

        <ol className="move-list">
          {moves.map((move) => {
            const className = move.ply === currentPly ? "current" : move.ply === game.deviation_ply ? "deviation" : "";

            return (
              <li key={move.ply} className={className} onClick={() => setCurrentPly(move.ply)}>
                {move.color === "w" ? `${Math.ceil(move.ply / 2)}. ` : ""}
                {move.san}
              </li>
            );
          })}
        </ol>
      </div>
    </div>
  );
}
