import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { fetchBoards, createBoard, updateBoard, deleteBoard } from '../api/boards';
import type { Board } from '../types';

export default function BoardListPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [boards, setBoards] = useState<Board[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newTitle, setNewTitle] = useState('');
  const [creating, setCreating] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState('');

  const loadBoards = useCallback(async () => {
    try {
      setError('');
      const data = await fetchBoards();
      setBoards(data);
    } catch {
      setError('Fehler beim Laden der Boards');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadBoards();
  }, [loadBoards]);

  const handleCreate = async () => {
    const trimmed = newTitle.trim();
    if (!trimmed) return;
    setCreating(true);
    setError('');
    try {
      await createBoard(trimmed);
      setNewTitle('');
      await loadBoards();
    } catch {
      setError('Fehler beim Erstellen des Boards');
    } finally {
      setCreating(false);
    }
  };

  const handleRename = async (id: number) => {
    const trimmed = editTitle.trim();
    if (!trimmed || trimmed.length > 100) return;
    setError('');
    try {
      await updateBoard(id, trimmed);
      setEditingId(null);
      setEditTitle('');
      await loadBoards();
    } catch {
      setError('Fehler beim Umbenennen des Boards');
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Board wirklich löschen?')) return;
    setError('');
    try {
      await deleteBoard(id);
      await loadBoards();
    } catch {
      setError('Fehler beim Löschen des Boards');
    }
  };

  const startEditing = (board: Board) => {
    setEditingId(board.id);
    setEditTitle(board.title);
  };

  const cancelEditing = () => {
    setEditingId(null);
    setEditTitle('');
  };

  if (loading) {
    return (
      <div className="dashboard">
        <header className="topbar">
          <h1 className="topbar-title">Boards</h1>
          <div className="topbar-user">
            <span>{user?.username}</span>
            <button className="btn-secondary btn-sm" onClick={logout}>
              Logout
            </button>
          </div>
        </header>
        <main className="content">
          <p className="empty-message">Laden...</p>
        </main>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="topbar">
        <h1 className="topbar-title">Boards</h1>
        <div className="topbar-user">
          <span>{user?.username}</span>
          <button className="btn-secondary btn-sm" onClick={logout}>
            Logout
          </button>
        </div>
      </header>
      <main className="board-list-container">
        {error && <div className="board-list-error">{error}</div>}

        <div className="board-list-create">
          <input
            className="board-list-input"
            type="text"
            placeholder="Neues Board..."
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleCreate();
            }}
            maxLength={100}
          />
          <button
            className="btn-primary board-list-create-btn"
            onClick={handleCreate}
            disabled={creating || !newTitle.trim()}
          >
            {creating ? 'Erstelle...' : 'Neues Board'}
          </button>
        </div>

        {boards.length === 0 ? (
          <p className="empty-message">
            Keine Boards vorhanden &ndash; erstelle dein erstes Board!
          </p>
        ) : (
          <ul className="board-list">
            {boards.map((board) => (
              <li key={board.id} className="board-list-item">
                {editingId === board.id ? (
                  <div className="board-list-item-edit">
                    <input
                      className="board-list-input"
                      type="text"
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') handleRename(board.id);
                        if (e.key === 'Escape') cancelEditing();
                      }}
                      maxLength={100}
                      autoFocus
                    />
                    <button
                      className="btn-secondary btn-sm"
                      onClick={() => handleRename(board.id)}
                    >
                      Speichern
                    </button>
                    <button
                      className="btn-secondary btn-sm"
                      onClick={cancelEditing}
                    >
                      Abbrechen
                    </button>
                  </div>
                ) : (
                  <div className="board-list-item-row">
                    <button
                      className="board-list-title-btn"
                      onClick={() => navigate(`/board/${board.id}`)}
                    >
                      {board.title}
                    </button>
                    <div className="board-list-actions">
                      <button
                        className="btn-secondary btn-sm"
                        onClick={() => startEditing(board)}
                      >
                        Umbenennen
                      </button>
                      <button
                        className="btn-danger btn-sm"
                        onClick={() => handleDelete(board.id)}
                      >
                        Löschen
                      </button>
                    </div>
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}
