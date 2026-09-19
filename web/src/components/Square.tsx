import { useMemo } from "react";
import { BOARD_DARK_COLOR, BOARD_LIGHT_COLOR, LEGAL_TARGET_COLOR, SELECTED_HIGHLIGHT_COLOR } from "../lib/pieceTheme";

interface SquareProps {
  square: string;
  position: [number, number, number];
  isLight: boolean;
  isSelected: boolean;
  isLegalTarget: boolean;
  onClick: (square: string) => void;
}

export function Square({ square, position, isLight, isSelected, isLegalTarget, onClick }: SquareProps) {
  const color = useMemo(() => {
    if (isSelected) return SELECTED_HIGHLIGHT_COLOR;
    return isLight ? BOARD_LIGHT_COLOR : BOARD_DARK_COLOR;
  }, [isLight, isSelected]);

  return (
    <group>
      <mesh
        position={position}
        receiveShadow
        onClick={(event) => {
          event.stopPropagation();
          onClick(square);
        }}
      >
        <boxGeometry args={[1, 0.1, 1]} />
        <meshStandardMaterial color={color} />
      </mesh>
      {isLegalTarget && (
        <mesh position={[position[0], position[1] + 0.06, position[2]]}>
          <cylinderGeometry args={[0.15, 0.15, 0.02, 24]} />
          <meshStandardMaterial color={LEGAL_TARGET_COLOR} />
        </mesh>
      )}
    </group>
  );
}
