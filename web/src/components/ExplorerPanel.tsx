import type { ExplorerState } from "../hooks/useExplorer";

interface ExplorerPanelProps {
  state: ExplorerState;
  onPlayMove: (uci: string) => void;
  onRetry: () => void;
}

export function ExplorerPanel({ state, onPlayMove, onRetry }: ExplorerPanelProps) {
  if (state.status === "loading") {
    return <div className="explorer-panel">Loading book moves…</div>;
  }

  if (state.status === "error") {
    return (
      <div className="explorer-panel">
        <p>Couldn't load book moves ({state.message}).</p>
        <button onClick={onRetry}>Retry</button>
      </div>
    );
  }

  const { moves } = state.result;

  if (moves.length === 0) {
    return <div className="explorer-panel">No book data for this position.</div>;
  }

  return (
    <div className="explorer-panel">
      {moves.map((move) => (
        <button key={move.uci} className="explorer-move" onClick={() => onPlayMove(move.uci)}>
          <span className="explorer-move-san">{move.san}</span>
          <span className="explorer-move-games">{move.games.toLocaleString()} games</span>
          <div className="explorer-move-bar">
            <div className="bar-white" style={{ width: `${move.whiteWinPct}%` }} />
            <div className="bar-draw" style={{ width: `${move.drawPct}%` }} />
            <div className="bar-black" style={{ width: `${move.blackWinPct}%` }} />
          </div>
        </button>
      ))}
    </div>
  );
}
