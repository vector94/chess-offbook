import { Chessboard } from "react-chessboard";
import { Controls } from "./components/Controls";
import { StatusBanner } from "./components/StatusBanner";
import { ExplorerPanel } from "./components/ExplorerPanel";
import { useChessGame } from "./hooks/useChessGame";
import { useExplorer } from "./hooks/useExplorer";
import { buildSquareStyles } from "./lib/squareStyles";
import "./App.css";

function App() {
  const chessGame = useChessGame();
  const explorer = useExplorer(chessGame.fen);

  return (
    <div className="app">
      <div className="board-pane">
        <div className="board-wrapper">
          <Chessboard
            options={{
              position: chessGame.fen,
              boardOrientation: chessGame.orientation,
              onPieceDrop: ({ sourceSquare, targetSquare }) =>
                targetSquare
                  ? chessGame.attemptMove(sourceSquare, targetSquare)
                  : false,
              onSquareClick: ({ square }) => chessGame.selectSquare(square),
              squareStyles: buildSquareStyles(
                chessGame.selectedSquare,
                chessGame.legalTargets,
              ),
            }}
          />
        </div>
      </div>
      <div className="sidebar">
        <StatusBanner status={chessGame.status} />
        <Controls onReset={chessGame.reset} onFlip={chessGame.flipBoard} />
        <ExplorerPanel state={explorer.state} onPlayMove={chessGame.playMove} onRetry={explorer.retry} />
      </div>
    </div>
  );
}

export default App;
