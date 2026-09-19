import type { FC } from "react";
import type { PieceColor, PieceType } from "../types";
import { PIECE_BLACK_COLOR, PIECE_WHITE_COLOR } from "../lib/pieceTheme";

interface Piece3DProps {
  type: PieceType;
  color: PieceColor;
  position: [number, number, number];
}

const Pawn: FC<{ color: string }> = ({ color }) => (
  <group>
    <mesh position={[0, 0.06, 0]} castShadow>
      <cylinderGeometry args={[0.26, 0.3, 0.12, 20]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.3, 0]} castShadow>
      <coneGeometry args={[0.2, 0.36, 20]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.52, 0]} castShadow>
      <sphereGeometry args={[0.14, 20, 20]} />
      <meshStandardMaterial color={color} />
    </mesh>
  </group>
);

const Rook: FC<{ color: string }> = ({ color }) => (
  <group>
    <mesh position={[0, 0.07, 0]} castShadow>
      <cylinderGeometry args={[0.28, 0.32, 0.14, 20]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.35, 0]} castShadow>
      <cylinderGeometry args={[0.24, 0.26, 0.42, 20]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.6, 0]} castShadow>
      <cylinderGeometry args={[0.27, 0.24, 0.1, 8]} />
      <meshStandardMaterial color={color} />
    </mesh>
  </group>
);

const Knight: FC<{ color: string }> = ({ color }) => (
  <group>
    <mesh position={[0, 0.07, 0]} castShadow>
      <cylinderGeometry args={[0.28, 0.32, 0.14, 20]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.32, 0]} castShadow>
      <cylinderGeometry args={[0.2, 0.26, 0.36, 16]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.55, 0.05]} rotation={[0.3, 0, 0]} castShadow>
      <boxGeometry args={[0.18, 0.3, 0.32]} />
      <meshStandardMaterial color={color} />
    </mesh>
  </group>
);

const Bishop: FC<{ color: string }> = ({ color }) => (
  <group>
    <mesh position={[0, 0.07, 0]} castShadow>
      <cylinderGeometry args={[0.28, 0.32, 0.14, 20]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.36, 0]} castShadow>
      <coneGeometry args={[0.22, 0.5, 20]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.68, 0]} castShadow>
      <sphereGeometry args={[0.09, 16, 16]} />
      <meshStandardMaterial color={color} />
    </mesh>
  </group>
);

const Queen: FC<{ color: string }> = ({ color }) => (
  <group>
    <mesh position={[0, 0.08, 0]} castShadow>
      <cylinderGeometry args={[0.3, 0.34, 0.16, 20]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.42, 0]} castShadow>
      <cylinderGeometry args={[0.22, 0.28, 0.52, 20]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.72, 0]} castShadow>
      <torusGeometry args={[0.16, 0.06, 12, 24]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.84, 0]} castShadow>
      <sphereGeometry args={[0.1, 16, 16]} />
      <meshStandardMaterial color={color} />
    </mesh>
  </group>
);

const King: FC<{ color: string }> = ({ color }) => (
  <group>
    <mesh position={[0, 0.08, 0]} castShadow>
      <cylinderGeometry args={[0.3, 0.34, 0.16, 20]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.44, 0]} castShadow>
      <cylinderGeometry args={[0.22, 0.28, 0.56, 20]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.78, 0]} castShadow>
      <torusGeometry args={[0.17, 0.06, 12, 24]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.92, 0]} castShadow>
      <boxGeometry args={[0.06, 0.18, 0.06]} />
      <meshStandardMaterial color={color} />
    </mesh>
    <mesh position={[0, 0.98, 0]} castShadow>
      <boxGeometry args={[0.18, 0.06, 0.06]} />
      <meshStandardMaterial color={color} />
    </mesh>
  </group>
);

const PIECE_COMPONENTS: Record<PieceType, FC<{ color: string }>> = {
  p: Pawn,
  r: Rook,
  n: Knight,
  b: Bishop,
  q: Queen,
  k: King,
};

export function Piece3D({ type, color, position }: Piece3DProps) {
  const hex = color === "w" ? PIECE_WHITE_COLOR : PIECE_BLACK_COLOR;
  const Shape = PIECE_COMPONENTS[type];
  return (
    <group position={position}>
      <Shape color={hex} />
    </group>
  );
}
