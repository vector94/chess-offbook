// These types use the same snake_case names as the api JSON, so no conversion is needed.

export type Color = "white" | "black";

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

export type PositionStats = { total_games: number; moves: BookMove[] };

export type Deviation = {
  fen: string;
  played_san: string;
  book_moves: BookMove[];
  opening_name: string | null;
  game_result: GameResult;
};

export type FlaggedMove = {
  ply: number;
  color: Color;
  fen_before: string;
  played_san: string;
  classification: "mistake" | "blunder";
  best_san: string;
  best_line: string[];
  win_chance_before: number;
  win_chance_after: number;
};
