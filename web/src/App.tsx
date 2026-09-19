import { Chessboard } from "react-chessboard";
import { Controls } from "./components/Controls";
import { StatusBanner } from "./components/StatusBanner";
import { useChessGame } from "./hooks/useChessGame";
import { buildSquareStyles } from "./lib/squareStyles";
import "./App.css";

function App() {
  const chessGame = useChessGame();

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
      </div>
    </div>
  );
}

export default App;
