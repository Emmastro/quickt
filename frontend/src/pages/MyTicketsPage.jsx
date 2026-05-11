import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Ticket, Clock, QrCode } from 'lucide-react';
import { t } from '../i18n';
import { useMyTickets } from '../hooks/useTickets';
import { formatXOF, formatTime } from '../utils/format';
import StatusBadge from '../components/common/StatusBadge';

const TABS = [
  { key: 'upcoming', statuses: ['reserved', 'confirmed'] },
  { key: 'past', statuses: ['used', 'completed'] },
  { key: 'cancelled', statuses: ['cancelled', 'expired'] },
];

export default function MyTicketsPage() {
  const [activeTab, setActiveTab] = useState('upcoming');
  const { data, isLoading } = useMyTickets();

  const tickets = data?.items || [];
  const activeStatuses = TABS.find((tab) => tab.key === activeTab)?.statuses || [];
  const filtered = tickets.filter((ticket) => activeStatuses.includes(ticket.status));

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-primary-200 border-t-primary-700" />
      </div>
    );
  }

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      <h1 className="text-xl font-bold text-gray-900 mb-5">{t('ticket.my_tickets')}</h1>

      {/* Tabs */}
      <div className="flex gap-1 bg-gray-100 rounded-xl p-1 mb-5">
        {TABS.map(({ key }) => (
          <button
            key={key}
            onClick={() => setActiveTab(key)}
            className={`flex-1 py-2 text-sm font-medium rounded-lg transition-colors ${
              activeTab === key
                ? 'bg-white text-primary-700 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {t(`ticket.${key}`)}
          </button>
        ))}
      </div>

      {/* Ticket list */}
      {filtered.length === 0 ? (
        <div className="card p-8 text-center">
          <Ticket className="w-10 h-10 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500">{t('ticket.no_tickets')}</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((ticket) => (
            <Link
              key={ticket.id}
              to={`/app/tickets/${ticket.id}`}
              className="ticket-card p-4 block hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="font-mono text-sm font-bold text-primary-700">{ticket.code}</div>
                <StatusBadge status={ticket.status} />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm text-gray-900 font-medium">{ticket.passenger_name}</div>
                  <div className="text-xs text-gray-500">
                    {t('ticket.seat')}: {ticket.seat_number}
                  </div>
                </div>
                <PriceDisplay amount={ticket.price} />
              </div>

              <div className="flex items-center gap-3 mt-2 pt-2 border-t border-gray-100 text-xs text-gray-400">
                <span>Ref: {ticket.booking_reference}</span>
                {ticket.status === 'confirmed' && (
                  <span className="flex items-center gap-1 text-green-600">
                    <QrCode className="w-3 h-3" />
                    QR
                  </span>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

function PriceDisplay({ amount }) {
  return <span className="font-bold text-primary-700">{formatXOF(amount)}</span>;
}
