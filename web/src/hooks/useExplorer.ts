import { useEffect, useState } from "react";
import { fetchExplorer } from "../lib/explorerApi";
import type { ExplorerResult } from "../types";

export type ExplorerState =
  | { status: "loading" }
  | { status: "ready"; result: ExplorerResult }
  | { status: "error"; message: string };

export function useExplorer(fen: string): { state: ExplorerState; retry: () => void } {
  const [state, setState] = useState<ExplorerState>({ status: "loading" });
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading" });

    fetchExplorer(fen)
      .then((result) => {
        if (!cancelled) setState({ status: "ready", result });
      })
      .catch((error: Error) => {
        if (!cancelled) setState({ status: "error", message: error.message });
      });

    return () => {
      cancelled = true;
    };
  }, [fen, attempt]);

  function retry() {
    setAttempt((current) => current + 1);
  }

  return { state, retry };
}
