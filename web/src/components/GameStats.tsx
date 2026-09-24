import { type RequestState, useRequest } from "../hooks/useRequest";
import { getPositionStats } from "../lib/api";
import { formatShare, moveLabel, summarizeMistakes } from "../lib/format";
import type { FlaggedMove, Game } from "../lib/models";
import type { ReplayMove } from "../lib/pgnReplay";

type GameStatsProps = {
  game: Game;
  moves: ReplayMove[];
  fen: string;
  nextMove: string | undefined;
  analysis: RequestState<FlaggedMove[]>;
};

export function GameStats({ game, moves, fen, nextMove, analysis }: GameStatsProps) {
  const [positionStats] = useRequest(fen, getPositionStats);
  const deviationMove = game.deviation_ply !== null ? moves[game.deviation_ply - 1] : undefined;

  return (
    <aside className="game-stats">
      <h3>Game</h3>
      <table>
        <tbody>
          <tr>
            <td>Opening</td>
            <td>{game.opening_name ?? "Unknown"}</td>
          </tr>
          <tr>
            <td>Result</td>
            <td>{game.game_result}</td>
          </tr>
          <tr>
            <td>Length</td>
            <td>{Math.ceil(moves.length / 2)} moves</td>
          </tr>
          <tr>
            <td>Left book</td>
            <td>{deviationMove ? moveLabel(deviationMove.ply, deviationMove.san) : "Never"}</td>
          </tr>
          {analysis.phase === "done" && (
            <>
              <tr>
                <td>White</td>
                <td>{summarizeMistakes(analysis.data, "white")}</td>
              </tr>
              <tr>
                <td>Black</td>
                <td>{summarizeMistakes(analysis.data, "black")}</td>
              </tr>
            </>
          )}
        </tbody>
      </table>
      {analysis.phase === "loading" && <p>Analyzing with Stockfish...</p>}
      {analysis.phase === "error" && <p>Engine analysis unavailable.</p>}

      <h3>Moves from this position</h3>
      {positionStats.phase === "loading" && <p>Loading...</p>}
      {positionStats.phase === "error" && <p>Stats unavailable.</p>}
      {positionStats.phase === "done" && positionStats.data.total_games === 0 && <p>No Lichess games.</p>}
      {positionStats.phase === "done" && positionStats.data.total_games > 0 && (
        <table>
          <thead>
            <tr>
              <th>Move</th>
              <th>Games</th>
              <th>Share</th>
            </tr>
          </thead>
          <tbody>
            {positionStats.data.moves.map((move) => (
              <tr key={move.uci} className={move.san === nextMove ? "played" : undefined}>
                <td>{move.san}</td>
                <td>{move.games.toLocaleString()}</td>
                <td>{formatShare(move.share)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </aside>
  );
}
