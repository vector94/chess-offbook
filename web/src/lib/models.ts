// These types use the same snake_case names as the api JSON, so no conversion is needed.

export type GameResult = "win" | "draw" | "loss";

export type BookMove = { san: string; uci: string; games: number; share: number };

export type Game = {
  found: true;
  chesscom_id: string;
  pgn: string;
  opening_name: string | null;
  played_at: string;
  game_result: GameResult;
  deviation_ply: number | null;
  book_moves: BookMove[] | null;
};

export type LatestGame = { found: false } | Game;
