import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { AuthProvider } from '../contexts/AuthContext';
import apiClient from '../api/client';
import BoardPage from '../pages/BoardPage';

vi.mock('../api/client', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
    interceptors: {
      request: { use: vi.fn() },
      response: { use: vi.fn() },
    },
  },
}));

const mockBoard = { id: 1, title: 'My Board', owner_id: 1 };
const mockColumns = [
  { id: 1, title: 'To Do', position: 0, board_id: 1 },
  { id: 2, title: 'Done', position: 1, board_id: 1 },
];
const mockCardsCol1 = [
  { id: 1, title: 'Task 1', description: '', position: 0, column_id: 1 },
];
const mockCardsCol2: typeof mockCardsCol1 = [];

function renderBoardPage() {
  return render(
    <MemoryRouter initialEntries={['/board/1']}>
      <AuthProvider>
        <Routes>
          <Route path="/board/:id" element={<BoardPage />} />
        </Routes>
      </AuthProvider>
    </MemoryRouter>,
  );
}

function setupMocks() {
  vi.mocked(apiClient.get).mockImplementation((url: string) => {
    if (url === '/boards/1') return Promise.resolve({ data: mockBoard });
    if (url === '/boards/1/columns')
      return Promise.resolve({ data: mockColumns });
    if (url === '/columns/1/cards')
      return Promise.resolve({ data: mockCardsCol1 });
    if (url === '/columns/2/cards')
      return Promise.resolve({ data: mockCardsCol2 });
    return Promise.reject(new Error('not found'));
  });
}

describe('BoardPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('shows loading state initially', () => {
    vi.mocked(apiClient.get).mockResolvedValue({ data: mockBoard });
    renderBoardPage();
    expect(screen.getByText('Loading board...')).toBeInTheDocument();
  });

  it('renders board title after loading', async () => {
    setupMocks();
    renderBoardPage();

    await waitFor(() => {
      expect(screen.getByText('My Board')).toBeInTheDocument();
    });
  });

  it('renders columns after loading', async () => {
    setupMocks();
    renderBoardPage();

    await waitFor(() => {
      expect(screen.getByText('To Do')).toBeInTheDocument();
    });
    await waitFor(() => {
      expect(screen.getByText('Done')).toBeInTheDocument();
    });
  });

  it('renders cards inside columns', async () => {
    setupMocks();
    renderBoardPage();

    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });
  });

  it('shows new column button', async () => {
    setupMocks();
    renderBoardPage();

    await waitFor(() => {
      expect(screen.getByText('+ New Column')).toBeInTheDocument();
    });
  });

  it('shows back button', async () => {
    setupMocks();
    renderBoardPage();

    await waitFor(() => {
      expect(screen.getByText('←')).toBeInTheDocument();
    });
  });

  it('shows error on load failure', async () => {
    vi.mocked(apiClient.get).mockRejectedValue({
      response: { data: { detail: 'Board not found' } },
    });

    renderBoardPage();

    await waitFor(() => {
      expect(screen.getByText('Board not found')).toBeInTheDocument();
    });
  });
});
