import { Board3D } from "./components/Board3D";
import "./App.css";

const START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

function App() {
  return (
    <div className="app">
      <Board3D
        fen={START_FEN}
        orientation="white"
        selectedSquare={null}
        legalTargets={[]}
        onSquareClick={() => {}}
      />
    </div>
  );
}

export default App;
