import apiClient from './client';
import type { Board } from '../types';

export async function fetchBoards(): Promise<Board[]> {
  const res = await apiClient.get<Board[]>('/boards');
  return res.data;
}

export async function createBoard(title: string): Promise<Board> {
  const res = await apiClient.post<Board>('/boards', { title });
  return res.data;
}

export async function updateBoard(id: number, title: string): Promise<Board> {
  const res = await apiClient.put<Board>(`/boards/${id}`, { title });
  return res.data;
}

export async function deleteBoard(id: number): Promise<void> {
  await apiClient.delete(`/boards/${id}`);
}
