import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { DndContext, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import type { Column, Card } from '../types';
import ColumnLane from './ColumnLane';

function DndWrapper({ children }: { children: React.ReactNode }) {
  const sensors = useSensors(useSensor(PointerSensor));
  return <DndContext sensors={sensors}>{children}</DndContext>;
}

const mockColumn: Column = {
  id: 1,
  title: 'To Do',
  position: 0,
  board_id: 1,
};

const mockCards: Card[] = [
  { id: 1, title: 'Card A', description: '', position: 0, column_id: 1 },
  { id: 2, title: 'Card B', description: '', position: 1, column_id: 1 },
];

describe('ColumnLane', () => {
  it('renders column title', () => {
    render(
      <DndWrapper>
        <ColumnLane
          column={mockColumn}
          cards={[]}
          onTitleChange={vi.fn()}
          onDelete={vi.fn()}
          onCardCreate={vi.fn()}
          onCardUpdate={vi.fn()}
          onCardDelete={vi.fn()}
        />
      </DndWrapper>,
    );
    expect(screen.getByText('To Do')).toBeInTheDocument();
  });

  it('renders cards in the column', () => {
    render(
      <DndWrapper>
        <ColumnLane
          column={mockColumn}
          cards={mockCards}
          onTitleChange={vi.fn()}
          onDelete={vi.fn()}
          onCardCreate={vi.fn()}
          onCardUpdate={vi.fn()}
          onCardDelete={vi.fn()}
        />
      </DndWrapper>,
    );
    expect(screen.getByText('Card A')).toBeInTheDocument();
    expect(screen.getByText('Card B')).toBeInTheDocument();
  });

  it('shows empty state when no cards', () => {
    render(
      <DndWrapper>
        <ColumnLane
          column={mockColumn}
          cards={[]}
          onTitleChange={vi.fn()}
          onDelete={vi.fn()}
          onCardCreate={vi.fn()}
          onCardUpdate={vi.fn()}
          onCardDelete={vi.fn()}
        />
      </DndWrapper>,
    );
    expect(screen.getByText('No cards yet')).toBeInTheDocument();
  });

  it('renders add card button', () => {
    render(
      <DndWrapper>
        <ColumnLane
          column={mockColumn}
          cards={[]}
          onTitleChange={vi.fn()}
          onDelete={vi.fn()}
          onCardCreate={vi.fn()}
          onCardUpdate={vi.fn()}
          onCardDelete={vi.fn()}
        />
      </DndWrapper>,
    );
    expect(screen.getByText('+ Add card')).toBeInTheDocument();
  });

  it('renders delete column button', () => {
    render(
      <DndWrapper>
        <ColumnLane
          column={mockColumn}
          cards={[]}
          onTitleChange={vi.fn()}
          onDelete={vi.fn()}
          onCardCreate={vi.fn()}
          onCardUpdate={vi.fn()}
          onCardDelete={vi.fn()}
        />
      </DndWrapper>,
    );
    expect(screen.getByLabelText('Delete column')).toBeInTheDocument();
  });
});
