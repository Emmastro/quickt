import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Check, X } from 'lucide-react';
import { agenciesService } from '../../services/agencies.service';
import { t } from '../../i18n';
import StatusBadge from '../../components/common/StatusBadge';
import { showToast } from '../../utils/toast';

export default function AdminAgenciesPage() {
  const queryClient = useQueryClient();
  const { data, isLoading } = useQuery({ queryKey: ['agencies'], queryFn: () => agenciesService.list() });

  const approveMutation = useMutation({
    mutationFn: agenciesService.approve,
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['agencies'] }); showToast.success('Agence approuvee'); },
  });

  const suspendMutation = useMutation({
    mutationFn: agenciesService.suspend,
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['agencies'] }); showToast.success('Agence suspendue'); },
  });

  const agencies = data?.items || data || [];

  return (
    <div className="px-4 py-6 max-w-4xl mx-auto">
      <h1 className="text-xl font-bold text-gray-900 mb-5">{t('admin.agencies')}</h1>

      {isLoading ? (
        <div className="flex justify-center py-10">
          <div className="animate-spin rounded-full h-8 w-8 border-4 border-primary-200 border-t-primary-700" />
        </div>
      ) : (
        <div className="space-y-2">
          {agencies.map((agency) => (
            <div key={agency.id} className="card p-4">
              <div className="flex items-center justify-between mb-2">
                <div>
                  <div className="font-medium text-gray-900">{agency.name}</div>
                  <div className="text-sm text-gray-500">{agency.city} — {agency.email}</div>
                </div>
                <StatusBadge status={agency.status} />
              </div>
              <div className="flex items-center gap-2 mt-2">
                {agency.status !== 'approved' && (
                  <button
                    onClick={() => approveMutation.mutate(agency.id)}
                    className="flex items-center gap-1 text-sm text-green-600 font-medium hover:text-green-800"
                  >
                    <Check className="w-4 h-4" />
                    Approuver
                  </button>
                )}
                {agency.status !== 'suspended' && (
                  <button
                    onClick={() => suspendMutation.mutate(agency.id)}
                    className="flex items-center gap-1 text-sm text-red-600 font-medium hover:text-red-800"
                  >
                    <X className="w-4 h-4" />
                    Suspendre
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
