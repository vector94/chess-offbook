import { type RequestState, useRequest } from "../hooks/useRequest";
import { explainDeviation } from "../lib/api";
import type { Game } from "../lib/models";
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
