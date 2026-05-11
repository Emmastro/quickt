import { Link } from 'react-router-dom';
import { Users, ChevronRight } from 'lucide-react';
import { t } from '../../i18n';
import { useAgencyDepartures, useUpdateDepartureStatus } from '../../hooks/useDepartures';
import { formatDate, formatTime, formatXOF } from '../../utils/format';
import StatusBadge from '../../components/common/StatusBadge';

const NEXT_STATUS = {
  scheduled: 'boarding',
  boarding: 'departed',
  departed: 'completed',
};

export default function ManageDeparturesPage() {
  const { data, isLoading } = useAgencyDepartures();
  const updateStatus = useUpdateDepartureStatus();
  const departures = data?.items || [];

  if (isLoading) {
    return (
      <div className="flex justify-center py-20">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-primary-200 border-t-primary-700" />
      </div>
    );
  }

  return (
    <div className="px-4 py-6 max-w-4xl mx-auto">
      <h1 className="text-xl font-bold text-gray-900 mb-5">{t('agency.departures')}</h1>

      {departures.length === 0 ? (
        <div className="card p-8 text-center text-gray-500">Aucun depart</div>
      ) : (
        <div className="space-y-2">
          {departures.map((dep) => {
            const nextStatus = NEXT_STATUS[dep.status];
            const booked = dep.total_seats - dep.available_seats;
            return (
              <div key={dep.id} className="card p-4">
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <div className="font-medium text-gray-900">
                      {formatDate(dep.departure_date)} — {formatTime(dep.departure_time)}
                    </div>
                    <div className="text-sm text-gray-500">
                      {booked}/{dep.total_seats} passagers — {formatXOF(dep.price)}
                    </div>
                  </div>
                  <StatusBadge status={dep.status} />
                </div>
                <div className="flex items-center gap-2 mt-2">
                  {nextStatus && (
                    <button
                      onClick={() => updateStatus.mutate({ id: dep.id, status: nextStatus })}
                      className="text-sm text-primary-600 font-medium hover:text-primary-800 flex items-center gap-1"
                    >
                      <ChevronRight className="w-4 h-4" />
                      {nextStatus}
                    </button>
                  )}
                  <Link
                    to={`/app/agency/passengers/${dep.id}`}
                    className="text-sm text-gray-500 hover:text-gray-700 flex items-center gap-1 ml-auto"
                  >
                    <Users className="w-4 h-4" />
                    Passagers
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
