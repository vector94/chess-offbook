import type { CSSProperties } from "react";

const SELECTED_STYLE: CSSProperties = {
  backgroundColor: "rgba(255, 255, 0, 0.4)",
};

const LEGAL_TARGET_STYLE: CSSProperties = {
  backgroundImage:
    "radial-gradient(circle, rgba(0,0,0,0.25) 19%, transparent 20%)",
  backgroundSize: "100% 100%",
  backgroundPosition: "center",
  backgroundRepeat: "no-repeat",
};

export function buildSquareStyles(
  selectedSquare: string | null,
  legalTargets: string[],
): Record<string, CSSProperties> {
  const styles: Record<string, CSSProperties> = {};

  if (selectedSquare) {
    styles[selectedSquare] = SELECTED_STYLE;
  }

  for (const square of legalTargets) {
    styles[square] = LEGAL_TARGET_STYLE;
  }

  return styles;
}
