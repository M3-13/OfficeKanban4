import { useState } from 'react';
import { useDroppable } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import type { Column, Card } from '../types';
import apiClient from '../api/client';
import InlineEdit from './InlineEdit';
import CardItem from './CardItem';

interface ColumnLaneProps {
  column: Column;
  cards: Card[];
  onTitleChange: (id: number, title: string) => void;
  onDelete: (id: number) => void;
  onCardCreate: (columnId: number, card: Card) => void;
  onCardUpdate: (cardId: number, data: { title?: string; description?: string }) => void;
  onCardDelete: (cardId: number) => void;
}

export default function ColumnLane({
  column,
  cards,
  onTitleChange,
  onDelete,
  onCardCreate,
  onCardUpdate,
  onCardDelete,
}: ColumnLaneProps) {
  const [newCardTitle, setNewCardTitle] = useState('');
  const [adding, setAdding] = useState(false);
  const [error, setError] = useState('');

  const { setNodeRef, isOver } = useDroppable({ id: `col-${column.id}` });

  const cardIds = cards.map((c) => c.id);

  const handleTitleSave = async (title: string) => {
    const prev = column.title;
    try {
      onTitleChange(column.id, title);
      await apiClient.put(`/boards/${column.board_id}/columns/${column.id}`, { title });
    } catch {
      onTitleChange(column.id, prev);
      setError('Failed to rename column');
    }
  };

  const handleAddCard = async () => {
    const trimmed = newCardTitle.trim();
    if (!trimmed) return;
    setAdding(true);
    setError('');
    try {
      const r = await apiClient.post(`/columns/${column.id}/cards`, {
        title: trimmed,
        description: '',
      });
      onCardCreate(column.id, r.data);
      setNewCardTitle('');
    } catch {
      setError('Failed to create card');
    } finally {
      setAdding(false);
    }
  };

  const handleDelete = async () => {
    try {
      await apiClient.delete(`/boards/${column.board_id}/columns/${column.id}`);
      onDelete(column.id);
    } catch {
      setError('Failed to delete column');
    }
  };

  return (
    <div className="column-lane">
      <div className="column-lane__header">
        <InlineEdit
          value={column.title}
          onSave={handleTitleSave}
          className="column-lane__title"
        />
        <button
          className="btn-icon btn-icon--danger"
          onClick={handleDelete}
          title="Delete column"
          aria-label="Delete column"
        >
          &#x2715;
        </button>
      </div>

      <div
        ref={setNodeRef}
        className={`column-lane__cards${isOver ? ' column-lane__cards--over' : ''}`}
      >
        <SortableContext items={cardIds} strategy={verticalListSortingStrategy}>
          {cards.map((card) => (
            <CardItem
              key={card.id}
              card={card}
              onUpdate={onCardUpdate}
              onDelete={onCardDelete}
            />
          ))}
        </SortableContext>

        {cards.length === 0 && !adding && (
          <p className="column-lane__empty">No cards yet</p>
        )}
      </div>

      <div className="column-lane__add">
        {adding ? (
          <div className="column-lane__add-form">
            <input
              className="column-lane__add-input"
              value={newCardTitle}
              onChange={(e) => setNewCardTitle(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleAddCard();
                if (e.key === 'Escape') {
                  setAdding(false);
                  setNewCardTitle('');
                }
              }}
              placeholder="Card title..."
              autoFocus
              maxLength={200}
            />
            <div className="column-lane__add-actions">
              <button className="btn-primary btn-sm" onClick={handleAddCard}>
                Add
              </button>
              <button
                className="btn-secondary btn-sm"
                onClick={() => {
                  setAdding(false);
                  setNewCardTitle('');
                }}
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <button
            className="column-lane__add-btn"
            onClick={() => setAdding(true)}
          >
            + Add card
          </button>
        )}
      </div>

      {error && <div className="column-lane__error">{error}</div>}
    </div>
  );
}
