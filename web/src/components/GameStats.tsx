import { useRequest } from "../hooks/useRequest";
import { getPositionStats } from "../lib/api";
import { formatShare, moveLabel } from "../lib/format";
import type { Game } from "../lib/models";
import type { ReplayMove } from "../lib/pgnReplay";

type GameStatsProps = {
  game: Game;
  moves: ReplayMove[];
  fen: string;
  nextMove: string | undefined;
};

export function GameStats({ game, moves, fen, nextMove }: GameStatsProps) {
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
        </tbody>
      </table>

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
