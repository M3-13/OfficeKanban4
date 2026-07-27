import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { DndContext, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import type { Card } from '../types';
import CardItem from './CardItem';

function DndWrapper({ children }: { children: React.ReactNode }) {
  const sensors = useSensors(useSensor(PointerSensor));
  return (
    <DndContext sensors={sensors}>
      <SortableContext items={[1]} strategy={verticalListSortingStrategy}>
        {children}
      </SortableContext>
    </DndContext>
  );
}

const mockCard: Card = {
  id: 1,
  title: 'Test Card',
  description: 'A test description',
  position: 0,
  column_id: 1,
};

describe('CardItem', () => {
  it('renders card title', () => {
    render(
      <DndWrapper>
        <CardItem
          card={mockCard}
          onUpdate={vi.fn()}
          onDelete={vi.fn()}
        />
      </DndWrapper>,
    );
    expect(screen.getByText('Test Card')).toBeInTheDocument();
  });

  it('shows description preview', () => {
    render(
      <DndWrapper>
        <CardItem
          card={mockCard}
          onUpdate={vi.fn()}
          onDelete={vi.fn()}
        />
      </DndWrapper>,
    );
    expect(screen.getByText(/A test description/)).toBeInTheDocument();
  });

  it('shows add description for cards without description', () => {
    const cardNoDesc: Card = { ...mockCard, description: '' };
    render(
      <DndWrapper>
        <CardItem
          card={cardNoDesc}
          onUpdate={vi.fn()}
          onDelete={vi.fn()}
        />
      </DndWrapper>,
    );
    expect(screen.getByText('+ Add description')).toBeInTheDocument();
  });

  it('renders delete button', () => {
    render(
      <DndWrapper>
        <CardItem
          card={mockCard}
          onUpdate={vi.fn()}
          onDelete={vi.fn()}
        />
      </DndWrapper>,
    );
    expect(screen.getByLabelText('Delete card')).toBeInTheDocument();
  });

  it('renders drag handle', () => {
    render(
      <DndWrapper>
        <CardItem
          card={mockCard}
          onUpdate={vi.fn()}
          onDelete={vi.fn()}
        />
      </DndWrapper>,
    );
    const handle = screen.getByText('☰');
    expect(handle).toBeInTheDocument();
    expect(handle).toHaveClass('card-item__drag-handle');
  });
});
