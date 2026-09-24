import { type RequestState, useRequest } from "../hooks/useRequest";
import { explainDeviation, explainMistake } from "../lib/api";
import { ANNOTATION, moveLabel } from "../lib/format";
import type { FlaggedMove, Game } from "../lib/models";
import type { ReplayMove } from "../lib/pgnReplay";

function Explanation({ state }: { state: RequestState<string> }) {
  if (state.phase === "loading") return <p>Generating explanation...</p>;
  if (state.phase === "done") return <p>{state.data}</p>;

  return <p>Explanation unavailable.</p>;
}

export function DeviationCallout({ game, move }: { game: Game; move: ReplayMove }) {
  const bookMoves = game.book_moves ?? [];
  const deviation = {
    fen: move.fenBefore,
    played_san: move.san,
    book_moves: bookMoves,
    opening_name: game.opening_name,
    game_result: game.game_result,
  };

  const [explanation] = useRequest(deviation, explainDeviation);

  return (
    <div>
      <p>
        <strong>Left book here.</strong>
      </p>
      <p>
        Played <strong>{move.san}</strong>; book plays{" "}
        {bookMoves.length > 0 ? bookMoves.map((m) => m.san).join(", ") : "(no book moves recorded)"}
      </p>
      <Explanation state={explanation} />
    </div>
  );
}

export function MistakeCallout({ move }: { move: FlaggedMove }) {
  const [explanation] = useRequest(move, explainMistake);
  const label = move.classification === "blunder" ? "Blunder" : "Mistake";

  return (
    <div>
      <p>
        <strong className={move.classification}>{label}:</strong> {moveLabel(move.ply, move.played_san)}
        {ANNOTATION[move.classification]} Better was <strong>{moveLabel(move.ply, move.best_san)}</strong>
      </p>
      <p>Engine line: {move.best_line.join(" ")}</p>
      <Explanation state={explanation} />
    </div>
  );
}
