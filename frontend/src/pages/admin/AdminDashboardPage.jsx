import { Building2, Users, MapPin, Ticket } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { agenciesService } from '../../services/agencies.service';
import { routesService } from '../../services/routes.service';
import { t } from '../../i18n';

export default function AdminDashboardPage() {
  const { data: agenciesData } = useQuery({ queryKey: ['agencies'], queryFn: () => agenciesService.list() });
  const { data: routesData } = useQuery({ queryKey: ['routes'], queryFn: () => routesService.list() });

  const agencies = agenciesData?.items || agenciesData || [];
  const routes = routesData?.items || routesData || [];

  const stats = [
    { icon: Building2, label: 'Agences', value: agencies.length, color: 'bg-blue-100 text-blue-700' },
    { icon: MapPin, label: 'Itineraires', value: routes.length, color: 'bg-green-100 text-green-700' },
  ];

  return (
    <div className="px-4 py-6 max-w-4xl mx-auto">
      <h1 className="text-xl font-bold text-gray-900 mb-5">{t('admin.dashboard')}</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
        {stats.map(({ icon: Icon, label, value, color }) => (
          <div key={label} className="card p-5">
            <div className="flex items-center gap-3">
              <div className={`w-12 h-12 ${color} rounded-xl flex items-center justify-center`}>
                <Icon className="w-6 h-6" />
              </div>
              <div>
                <div className="text-3xl font-bold text-gray-900">{value}</div>
                <div className="text-sm text-gray-500">{label}</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <h2 className="font-semibold text-gray-900 mb-3">Agences recentes</h2>
      <div className="space-y-2">
        {agencies.slice(0, 5).map((agency) => (
          <div key={agency.id} className="card p-4 flex items-center justify-between">
            <div>
              <div className="font-medium text-gray-900">{agency.name}</div>
              <div className="text-sm text-gray-500">{agency.city} — {agency.region}</div>
            </div>
            <span className={`status-badge ${
              agency.status === 'approved' ? 'bg-green-100 text-green-800' :
              agency.status === 'pending' ? 'bg-amber-100 text-amber-800' :
              'bg-red-100 text-red-800'
            }`}>
              {agency.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
