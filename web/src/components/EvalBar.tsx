export function EvalBar({ whiteChance }: { whiteChance: number | undefined }) {
  // a dimmed, even bar until Stockfish has answered
  const waiting = whiteChance === undefined;
  const percent = Math.round((whiteChance ?? 0.5) * 100);
  const label = waiting ? "Evaluation loading" : `White ${percent}%`;

  return (
    <div className={waiting ? "eval-bar waiting" : "eval-bar"} role="img" aria-label={label} title={label}>
      <div className="eval-bar-white" style={{ height: `${percent}%` }} />
    </div>
  );
}
