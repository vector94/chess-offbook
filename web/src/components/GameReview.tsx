import { DEFAULT_POSITION } from "chess.js";
import { useMemo, useState } from "react";
import { Chessboard } from "react-chessboard";
import { useRequest } from "../hooks/useRequest";
import { getGameAnalysis } from "../lib/api";
import { ANNOTATION } from "../lib/format";
import type { Game } from "../lib/models";
import { replayPgn } from "../lib/pgnReplay";
import { DeviationCallout, MistakeCallout } from "./Callouts";
import { GameStats } from "./GameStats";

export function GameReview({ game }: { game: Game }) {
  const moves = useMemo(() => replayPgn(game.pgn), [game.pgn]);

  // the board shows the position after this many half moves
  const [currentPly, setCurrentPly] = useState(game.deviation_ply ?? 0);

  const [analysis] = useRequest(game.pgn, getGameAnalysis);
  const flaggedMoves = analysis.phase === "done" ? analysis.data : [];
  const flaggedByPly = new Map(flaggedMoves.map((move) => [move.ply, move]));
  const currentMistake = flaggedByPly.get(currentPly);

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
        {deviationMove && currentPly === deviationMove.ply && <DeviationCallout game={game} move={deviationMove} />}
        {currentMistake && <MistakeCallout move={currentMistake} />}
        {game.deviation_ply === null && <p>Stayed in book the whole game.</p>}

        <ol className="move-list">
          {moves.map((move) => {
            const flagged = flaggedByPly.get(move.ply);
            const className = move.ply === currentPly ? "current" : move.ply === game.deviation_ply ? "deviation" : "";

            return (
              <li key={move.ply} className={className} onClick={() => setCurrentPly(move.ply)}>
                {move.color === "w" ? `${Math.ceil(move.ply / 2)}. ` : ""}
                {move.san}
                {flagged && <span className={flagged.classification}>{ANNOTATION[flagged.classification]}</span>}
              </li>
            );
          })}
        </ol>
      </div>

      <GameStats game={game} moves={moves} fen={position} nextMove={moves[currentPly]?.san} analysis={analysis} />
    </div>
  );
}
