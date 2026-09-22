import { useEffect, useState } from "react";

export type RequestState<T> =
  | { phase: "loading" }
  | { phase: "error"; message: string }
  | { phase: "done"; data: T };

// Calls load(input) every time input changes. A null input means there is nothing to load.
export function useRequest<I, T>(input: I | null, load: (input: I) => Promise<T>) {
  const [state, setState] = useState<RequestState<T>>({ phase: "loading" });
  const [attempt, setAttempt] = useState(0);

  const key = JSON.stringify(input);

  useEffect(() => {
    if (input === null) return;

    // if the input changes before the answer comes, the old answer is ignored
    let cancelled = false;

    setState({ phase: "loading" });
    load(input)
      .then((data) => {
        if (!cancelled) setState({ phase: "done", data });
      })
      .catch((error: Error) => {
        if (!cancelled) setState({ phase: "error", message: error.message });
      });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key, attempt]);

  const retry = () => setAttempt((n) => n + 1);

  return [state, retry] as const;
}
