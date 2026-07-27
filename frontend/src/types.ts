export interface User {
  id: number;
  username: string;
}

export interface Board {
  id: number;
  title: string;
  owner_id: number;
}

export interface Column {
  id: number;
  title: string;
  position: number;
  board_id: number;
}

export interface Card {
  id: number;
  title: string;
  description: string;
  position: number;
  column_id: number;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}
