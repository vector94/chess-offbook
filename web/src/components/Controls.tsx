interface ControlsProps {
  onReset: () => void;
  onFlip: () => void;
}

export function Controls({ onReset, onFlip }: ControlsProps) {
  return (
    <div className="controls">
      <button onClick={onReset}>Reset</button>
      <button onClick={onFlip}>Flip board</button>
    </div>
  );
}
