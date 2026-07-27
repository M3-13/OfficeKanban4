import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider } from '../contexts/AuthContext';

vi.mock('../api/boards', () => ({
  fetchBoards: vi.fn(),
  createBoard: vi.fn(),
  updateBoard: vi.fn(),
  deleteBoard: vi.fn(),
}));

import BoardListPage from './BoardListPage';
import { fetchBoards, createBoard, updateBoard, deleteBoard } from '../api/boards';

function renderWithProviders() {
  localStorage.setItem('token', 'fake-token');
  localStorage.setItem('user', JSON.stringify({ id: 1, username: 'testuser' }));

  return render(
    <MemoryRouter>
      <AuthProvider>
        <BoardListPage />
      </AuthProvider>
    </MemoryRouter>,
  );
}

describe('BoardListPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('shows loading state initially', () => {
    vi.mocked(fetchBoards).mockReturnValue(new Promise(() => {}));
    renderWithProviders();
    expect(screen.getByText('Laden...')).toBeInTheDocument();
  });

  it('shows empty message when no boards exist', async () => {
    vi.mocked(fetchBoards).mockResolvedValue([]);
    renderWithProviders();
    await waitFor(() => {
      expect(screen.getByText(/Keine Boards vorhanden/)).toBeInTheDocument();
    });
  });

  it('renders board list', async () => {
    vi.mocked(fetchBoards).mockResolvedValue([
      { id: 1, title: 'Alpha Board', owner_id: 1 },
      { id: 2, title: 'Beta Board', owner_id: 1 },
    ]);
    renderWithProviders();
    await waitFor(() => {
      expect(screen.getByText('Alpha Board')).toBeInTheDocument();
    });
    expect(screen.getByText('Beta Board')).toBeInTheDocument();
  });

  it('creates a new board', async () => {
    vi.mocked(fetchBoards).mockResolvedValue([]);
    vi.mocked(createBoard).mockResolvedValue({ id: 3, title: 'New Board', owner_id: 1 });
    const user = userEvent.setup();
    renderWithProviders();

    await waitFor(() => {
      expect(screen.getByPlaceholderText('Neues Board...')).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText('Neues Board...');
    await user.type(input, 'New Board');
    await user.click(screen.getByText('Neues Board'));

    expect(createBoard).toHaveBeenCalledWith('New Board');
  });

  it('renames a board', async () => {
    vi.mocked(fetchBoards).mockResolvedValue([
      { id: 1, title: 'Old Name', owner_id: 1 },
    ]);
    vi.mocked(updateBoard).mockResolvedValue({ id: 1, title: 'New Name', owner_id: 1 });
    const user = userEvent.setup();
    renderWithProviders();

    await waitFor(() => {
      expect(screen.getByText('Umbenennen')).toBeInTheDocument();
    });

    await user.click(screen.getByText('Umbenennen'));

    const editInput = screen.getByDisplayValue('Old Name');
    await user.clear(editInput);
    await user.type(editInput, 'New Name');
    await user.click(screen.getByText('Speichern'));

    expect(updateBoard).toHaveBeenCalledWith(1, 'New Name');
  });

  it('deletes a board after confirmation', async () => {
    vi.mocked(fetchBoards).mockResolvedValue([
      { id: 1, title: 'To Delete', owner_id: 1 },
    ]);
    vi.mocked(deleteBoard).mockResolvedValue(undefined);
    const confirmSpy = vi.spyOn(window, 'confirm').mockReturnValue(true);
    const user = userEvent.setup();
    renderWithProviders();

    await waitFor(() => {
      expect(screen.getByText('Löschen')).toBeInTheDocument();
    });

    await user.click(screen.getByText('Löschen'));

    expect(confirmSpy).toHaveBeenCalled();
    expect(deleteBoard).toHaveBeenCalledWith(1);
    confirmSpy.mockRestore();
  });

  it('shows error message on fetch failure', async () => {
    vi.mocked(fetchBoards).mockRejectedValue(new Error('Network error'));
    renderWithProviders();
    await waitFor(() => {
      expect(screen.getByText('Fehler beim Laden der Boards')).toBeInTheDocument();
    });
  });
});
