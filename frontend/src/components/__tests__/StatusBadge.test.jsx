import { render, screen } from '@testing-library/react';
import StatusBadge from '../common/StatusBadge';
import { setActiveMessages } from '../../i18n';

beforeAll(() => {
  setActiveMessages({
    'status.confirmed': 'Confirme',
    'status.cancelled': 'Annule',
    'status.pending': 'En attente',
  });
});

describe('StatusBadge', () => {
  it('renders the translated status label', () => {
    render(<StatusBadge status="confirmed" />);
    expect(screen.getByText('Confirme')).toBeInTheDocument();
  });

  it('applies the correct style for confirmed status', () => {
    render(<StatusBadge status="confirmed" />);
    const badge = screen.getByText('Confirme');
    expect(badge.className).toContain('bg-green-100');
  });

  it('falls back to gray for unknown statuses', () => {
    render(<StatusBadge status="unknown" />);
    const badge = screen.getByText('status.unknown');
    expect(badge.className).toContain('bg-gray-100');
  });
});
