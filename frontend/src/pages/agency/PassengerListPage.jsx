import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, CheckCircle } from 'lucide-react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ticketsService } from '../../services/tickets.service';
import { t } from '../../i18n';
import StatusBadge from '../../components/common/StatusBadge';
import { showToast } from '../../utils/toast';

export default function PassengerListPage() {
  const { departureId } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['passengers', departureId],
    queryFn: () => ticketsService.getDeparturePassengers(departureId),
  });

  const markUsed = useMutation({
    mutationFn: ticketsService.markUsed,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['passengers', departureId] });
      showToast.success('Billet valide');
    },
  });

  const tickets = data?.items || [];

  return (
    <div className="px-4 py-6 max-w-4xl mx-auto">
      <button onClick={() => navigate(-1)} className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 mb-4">
        <ArrowLeft className="w-4 h-4" />
        {t('common.back')}
      </button>

      <h1 className="text-xl font-bold text-gray-900 mb-5">
        {t('agency.passengers')} ({tickets.length})
      </h1>

      {isLoading ? (
        <div className="flex justify-center py-10">
          <div className="animate-spin rounded-full h-8 w-8 border-4 border-primary-200 border-t-primary-700" />
        </div>
      ) : tickets.length === 0 ? (
        <div className="card p-8 text-center text-gray-500">Aucun passager</div>
      ) : (
        <div className="space-y-2">
          {tickets.map((ticket) => (
            <div key={ticket.id} className="card p-4 flex items-center justify-between">
              <div>
                <div className="font-medium text-gray-900">{ticket.passenger_name}</div>
                <div className="text-sm text-gray-500">
                  {t('ticket.seat')}: {ticket.seat_number} — {ticket.passenger_phone}
                </div>
                <div className="text-xs text-gray-400 font-mono">{ticket.code}</div>
              </div>
              <div className="flex items-center gap-2">
                <StatusBadge status={ticket.status} />
                {ticket.status === 'confirmed' && (
                  <button
                    onClick={() => markUsed.mutate(ticket.id)}
                    className="p-2 text-green-600 hover:bg-green-50 rounded-lg"
                    title="Valider"
                  >
                    <CheckCircle className="w-5 h-5" />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
