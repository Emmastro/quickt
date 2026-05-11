import { Building2, Bus, Calendar, Users } from 'lucide-react';
import { t } from '../../i18n';
import { useAgencyDepartures } from '../../hooks/useDepartures';

export default function AgencyDashboardPage() {
  const { data: departuresData, isLoading } = useAgencyDepartures();

  const departures = departuresData?.items || [];
  const today = new Date().toISOString().split('T')[0];
  const todayDepartures = departures.filter((d) => d.departure_date === today);
  const totalPassengers = departures.reduce((sum, d) => sum + d.total_seats - d.available_seats, 0);

  const stats = [
    { icon: Calendar, label: "Departs aujourd'hui", value: todayDepartures.length, color: 'bg-blue-100 text-blue-700' },
    { icon: Users, label: 'Total passagers', value: totalPassengers, color: 'bg-green-100 text-green-700' },
    { icon: Bus, label: 'Total departs', value: departures.length, color: 'bg-purple-100 text-purple-700' },
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-primary-200 border-t-primary-700" />
      </div>
    );
  }

  return (
    <div className="px-4 py-6 max-w-4xl mx-auto">
      <h1 className="text-xl font-bold text-gray-900 mb-5">{t('agency.dashboard')}</h1>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        {stats.map(({ icon: Icon, label, value, color }) => (
          <div key={label} className="card p-4">
            <div className="flex items-center gap-3">
              <div className={`w-10 h-10 ${color} rounded-xl flex items-center justify-center`}>
                <Icon className="w-5 h-5" />
              </div>
              <div>
                <div className="text-2xl font-bold text-gray-900">{value}</div>
                <div className="text-xs text-gray-500">{label}</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Upcoming departures */}
      <h2 className="font-semibold text-gray-900 mb-3">Prochains departs</h2>
      {todayDepartures.length === 0 ? (
        <div className="card p-6 text-center text-gray-500">
          Aucun depart programme aujourd'hui
        </div>
      ) : (
        <div className="space-y-2">
          {todayDepartures.map((dep) => (
            <div key={dep.id} className="card p-4 flex items-center justify-between">
              <div>
                <div className="font-medium text-gray-900">{dep.departure_time?.substring(0, 5)}</div>
                <div className="text-xs text-gray-500">
                  {dep.total_seats - dep.available_seats}/{dep.total_seats} passagers
                </div>
              </div>
              <span className={`status-badge ${
                dep.status === 'scheduled' ? 'bg-blue-100 text-blue-800' :
                dep.status === 'boarding' ? 'bg-indigo-100 text-indigo-800' :
                'bg-gray-100 text-gray-600'
              }`}>
                {dep.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
