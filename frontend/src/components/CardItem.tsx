import { useState } from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import type { Card } from '../types';
import apiClient from '../api/client';
import InlineEdit from './InlineEdit';

interface CardItemProps {
  card: Card;
  onUpdate: (id: number, data: { title?: string; description?: string }) => void;
  onDelete: (id: number) => void;
}

export default function CardItem({ card, onUpdate, onDelete }: CardItemProps) {
  const [expanded, setExpanded] = useState(false);
  const [editingDesc, setEditingDesc] = useState(false);
  const [descDraft, setDescDraft] = useState(card.description || '');
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState('');

  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: card.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.6 : 1,
    cursor: isDragging ? 'grabbing' : 'grab',
  };

  const handleTitleSave = async (title: string) => {
    const prev = card.title;
    try {
      onUpdate(card.id, { title });
      await apiClient.put(`/cards/${card.id}`, { title });
    } catch {
      onUpdate(card.id, { title: prev });
      setError('Failed to save title');
    }
  };

  const handleDescSave = async () => {
    const trimmed = descDraft.trim();
    const prev = card.description;
    try {
      onUpdate(card.id, { description: trimmed });
      await apiClient.put(`/cards/${card.id}`, { description: trimmed });
      setEditingDesc(false);
    } catch {
      onUpdate(card.id, { description: prev });
      setError('Failed to save description');
    }
  };

  const handleDelete = async () => {
    setDeleting(true);
    try {
      await apiClient.delete(`/cards/${card.id}`);
      onDelete(card.id);
    } catch {
      setDeleting(false);
      setError('Failed to delete card');
    }
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`card-item${isDragging ? ' card-item--dragging' : ''}`}
      {...attributes}
    >
      <div className="card-item__header">
        <span className="card-item__drag-handle" {...listeners}>
          &#x2630;
        </span>
        <InlineEdit
          value={card.title}
          onSave={handleTitleSave}
          className="card-item__title"
        />
        <button
          className="btn-icon btn-icon--danger"
          onClick={handleDelete}
          disabled={deleting}
          title="Delete card"
          aria-label="Delete card"
        >
          &#x2715;
        </button>
      </div>

      {!expanded && card.description && (
        <p
          className="card-item__desc-preview"
          onClick={() => {
            setExpanded(true);
            setDescDraft(card.description);
          }}
        >
          {card.description.slice(0, 80)}
          {card.description.length > 80 ? '...' : ''}
        </p>
      )}

      {expanded && (
        <div className="card-item__desc">
          {editingDesc ? (
            <textarea
              className="card-item__desc-textarea"
              value={descDraft}
              onChange={(e) => setDescDraft(e.target.value)}
              onBlur={handleDescSave}
              autoFocus
              rows={3}
            />
          ) : (
            <p
              onClick={() => {
                setEditingDesc(true);
                setDescDraft(card.description || '');
              }}
              className="card-item__desc-text"
            >
              {card.description || 'Add description...'}
            </p>
          )}
          <button
            className="btn-sm-text"
            onClick={() => setExpanded(false)}
          >
            Collapse
          </button>
        </div>
      )}

      {!expanded && !card.description && (
        <button
          className="card-item__add-desc"
          onClick={() => {
            setExpanded(true);
            setEditingDesc(true);
            setDescDraft('');
          }}
        >
          + Add description
        </button>
      )}

      {error && <div className="card-item__error">{error}</div>}
    </div>
  );
}
