import { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  DndContext,
  DragEndEvent,
  PointerSensor,
  closestCenter,
  useSensor,
  useSensors,
} from '@dnd-kit/core';
import type { Board, Card, Column } from '../types';
import apiClient from '../api/client';
import { useAuth } from '../contexts/AuthContext';
import ColumnLane from '../components/ColumnLane';

export default function BoardPage() {
  const { id } = useParams<{ id: string }>();
  const boardId = Number(id);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [board, setBoard] = useState<Board | null>(null);
  const [columns, setColumns] = useState<Column[]>([]);
  const [cardsByColumn, setCardsByColumn] = useState<Record<number, Card[]>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newColumnTitle, setNewColumnTitle] = useState('');
  const [addingColumn, setAddingColumn] = useState(false);

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } }),
  );

  const loadBoard = useCallback(async () => {
    try {
      const [boardRes, colsRes] = await Promise.all([
        apiClient.get(`/boards/${boardId}`),
        apiClient.get(`/boards/${boardId}/columns`),
      ]);
      setBoard(boardRes.data);
      const cols: Column[] = colsRes.data;
      setColumns(cols);

      const cardsMap: Record<number, Card[]> = {};
      const cardPromises = cols.map((col) =>
        apiClient.get(`/columns/${col.id}/cards`).then((r) => {
          cardsMap[col.id] = r.data;
        }),
      );
      await Promise.all(cardPromises);
      setCardsByColumn(cardsMap);
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail || 'Failed to load board';
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, [boardId]);

  useEffect(() => {
    loadBoard();
  }, [loadBoard]);

  const handleDragEnd = useCallback(
    (event: DragEndEvent) => {
      const { active, over } = event;
      if (!over) return;

      const activeCardId = active.id as number;
      let targetColumnId: number;
      let targetIndex: number;

      if (typeof over.id === 'string' && over.id.startsWith('col-')) {
        targetColumnId = parseInt(over.id.slice(4), 10);
        targetIndex = (cardsByColumn[targetColumnId] || []).length;
      } else {
        const overCardId = over.id as number;
        let found: Card | undefined;
        for (const colCards of Object.values(cardsByColumn)) {
          found = colCards.find((c) => c.id === overCardId);
          if (found) break;
        }
        if (!found) return;
        targetColumnId = found.column_id;
        targetIndex = (cardsByColumn[targetColumnId] || []).findIndex(
          (c) => c.id === overCardId,
        );
        if (targetIndex === -1) targetIndex = 0;
      }

      let activeCard: Card | undefined;
      let sourceColumnId = 0;
      for (const [colId, colCards] of Object.entries(cardsByColumn)) {
        activeCard = colCards.find((c) => c.id === activeCardId);
        if (activeCard) {
          sourceColumnId = Number(colId);
          break;
        }
      }
      if (!activeCard) return;

      const sourceIndex = (cardsByColumn[sourceColumnId] || []).findIndex(
        (c) => c.id === activeCardId,
      );
      if (
        sourceColumnId === targetColumnId &&
        sourceIndex === targetIndex
      ) {
        return;
      }

      const prevState = JSON.parse(JSON.stringify(cardsByColumn));

      setCardsByColumn((prev) => {
        const updated = { ...prev };
        updated[sourceColumnId] = (updated[sourceColumnId] || []).filter(
          (c) => c.id !== activeCardId,
        );
        const targetCards = [...(updated[targetColumnId] || [])];
        const movedCard = { ...activeCard!, column_id: targetColumnId };
        const insertAt = Math.min(targetIndex, targetCards.length);
        targetCards.splice(insertAt, 0, movedCard);
        updated[targetColumnId] = targetCards;
        return updated;
      });

      apiClient
        .put(`/cards/${activeCardId}/move`, {
          column_id: targetColumnId,
          position: targetIndex,
        })
        .catch(() => {
          setCardsByColumn(prevState);
          setError('Failed to move card. Reverted.');
        });
    },
    [cardsByColumn],
  );

  const handleColumnTitleChange = useCallback(
    (columnId: number, title: string) => {
      setColumns((prev) =>
        prev.map((c) => (c.id === columnId ? { ...c, title } : c)),
      );
    },
    [],
  );

  const handleColumnDelete = useCallback(
    (columnId: number) => {
      setColumns((prev) => prev.filter((c) => c.id !== columnId));
      setCardsByColumn((prev) => {
        const updated = { ...prev };
        delete updated[columnId];
        return updated;
      });
    },
    [],
  );

  const handleCardCreate = useCallback(
    (_columnId: number, _card: Card) => {
      loadBoard();
    },
    [loadBoard],
  );

  const handleCardUpdate = useCallback(
    (cardId: number, data: { title?: string; description?: string }) => {
      setCardsByColumn((prev) => {
        const updated = { ...prev };
        for (const colId of Object.keys(updated)) {
          updated[Number(colId)] = updated[Number(colId)].map((c) =>
            c.id === cardId ? { ...c, ...data } : c,
          );
        }
        return updated;
      });
    },
    [],
  );

  const handleCardDelete = useCallback((cardId: number) => {
    setCardsByColumn((prev) => {
      const updated = { ...prev };
      for (const colId of Object.keys(updated)) {
        updated[Number(colId)] = updated[Number(colId)].filter(
          (c) => c.id !== cardId,
        );
      }
      return updated;
    });
  }, []);

  const handleAddColumn = async () => {
    const trimmed = newColumnTitle.trim();
    if (!trimmed) return;
    setAddingColumn(true);
    setError('');
    try {
      const r = await apiClient.post(`/boards/${boardId}/columns`, {
        title: trimmed,
      });
      setColumns((prev) => [...prev, r.data]);
      setCardsByColumn((prev) => ({ ...prev, [r.data.id]: [] }));
      setNewColumnTitle('');
    } catch {
      setError('Failed to create column');
    } finally {
      setAddingColumn(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <header className="topbar">
          <h1 className="topbar-title">
            <button className="btn-back" onClick={() => navigate('/')}>
              &larr;
            </button>{' '}
            Loading...
          </h1>
          <div className="topbar-user">
            <span>{user?.username}</span>
            <button className="btn-secondary btn-sm" onClick={logout}>
              Logout
            </button>
          </div>
        </header>
        <main className="content">
          <p className="empty-message">Loading board...</p>
        </main>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="topbar">
        <h1 className="topbar-title">
          <button className="btn-back" onClick={() => navigate('/')}>
            &larr;
          </button>{' '}
          {board?.title || `Board ${boardId}`}
        </h1>
        <div className="topbar-user">
          <span>{user?.username}</span>
          <button className="btn-secondary btn-sm" onClick={logout}>
            Logout
          </button>
        </div>
      </header>

      <main className="board-content">
        {error && <div className="board-error">{error}</div>}

        <DndContext
          sensors={sensors}
          collisionDetection={closestCenter}
          onDragEnd={handleDragEnd}
        >
          <div className="board-lanes">
            {columns.map((column) => (
              <ColumnLane
                key={column.id}
                column={column}
                cards={cardsByColumn[column.id] || []}
                onTitleChange={handleColumnTitleChange}
                onDelete={handleColumnDelete}
                onCardCreate={handleCardCreate}
                onCardUpdate={handleCardUpdate}
                onCardDelete={handleCardDelete}
              />
            ))}

            <div className="column-lane column-lane--new">
              {addingColumn ? (
                <div className="column-lane__add-form">
                  <input
                    className="column-lane__add-input"
                    value={newColumnTitle}
                    onChange={(e) => setNewColumnTitle(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') handleAddColumn();
                      if (e.key === 'Escape') {
                        setAddingColumn(false);
                        setNewColumnTitle('');
                      }
                    }}
                    placeholder="Column name..."
                    autoFocus
                    maxLength={100}
                  />
                  <div className="column-lane__add-actions">
                    <button
                      className="btn-primary btn-sm"
                      onClick={handleAddColumn}
                    >
                      Add
                    </button>
                    <button
                      className="btn-secondary btn-sm"
                      onClick={() => {
                        setAddingColumn(false);
                        setNewColumnTitle('');
                      }}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <button
                  className="column-lane__add-btn column-lane__add-btn--new"
                  onClick={() => setAddingColumn(true)}
                >
                  + New Column
                </button>
              )}
            </div>
          </div>
        </DndContext>
      </main>
    </div>
  );
}
