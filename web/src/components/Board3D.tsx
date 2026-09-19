import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { Chess } from "chess.js";
import { squareToPosition, type Orientation } from "../lib/boardGeometry";
import { Square } from "./Square";
import { Piece3D } from "./Piece3D";

interface Board3DProps {
  fen: string;
  orientation: Orientation;
  selectedSquare: string | null;
  legalTargets: string[];
  onSquareClick: (square: string) => void;
}

const FILES = ["a", "b", "c", "d", "e", "f", "g", "h"];

export function Board3D({ fen, orientation, selectedSquare, legalTargets, onSquareClick }: Board3DProps) {
  const board = new Chess(fen).board();

  const squares = [];
  for (const file of FILES) {
    for (let rank = 1; rank <= 8; rank++) {
      const square = `${file}${rank}`;
      const isLight = (FILES.indexOf(file) + rank) % 2 === 1;
      squares.push(
        <Square
          key={square}
          square={square}
          position={squareToPosition(square, orientation)}
          isLight={isLight}
          isSelected={selectedSquare === square}
          isLegalTarget={legalTargets.includes(square)}
          onClick={onSquareClick}
        />
      );
    }
  }

  const pieces = [];
  for (let rankIndex = 0; rankIndex < 8; rankIndex++) {
    for (let fileIndex = 0; fileIndex < 8; fileIndex++) {
      const cell = board[rankIndex][fileIndex];
      if (!cell) continue;
      const square = `${FILES[fileIndex]}${8 - rankIndex}`;
      const [x, , z] = squareToPosition(square, orientation);
      pieces.push(<Piece3D key={square} type={cell.type} color={cell.color} position={[x, 0.1, z]} />);
    }
  }

  return (
    <Canvas shadows camera={{ position: [0, 7, 6], fov: 45 }}>
      <ambientLight intensity={0.6} />
      <directionalLight position={[4, 8, 4]} intensity={1} castShadow />
      <OrbitControls maxPolarAngle={Math.PI / 2 - 0.05} minDistance={4} maxDistance={14} />
      {squares}
      {pieces}
    </Canvas>
  );
}
