import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, QrCode, X } from 'lucide-react';
import { t } from '../i18n';
import { useTicketDetail, useCancelTicket } from '../hooks/useTickets';
import { formatXOF, formatDate, formatTime } from '../utils/format';
import StatusBadge from '../components/common/StatusBadge';
import RouteDisplay from '../components/common/RouteDisplay';

export default function TicketDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: ticket, isLoading } = useTicketDetail(id);
  const cancelMutation = useCancelTicket();
  const [showCancel, setShowCancel] = useState(false);
  const [cancelReason, setCancelReason] = useState('');

  const handleCancel = async () => {
    try {
      await cancelMutation.mutateAsync({ id: Number(id), reason: cancelReason });
      setShowCancel(false);
    } catch {
      // handled
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-primary-200 border-t-primary-700" />
      </div>
    );
  }

  if (!ticket) return null;

  const canCancel = ['reserved', 'confirmed'].includes(ticket.status);

  return (
    <div className="px-4 py-6 max-w-lg mx-auto">
      <button onClick={() => navigate(-1)} className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 mb-4">
        <ArrowLeft className="w-4 h-4" />
        {t('common.back')}
      </button>

      {/* Ticket card */}
      <div className="card overflow-hidden">
        {/* Header */}
        <div className="bg-primary-700 px-5 py-4 text-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium opacity-80">{ticket.agency_name}</span>
            <StatusBadge status={ticket.status} />
          </div>
          <RouteDisplay
            origin={ticket.origin_city}
            destination={ticket.destination_city}
            compact
          />
          <div className="flex items-center gap-4 mt-2 text-sm opacity-80">
            <span>{formatDate(ticket.departure_date)}</span>
            <span>{formatTime(ticket.departure_time)}</span>
          </div>
        </div>

        {/* QR Code */}
        {ticket.qr_code_url && (
          <div className="flex flex-col items-center py-6 border-b border-dashed border-gray-200">
            <img src={ticket.qr_code_url} alt="QR Code" className="w-40 h-40 mb-2" />
            <p className="text-xs text-gray-500">{t('ticket.show_qr')}</p>
          </div>
        )}

        {/* Details */}
        <div className="p-5 space-y-3">
          <DetailRow label={t('ticket.code')} value={ticket.code} mono />
          <DetailRow label="Ref" value={ticket.booking_reference} mono />
          <DetailRow label={t('ticket.seat')} value={ticket.seat_number} />
          <DetailRow label={t('ticket.passenger')} value={ticket.passenger_name} />
          <DetailRow label="Tel" value={ticket.passenger_phone} />
          <DetailRow label="Prix" value={formatXOF(ticket.price)} />
          {ticket.bus_model && <DetailRow label="Bus" value={ticket.bus_model} />}
          {ticket.cancellation_reason && (
            <DetailRow label={t('ticket.cancel_reason')} value={ticket.cancellation_reason} />
          )}
        </div>

        {/* Actions */}
        {canCancel && (
          <div className="px-5 pb-5">
            {showCancel ? (
              <div className="space-y-3">
                <textarea
                  value={cancelReason}
                  onChange={(e) => setCancelReason(e.target.value)}
                  className="input-field"
                  placeholder={t('ticket.cancel_reason')}
                  rows={2}
                />
                <div className="flex gap-2">
                  <button
                    onClick={handleCancel}
                    disabled={cancelMutation.isPending}
                    className="btn-danger flex-1 flex items-center justify-center gap-2"
                  >
                    <X className="w-4 h-4" />
                    {t('common.confirm')}
                  </button>
                  <button
                    onClick={() => setShowCancel(false)}
                    className="btn-secondary flex-1"
                  >
                    {t('common.cancel')}
                  </button>
                </div>
              </div>
            ) : (
              <button
                onClick={() => setShowCancel(true)}
                className="w-full py-3 text-red-600 bg-red-50 rounded-xl font-medium hover:bg-red-100 transition-colors"
              >
                {t('ticket.cancel')}
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function DetailRow({ label, value, mono }) {
  return (
    <div className="flex items-center justify-between py-1">
      <span className="text-sm text-gray-500">{label}</span>
      <span className={`text-sm font-medium text-gray-900 ${mono ? 'font-mono' : ''}`}>{value}</span>
    </div>
  );
}
